# Versão web — GitHub Pages

A versão web fica em `docs/`. Não precisa executar Python, instalar aplicativo nem abrir `.cmd` para usar o site. O workflow `.github/workflows/pages.yml` prepara os materiais oficiais e publica o conteúdo estático.

## Biblioteca

O build baixa os 14 PDFs gratuitos listados em `official-downloads.json`, das URLs oficiais de Daggerheart, e gera suas capas. Eles são servidos junto com o site. O livro básico comercial e os PDFs particulares não são redistribuídos na publicação. Cada usuário pode adicioná-los à biblioteca pessoal do navegador e lê-los no próprio site.

## Fichas

Importe PDFs preenchidos em Minhas fichas. O site lê os valores existentes e mostra os campos de formulário diretamente sobre a página. Use Salvar neste aparelho e Baixar PDF editado para guardar uma cópia. Campos de texto, checkbox, dropdown e grupos de rádio são suportados. Não há OCR para manuscritos ou scans.

Para PDFs sem campos, Editar texto visível permite substituir visualmente trechos identificáveis por cobertura branca e novo texto. Isso não remove o texto subjacente, não é redação segura e pode exigir ajustes de layout. PDFs escaneados não possuem trechos de texto selecionáveis; importe uma versão preenchível.

## Privacidade e armazenamento

Fichas e livros pessoais ficam no IndexedDB do navegador; notas ficam no armazenamento local. Não são enviados ao GitHub nem compartilhados automaticamente com outros usuários/dispositivos. Limpar os dados do navegador pode apagá-los. Exporte PDFs e notas para backup. A hospedagem é pública, sem contas.

## Publicação

Em Settings → Pages, selecione GitHub Actions como Source. A conta precisa permitir Pages nesse repositório; em planos gratuitos ele precisa ser público. Os arquivos antigos do modo local continuam no histórico, mas o site usa somente `docs/`.

O build usa PDF.js 4.10.38 (Apache-2.0) e pdf-lib 1.17.1 (MIT), baixados do registro npm via jsDelivr. Materiais do jogo mantêm suas respectivas titularidades. Projeto pessoal não oficial.
