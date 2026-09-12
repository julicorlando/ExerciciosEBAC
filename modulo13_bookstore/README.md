# Bookstore - EBAC - Dockerfile

Projeto desenvolvido em continuidade às atividades de serializers, ViewSets, paginação e Token Authentication do Bookstore com Django REST Framework.

## Objetivo desta atividade

Criar um `Dockerfile` para empacotar e executar o projeto Bookstore em um container Docker, conforme os conceitos estudados de imagem, container, host, `build` e `run`.

## Dockerfile

O arquivo está em:

```text
modulo13_bookstore/Dockerfile
```

A imagem utiliza:

- `python:3.12-slim` como imagem base;
- Poetry para instalar as dependências do projeto;
- `/app` como diretório de trabalho;
- porta `8000` para a aplicação Django;
- `python manage.py runserver 0.0.0.0:8000` como comando de execução.

Também foi criado um `.dockerignore` para evitar o envio de arquivos desnecessários para o contexto do build.

## Construir a imagem

A partir da pasta `modulo13_bookstore`:

```bash
docker build -t bookstore-ebac:modulo17 .
```

## Executar o container

```bash
docker run --rm -p 8000:8000 bookstore-ebac:modulo17
```

Depois acesse:

```text
http://127.0.0.1:8000/api/products/
```

## Validar o projeto dentro da imagem

```bash
docker run --rm bookstore-ebac:modulo17 python manage.py check
docker run --rm bookstore-ebac:modulo17 python manage.py test
```

## Funcionalidades preservadas das atividades anteriores

- serializers de `Category`, `Product` e `Order`;
- ViewSets e rotas REST;
- paginação com Django REST Framework;
- Django Debug Toolbar em desenvolvimento;
- `ProductViewSet` com acesso público;
- `OrderViewSet` protegido com Token Authentication;
- cada usuário visualiza somente os próprios pedidos;
- endpoint `POST /api/token/` para obtenção de token.

## CI

O GitHub Actions desta atividade executa automaticamente:

1. build da imagem Docker;
2. `python manage.py check` dentro do container;
3. `python manage.py test` dentro do container.

Isso valida que a imagem não apenas é construída, mas também consegue executar o projeto e a suíte de testes.
