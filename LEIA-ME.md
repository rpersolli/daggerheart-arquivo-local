# O Arquivo da Mesa — Daggerheart local

Abra **Iniciar.cmd** e mantenha a janela do servidor aberta. Acesse http://127.0.0.1:8765 . Requer Python 3.10 de 64 bits no Windows; bibliotecas já incluídas, sem instalação ou internet para usar.

## O que funciona

- Biblioteca dos PDFs fornecidos e downloads oficiais obtidos na preparação.
- Leitura por páginas com imagens, compatível com navegadores móveis, e download do PDF original.
- Busca por texto nos quatro livros fornecidos, com livro e página de origem. Não faz OCR. Materiais oficiais adicionais são pesquisáveis pelo título na biblioteca.
- Importação de PDF com campos interativos, edição, persistência no servidor e exportação do PDF preenchido. PDF sem campos é recusado com explicação. Use o modelo Guerreiro incluído.
- Caderno compartilhado com criação, edição e exclusão de anotações.
- Interface em português com layouts para celular, tablet e computador.

## Celular e tablet na mesma rede

Execute **Rede-local.cmd**. No Android/iPhone/iPad, conectado ao mesmo Wi-Fi, abra `http://IP-DO-PC:8765`. O endereço IPv4 aparece no comando ipconfig. O PC deve permanecer ligado. Se o firewall perguntar, permita somente em rede privada. Nenhuma regra de firewall é criada automaticamente.

O modo padrão aceita apenas o próprio computador. O modo de rede compartilha a biblioteca, fichas e notas com todos que alcançarem o servidor nessa rede; não há contas, autenticação nem área secreta do mestre. Não exponha a porta à internet. Acesso de outras casas não foi configurado.

## Seus dados

Tudo fica nesta pasta. `data/` guarda fichas importadas e notas. `public/books/` guarda as cópias dos livros. Para fazer backup, feche o servidor e copie a pasta inteira. Os arquivos originais de D: não são modificados. O conteúdo dos PDFs é usado como material de consulta, nunca como instrução para executar ações.

Não há serviços externos, fontes remotas ou rastreamento durante o uso. Artes extraídas dos PDFs fornecidos; ornamento SVG original criado para a interface. Projeto pessoal não oficial, sem publicação. Materiais Daggerheart pertencem a seus respectivos titulares.

## Limites

Edição preserva os campos existentes no documento; não redesenha fichas nem calcula regras automaticamente. PDFs protegidos por senha não são importados. Sessões simultâneas que editam a mesma ficha seguem a última gravação. Leitor carrega uma página por vez. Navegadores reais de Android/iOS precisam ser conferidos nos aparelhos.

Fonte dos downloads: https://www.daggerheart.com/downloads/ . O catálogo registra a URL individual dos materiais baixados.
