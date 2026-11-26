#!/usr/bin/env python3
"""Converte a coleta de comentários do TheBibleSays.com (Markdown) em
www/data/com/<livro>.json, no formato que o app lê:
    [[capitulo, versiculo_inicial, versiculo_final, titulo, resumo, html], ...]

Uso: python3 tools/build_commentary.py ~/Downloads/tbs-comentarios-pt.json
"""
import html
import json
import re
import sys
from pathlib import Path

CODES = ["gen","exo","lev","num","deu","jos","jdg","rut","1sa","2sa","1ki","2ki","1ch","2ch","ezr","neh","est","job","psa","pro","ecc","sng","isa","jer","lam","ezk","dan","hos","jol","amo","oba","jon","mic","nam","hab","zep","hag","zec","mal","mat","mrk","luk","jhn","act","rom","1co","2co","gal","eph","php","col","1th","2th","1ti","2ti","tit","phm","heb","jas","1pe","2pe","1jn","2jn","3jn","jud","rev"]
ALIASES = {"joe": "jol", "nah": "nam", "eze": "ezk"}
IDX = {c: i for i, c in enumerate(CODES)}
COM_URL = re.compile(r"^https://thebiblesays\.com/pt/commentary/([0-9a-z]{3})\+(\d+)(?::(\d+))?(?:\.md)?$")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def book_index(code):
    return IDX.get(ALIASES.get(code, code))


def parse_front(fm):
    out = {}
    for line in fm.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        try:
            out[k.strip()] = json.loads(v)
        except ValueError:
            out[k.strip()] = v
    return out


def inline(text):
    parts, last = [], 0
    for m in LINK.finditer(text):
        parts.append(fmt(text[last:m.start()]))
        label, url = fmt(m.group(1)), m.group(2)
        cm = COM_URL.match(url)
        b = book_index(cm.group(1)) if cm else None
        if b is not None:
            parts.append(f'<span class="lk" data-com="{b}.{cm.group(2)}.{cm.group(3) or 1}">{label}</span>')
        elif url.startswith("https://"):
            parts.append(f'<a href="{html.escape(url)}" data-ext>{label}</a>')
        else:
            parts.append(label)
        last = m.end()
    parts.append(fmt(text[last:]))
    return "".join(parts)


def fmt(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    return t


def md_to_html(body):
    out, items, ltag = [], [], None

    def flush():
        nonlocal items, ltag
        if items:
            out.append(f"<{ltag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{ltag}>")
        items, ltag = [], None

    para = []

    def flush_para():
        nonlocal para
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
        para = []

    for line in body.strip().splitlines():
        if not line.strip():
            flush_para()
            flush()
            continue
        m = re.match(r"^\s*([-*]|\d+\.)\s+(.*)", line)
        h = re.match(r"^#{1,6}\s+(.*)", line)
        if m and not re.match(r"^\*[^*\s]", line.strip()):
            flush_para()
            tag = "ol" if m.group(1)[0].isdigit() else "ul"
            if ltag and ltag != tag:
                flush()
            ltag = tag
            items.append(m.group(2))
        elif items and line.startswith((" ", "\t")):
            items[-1] += " " + line.strip()
        elif h:
            flush_para()
            flush()
            out.append(f"<h4>{inline(h.group(1))}</h4>")
        else:
            flush()
            para.append(line.strip())
    flush_para()
    flush()
    return "".join(out)


def convert(md):
    if not md.startswith("---"):
        return None
    _, fm, body = md.split("---", 2)
    meta = parse_front(fm)
    # corta o rodapé de navegação (Previous/Next/Canonical)
    cut = body.rfind("\n---\n")
    if cut >= 0 and "Canonical page:" in body[cut:]:
        body = body[:cut]
    lines = body.strip().splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    body = "\n".join(lines).strip()
    desc = (meta.get("description") or "").strip()
    first = body.split("\n\n", 1)
    if first and first[0].strip().strip("*").strip() == desc:
        body = first[1] if len(first) > 1 else ""
    return meta, desc, md_to_html(body)


def main(src):
    raw = json.loads(Path(src).read_text(encoding="utf-8"))
    books = {i: [] for i in range(66)}
    skipped = []
    for path, md in raw.items():
        m = re.match(r"^/pt/commentary/([0-9a-z]{3})\+(\d+)(?::(\d+))?$", path)
        b = book_index(m.group(1)) if m else None
        r = convert(md) if b is not None else None
        if not r:
            skipped.append(path)
            continue
        meta, desc, body = r
        title = meta.get("title", "")
        if "em breve" in title.lower() or len(body) < 80:
            skipped.append(path)
            continue
        c = int(meta.get("chapter") or m.group(2))
        vs = int(meta.get("verse_start") or m.group(3) or 1)
        ve = int(meta.get("verse_end") or vs)
        books[b].append([c, vs, ve, title, desc, body])
    out = Path(__file__).resolve().parent.parent / "www" / "data" / "com"
    out.mkdir(parents=True, exist_ok=True)
    total = 0
    for b, lst in books.items():
        lst.sort(key=lambda e: (e[0], e[1]))
        (out / f"{b}.json").write_text(json.dumps(lst, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        total += len(lst)
    empty = [CODES[b] for b, l in books.items() if not l]
    print(f"{total} comentários em {66 - len(empty)} livros; ignorados: {len(skipped)}")
    if empty:
        print("livros sem comentário:", " ".join(empty))
    for p in skipped[:15]:
        print("  ignorado:", p)


if __name__ == "__main__":
    main(sys.argv[1])
