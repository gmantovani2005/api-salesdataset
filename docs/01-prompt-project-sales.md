## Objetivo
Criar uma API em FastAPI com o banco de dados Postgresql e documentação swagger. O projeto foi instruturado inicialmente utilizando o comando `uv`.

## Requisitos
- O banco de dados já está criado conforme o arquivo `docs/schema.sql`. Utilize este arquivo para definir os modelos, DTOs e relacionamentos.
- Crie um arquivo `.env.example` na raiz do projeto para definir as variáveis de ambiente necessárias.
- Crie todo o CRUD de cada tabela. Sempre que possível utilize o `SQLAlchemy` para interagir com o banco de dados.
- Rotas de Listagem devem ser capazes de retornar todos os registros e permitir filtros.

## Ao Finalizar
- Gere o arquivo README.md com o explicação de cada pasta e arquivo criado.
- Gere os arquivos `docker-compose.yml`, `dockerfile` e `kubernetes.yml` para rodar todo o projeto. O Postgresql já está executando mas mesmo assim crie um arquivo de docker apenas como modelo. Não será utilizado.