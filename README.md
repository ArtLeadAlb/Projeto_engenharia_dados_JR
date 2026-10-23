Projeto de Engenharia de Dados JR — Python e SQLite3
1. Sobre o projeto

Este projeto tem como objetivo desenvolver uma aplicação de Engenharia de Dados utilizando Python e SQLite3, aplicando conceitos fundamentais de modelagem relacional, manipulação de dados, consultas SQL, integridade referencial e organização de código.

A aplicação simula um pequeno sistema de vendas, armazenando informações sobre clientes, produtos, pedidos e itens dos pedidos.

O projeto foi desenvolvido com foco em boas práticas de programação, modularização, reutilização de funções e organização de um banco de dados relacional.

2. Objetivos
Criar um banco de dados relacional utilizando SQLite3.
Implementar tabelas com chaves primárias e estrangeiras.
Popular as tabelas com dados de exemplo.
Desenvolver consultas SQL para análise de vendas.
Organizar o código Python em funções e módulos.
Criar um menu interativo no terminal.
Validar a estrutura do banco e a integridade referencial.
Manter os arquivos de código separados dos arquivos de dados.
3. Tecnologias utilizadas
Python 3: linguagem utilizada no desenvolvimento da aplicação.
SQLite3: banco de dados relacional incorporado ao Python.
SQL: linguagem utilizada para criação, inserção, consulta e validação dos dados.
Git e GitHub: versionamento e publicação do projeto.

Não é necessário instalar um servidor de banco de dados ou uma biblioteca externa para utilizar SQLite3, pois o módulo sqlite3 já faz parte da biblioteca padrão do Python.

4. Estrutura do projeto

A organização dos diretórios foi definida para separar os scripts Python do banco de dados.

Projeto_engenharia_dados_JR/
│
├── data/
│   └── vendas.db
│
├── src/
│   ├── main.py
│   ├── conexao.py
│   ├── criar_tabelas.py
│   ├── inserir_dados.py
│   ├── validar_dados.py
│   └── relatorios.py
│
├── README.md
└── .gitignore

Responsabilidade dos arquivos
Arquivo	Responsabilidade
src/main.py	Apresenta o menu interativo e coordena a execução das funcionalidades.
src/conexao.py	Centraliza o caminho do banco e as funções de conexão e consulta.
src/criar_tabelas.py	Cria as tabelas e os relacionamentos do banco.
src/inserir_dados.py	Insere os dados de exemplo nas tabelas.
src/validar_dados.py	Verifica a existência das tabelas, a quantidade de registros e a integridade referencial.
src/relatorios.py	Contém as consultas SQL utilizadas nos relatórios.
data/vendas.db	Arquivo físico do banco de dados SQLite.

O caminho do banco é definido centralmente em conexao.py. Como o arquivo está dentro de src, o caminho é calculado a partir da localização do próprio script, permitindo utilizar data/vendas.db na raiz do projeto independentemente do diretório de execução.

5. Modelagem do banco de dados

O banco de dados contém quatro tabelas relacionadas.

Tabela clientes

Armazena as informações dos clientes.

Principais campos:

id_cliente: chave primária.
nome: nome do cliente.
email: e-mail único do cliente.
cidade: cidade do cliente.
Tabela produtos

Armazena o catálogo de produtos disponíveis.

Principais campos:

id_produto: chave primária.
nome: nome do produto.
categoria: categoria do produto.
preco: preço do produto.
estoque: quantidade disponível em estoque.
Tabela pedidos

Registra os pedidos realizados pelos clientes.

Principais campos:

id_pedido: chave primária.
id_cliente: chave estrangeira que referencia clientes.
data_pedido: data e hora do pedido.
status: situação do pedido.
Tabela itens_pedido

Registra os produtos incluídos em cada pedido.

Principais campos:

id_item: chave primária.
id_pedido: chave estrangeira que referencia pedidos.
id_produto: chave estrangeira que referencia produtos.
quantidade: quantidade do produto comprado.
preco_unitario: preço do produto no momento da venda.
Relacionamentos
Um cliente pode realizar vários pedidos.
Um pedido pertence a um único cliente.
Um pedido pode conter vários itens.
Um produto pode aparecer em vários itens de pedidos.
A tabela itens_pedido relaciona pedidos e produtos.

O modelo utiliza chaves primárias, chaves estrangeiras e restrições de integridade para manter a consistência dos dados.

6. Processo de desenvolvimento
Etapa 1 — Criação do banco de dados

Foi criada uma função para centralizar o acesso ao banco SQLite e garantir que o arquivo seja armazenado no diretório data.

O arquivo criar_tabelas.py contém funções específicas para a criação de cada tabela, utilizando comandos CREATE TABLE IF NOT EXISTS.

Essa abordagem permite executar novamente a criação sem apagar as tabelas existentes.

Etapa 2 — Carga de dados

