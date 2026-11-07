# Flux Biblia

Bíblia de estudo (ACF, NVI e paralelo) com números de Strong, referências cruzadas, anotações, destaques, marcações e progresso de leitura.

## Gerar o .ipa

Cada push na branch `main` dispara o workflow **Gerar .ipa (iOS, sem assinatura)** no GitHub Actions. Também dá para rodar manualmente em **Actions → Gerar .ipa → Run workflow**.

Ao terminar, o `FluxBiblia.ipa` fica disponível em **Releases** (link direto da versão mais recente: `releases/latest/download/FluxBiblia.ipa`) e também como artefato na página da execução.

## Instalar no iPhone (Sideloadly)

1. Conecte o iPhone ao Mac e abra o Sideloadly.
2. Arraste o `FluxBiblia.ipa` para a janela.
3. Informe seu Apple ID e clique em **Start**.
4. No iPhone: Ajustes → Geral → VPN e Gerenciamento de Dispositivos → confie no seu Apple ID.
5. Se pedir, ative o Modo de Desenvolvedor em Ajustes → Privacidade e Segurança.

Com Apple ID gratuito, a assinatura vale 7 dias; reinstale pelo Sideloadly depois disso.

## Estrutura

- `www/` — o app (HTML/CSS/JS) e os dados em JSON
- `assets/` — ícone e splash usados para gerar os recursos do iOS
- `capacitor.config.json` — configuração do Capacitor
- `.github/workflows/ios.yml` — compilação na nuvem

## Textos e licenças

- Almeida Corrigida Fiel — © Sociedade Bíblica Trinitariana do Brasil. Usada com permissão.
- Nova Versão Internacional — © Biblica, Inc. Usada com permissão.
- King James (1769) com números de Strong — domínio público.
- Dicionários de Strong — domínio público; versão digital © Open Scriptures (CC BY-SA).
- Referências cruzadas — OpenBible.info (CC BY).
