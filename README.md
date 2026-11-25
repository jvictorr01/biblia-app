# Flux Biblia

Bíblia de estudo (ACF, NVI e paralelo) com números de Strong, referências cruzadas, anotações, destaques, marcações e progresso de leitura.

## Gerar o .ipa e o .apk

Cada push na branch `main` dispara o workflow **Gerar .ipa e .apk** no GitHub Actions. Também dá para rodar manualmente em **Actions → Gerar .ipa e .apk → Run workflow**.

Ao terminar, o `FluxBiblia.ipa` e o `FluxBiblia.apk` ficam disponíveis em **Releases** (links diretos da versão mais recente: `releases/latest/download/FluxBiblia.ipa` e `releases/latest/download/FluxBiblia.apk`) e também como artefatos na página da execução.

## Instalar no iPhone (Sideloadly)

1. Conecte o iPhone ao Mac e abra o Sideloadly.
2. Arraste o `FluxBiblia.ipa` para a janela.
3. Informe seu Apple ID e clique em **Start**.
4. No iPhone: Ajustes → Geral → VPN e Gerenciamento de Dispositivos → confie no seu Apple ID.
5. Se pedir, ative o Modo de Desenvolvedor em Ajustes → Privacidade e Segurança.

Com Apple ID gratuito, a assinatura vale 7 dias; reinstale pelo Sideloadly depois disso.

## Instalar no Android

1. Baixe o `FluxBiblia.apk` no celular.
2. Toque no arquivo e permita a instalação de apps dessa origem quando o Android pedir.

O `.apk` é um build de debug: não expira, mas não serve para publicar na Play Store.

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