O arquivo inserir_dados.py foi organizado em funções responsáveis pela inserção de:

Clientes.
Produtos.
Pedidos.
Itens dos pedidos.

As operações utilizam consultas parametrizadas e executemany() para inserir múltiplos registros.

A carga utiliza transação, com commit() para confirmar as alterações e rollback() para desfazê-las em caso de erro.

Também são utilizadas verificações para evitar a inserção duplicada de registros em condições previstas pelo código.

Etapa 3 — Validação dos dados

O arquivo validar_dados.py permite verificar:

A existência das quatro tabelas.
A quantidade de registros em cada tabela.
A integridade referencial por meio do comando PRAGMA foreign_key_check.

Essas verificações ajudam a identificar problemas estruturais e inconsistências nos relacionamentos.

Etapa 4 — Consultas SQL e relatórios

O arquivo relatorios.py centraliza as consultas SQL, separando a lógica de acesso aos dados da interface do usuário.

Os relatórios utilizam consultas SQL para relacionar tabelas, agregar valores e apresentar informações relevantes para a análise das vendas.

Etapa 5 — Menu interativo

O arquivo main.py disponibiliza um menu no terminal para executar as funcionalidades do sistema sem precisar chamar cada script manualmente.

As opções incluem:

Gerar banco de dados.
Popular banco de dados.
Listar clientes.
Listar produtos.
Consultar pedidos por cliente.
Consultar o detalhamento dos pedidos.
Consultar o valor total por pedido.
Consultar o faturamento por cliente.
Identificar os produtos mais vendidos.
Consultar pedidos por status.
Consultar o faturamento por cidade.
Consultar pedidos pendentes.
Consultar vendas por período.
Consultar o resumo geral das vendas.
Sair do sistema.

Os relatórios são executados a partir das funções definidas em relatorios.py.

7. Como executar o projeto
Pré-requisitos
Python 3 instalado.
Git instalado, caso queira clonar o repositório.
Passo 1 — Clonar o repositório

Depois de publicar o projeto no GitHub, execute:

git clone URL_DO_SEU_REPOSITORIO


Entre na pasta do projeto:

cd Projeto_engenharia_dados_JR


Substitua URL_DO_SEU_REPOSITORIO pelo endereço real do repositório.

Passo 2 — Gerar o banco e popular os dados

Execute o menu principal a partir da raiz do projeto:

python src/main.py


No menu:

Selecione a opção 1 para gerar o banco de dados e as tabelas.
Selecione a opção 2 para popular o banco de dados.
Selecione uma das opções de relatório para consultar os dados.

Em sistemas nos quais o comando python não estiver configurado, pode ser necessário utilizar python3 ou, no Windows, py.

Passo 3 — Validar os dados

Para executar as verificações diretamente:

python src/validar_dados.py


O programa apresentará a quantidade de registros por tabela e o resultado da verificação das chaves estrangeiras.

Passo 4 — Executar os relatórios

Para acessar os relatórios, execute:

python src/main.py


Escolha a opção desejada e siga as instruções exibidas no terminal.

8. Boas práticas aplicadas

Durante o desenvolvimento, foram aplicadas as seguintes práticas:

Modularização: divisão do código em arquivos com responsabilidades específicas.
Funções: organização das operações em funções reutilizáveis.
Integridade referencial: utilização de chaves estrangeiras e restrições.
Consultas parametrizadas: utilização de parâmetros SQL para reduzir riscos de SQL injection em consultas que recebem valores externos.
Transações: utilização de commit() e rollback() para controlar a gravação dos dados.
Tratamento de erros: captura de exceções relacionadas às operações no banco.
Centralização da conexão: reutilização das funções definidas em conexao.py.
Organização de diretórios: separação entre código-fonte e dados.
Validação: verificação da estrutura e da integridade do banco.
9. Possíveis melhorias futuras

O projeto pode evoluir com novas funcionalidades, como:

Implementação de um pipeline ETL completo.
Extração de dados de arquivos CSV e Excel.
Transformação, limpeza e padronização dos dados.
Implementação de logs para monitorar a execução das cargas.
Criação de testes automatizados.
Controle de qualidade dos dados.
Exportação dos relatórios para CSV ou Excel.
Desenvolvimento de dashboards para visualização dos indicadores.
Automação da execução das cargas de dados.
Versionamento do esquema do banco de dados.
10. Considerações finais

Este projeto representa uma aplicação prática dos fundamentos de Engenharia de Dados utilizando Python, SQL e SQLite3.

A solução demonstra como estruturar um banco relacional, carregar dados, validar relacionamentos e desenvolver consultas para transformar registros operacionais em informações úteis para análise.

A organização modular também facilita a manutenção do código e a implementação de novas funcionalidades.

Projeto: Projeto de Engenharia de Dados JR
Tecnologias: Python, SQLite3 e SQL
Área: Engenharia de Dados

Aluno: Arthur Albuquerque