# Bookstore - EBAC - Docker Compose com PostgreSQL

Projeto desenvolvido em continuidade às atividades anteriores do Bookstore com Django REST Framework.

## Objetivo desta atividade

Adicionar Docker Compose ao projeto e configurar a aplicação Django para utilizar PostgreSQL em container separado.

## Serviços

O arquivo `docker-compose.yml` define dois serviços:

- `web`: aplicação Django construída a partir do `Dockerfile`;
- `db`: banco PostgreSQL 16.

O serviço `web` aguarda o PostgreSQL ficar saudável, executa as migrations e inicia o Django na porta `8000`.

## Banco de dados

Quando a variável `POSTGRES_HOST` está definida, o Django utiliza PostgreSQL.

Variáveis utilizadas:

```text
POSTGRES_DB=bookstore
POSTGRES_USER=bookstore
POSTGRES_PASSWORD=bookstore
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Para execução local sem Docker Compose, caso `POSTGRES_HOST` não esteja definida, o projeto continua utilizando SQLite.

## Dependência PostgreSQL

Foi adicionado ao Poetry o driver:

```text
psycopg[binary]
```

## Subir a aplicação

Entre na pasta do projeto:

```bash
cd modulo13_bookstore
```

Opcionalmente copie o arquivo de exemplo:

```bash
cp .env.example .env
```

No PowerShell:

```powershell
Copy-Item .env.example .env
```

Suba os serviços:

```bash
docker compose up --build
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:8000/
```

A API pode ser acessada, por exemplo, em:

```text
http://127.0.0.1:8000/api/products/
```

## Comandos úteis

Ver os containers:

```bash
docker compose ps
```

Executar o Django check:

```bash
docker compose exec web python manage.py check
```

Executar os testes:

```bash
docker compose exec web python manage.py test
```

Abrir o shell do PostgreSQL:

```bash
docker compose exec db psql -U bookstore -d bookstore
```

Parar os serviços:

```bash
docker compose down
```

Parar e remover também o volume do banco:

```bash
docker compose down -v
```

## Validação automatizada

O GitHub Actions desta atividade:

1. constrói as imagens;
2. sobe Django e PostgreSQL com Docker Compose;
3. aguarda a aplicação responder;
4. executa `python manage.py check`;
5. executa `python manage.py test` utilizando PostgreSQL;
6. encerra e remove os containers de teste.

## Funcionalidades anteriores preservadas

O projeto mantém as implementações das atividades anteriores:

- serializers de Category, Product e Order;
- ViewSets e rotas REST;
- paginação do Django REST Framework;
- Django Debug Toolbar;
- TokenAuthentication nos pedidos;
- produtos com acesso público;
- pedidos limitados ao usuário autenticado;
- Dockerfile do Bookstore.
