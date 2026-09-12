# Bookstore - EBAC - ViewSets e Testes

Projeto desenvolvido em continuidade às atividades do Bookstore com Django REST Framework.

## Objetivo desta atividade

Construir os ViewSets das entidades `Category`, `Product` e `Order` a partir dos serializers já existentes, publicar as rotas da API com `DefaultRouter` e validar o CRUD por meio de testes automatizados.

## ViewSets implementados

Os ViewSets estão em:

```text
store/views.py
```

Foram implementados:

- `CategoryViewSet`;
- `ProductViewSet`;
- `OrderViewSet`.

Todos utilizam `ModelViewSet`, disponibilizando as operações padrão de CRUD:

- `list`;
- `create`;
- `retrieve`;
- `update` / `partial_update`;
- `destroy`.

## Rotas

As rotas do app estão em `store/urls.py` e são incluídas pelo arquivo principal `bookstore/urls.py`.

Endpoints principais:

```text
GET/POST        /api/categories/
GET/PATCH/DELETE /api/categories/<id>/

GET/POST        /api/products/
GET/PATCH/DELETE /api/products/<id>/

GET/POST        /api/orders/
GET/PATCH/DELETE /api/orders/<id>/
```

## Serializers e relacionamentos

- `Product` retorna suas categorias no campo `categories` e recebe IDs em `category_ids` na escrita;
- `Order` retorna seus produtos no campo `products` e recebe IDs em `product_ids` na escrita.

## Testes automatizados

Os testes dos ViewSets estão em:

```text
store/tests/test_viewsets.py
```

Eles cobrem:

- listagem e criação;
- recuperação de objeto único;
- atualização parcial;
- exclusão;
- representação dos relacionamentos;
- criação de `Product` com categorias;
- criação de `Order` com produtos;
- rejeição de dados inválidos;
- validação dos códigos HTTP retornados pela API.

Os testes de serializers permanecem em:

```text
store/tests/test_serializers.py
```

## Instalação

```bash
cd modulo13_bookstore
poetry install
```

## Banco de dados

```bash
poetry run python manage.py migrate
```

## Executar os testes

Conforme solicitado nas atividades:

```bash
poetry run python manage.py test
```

## Executar a aplicação

```bash
poetry run python manage.py runserver
```

A API ficará disponível em:

```text
http://127.0.0.1:8000/api/
```
