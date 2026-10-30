# Daggerheart — O Arquivo da Mesa

Site para PC, tablet e celular. Abra no navegador, sem instalar aplicativos ou iniciar servidores:

**https://rpersolli.github.io/daggerheart-arquivo-local/**

- Biblioteca com 14 PDFs gratuitos oficiais e suas capas.
- Leitor de PDF dentro do site, navegação e busca por texto.
- Importação de livros pessoais e fichas já preenchidas.
- Edição dos campos sobre a ficha, salvamento no aparelho e exportação em PDF.
- Substituição visual de texto em PDFs sem campos (sem OCR; não remove o texto subjacente).
- Caderno pessoal com exportação de backup.

Fichas e livros importados ficam apenas no navegador de cada usuário, sem envio ao GitHub e sem sincronização entre aparelhos. Faça backup dos PDFs editados. O livro básico comercial não é redistribuído; pode ser importado na biblioteca pessoal.

## Código e publicação

A interface está em `docs/`. O workflow `.github/workflows/pages.yml` executa `build_web.py` para baixar as bibliotecas PDF.js e pdf-lib, os materiais gratuitos oficiais e gerar as capas, publicando tudo no GitHub Pages.

Consulte [WEB.md](WEB.md) para detalhes de privacidade, funcionamento e limitações. Os scripts do antigo modo local foram preservados, mas não são necessários para acessar o site.

Projeto pessoal não oficial de Daggerheart. Materiais e bibliotecas mantêm suas respectivas titularidades e licenças.
