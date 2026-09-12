# Bookstore - EBAC - Docker Network Bridge

Projeto desenvolvido em continuidade às atividades anteriores do Bookstore com Django REST Framework, Dockerfile e Docker Compose com PostgreSQL.

## Objetivo desta atividade

Deixar explícita no `docker-compose.yml` a rede utilizada pelos serviços da aplicação e do banco de dados, utilizando uma rede Docker do tipo `bridge`.

## Rede Docker

Foi criada a rede:

```text
bookstore_network
```

com o driver:

```text
bridge
```

Os serviços `web` e `db` foram associados explicitamente a essa mesma rede.

Trecho principal da configuração:

```yaml
services:
  db:
    networks:
      - bookstore_network

  web:
    networks:
      - bookstore_network

networks:
  bookstore_network:
    driver: bridge
```

Com isso, a aplicação Django se comunica com o PostgreSQL pelo nome do serviço `db`, dentro da rede privada criada pelo Docker Compose.

## Subir os serviços

Entre na pasta do projeto:

```bash
cd modulo13_bookstore
```

Suba a aplicação e o PostgreSQL:

```bash
docker compose up --build
```

A API ficará disponível em:

```text
http://127.0.0.1:8000/api/products/
```

## Verificar a rede

Liste as redes Docker:

```bash
docker network ls
```

Veja os containers do projeto:

```bash
docker compose ps
```

Também é possível inspecionar a rede criada pelo Compose:

```bash
docker network inspect modulo13_bookstore_bookstore_network
```

O nome pode variar conforme o nome da pasta/projeto do Docker Compose, mas o driver deve ser `bridge` e os containers `web` e `db` devem aparecer conectados à mesma rede.

## Testes

Execute a suíte dentro do container da aplicação:

```bash
docker compose exec web python manage.py test
```

Para encerrar os serviços:

```bash
docker compose down
```

Para remover também o volume do PostgreSQL:

```bash
docker compose down -v
```

## Validação automatizada

O GitHub Actions desta atividade valida automaticamente:

1. a sintaxe do `docker-compose.yml`;
2. a subida dos serviços `web` e `db`;
3. se os dois containers estão conectados à mesma rede;
4. se o driver da rede é `bridge`;
5. se a aplicação responde corretamente;
6. a execução dos testes do Django.

## Funcionalidades anteriores preservadas

O projeto continua com:

- serializers de Category, Product e Order;
- ViewSets e rotas REST;
- paginação do Django REST Framework;
- Django Debug Toolbar;
- TokenAuthentication nos pedidos;
- produtos com acesso público;
- pedidos restritos ao usuário autenticado;
- Dockerfile;
- Docker Compose;
- PostgreSQL em container separado.
