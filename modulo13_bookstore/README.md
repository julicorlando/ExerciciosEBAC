# Bookstore - EBAC - Serializers

Projeto desenvolvido para a atividade de criação e testes de serializers com Django REST Framework.

## Objetivo

Implementar serializers para as entidades `Product`, `Category` e `Order`, representar `Category` dentro de `Product` e validar o comportamento por meio de testes automatizados.

## Entidades

### Category

Campos principais:

- `id`;
- `name`;
- `description`.

### Product

Campos principais:

- `id`;
- `name`;
- `description`;
- `price`;
- `stock`;
- relacionamento muitos-para-muitos com `Category`.

Na leitura, `ProductSerializer` retorna as categorias de forma aninhada no campo `categories`. Na escrita, o campo `category_ids` permite informar as categorias por seus IDs.

### Order

Campos principais:

- `id`;
- `customer_name`;
- `customer_email`;
- `status`;
- relacionamento muitos-para-muitos com `Product`;
- `created_at`.

Na leitura, `OrderSerializer` retorna os produtos relacionados. Na escrita, `product_ids` recebe os IDs dos produtos.

## Serializers

Os serializers estão em:

```text
store/serializers.py
```

Foram implementados:

- `CategorySerializer`;
- `ProductSerializer`;
- `OrderSerializer`.

## Testes automatizados

Os testes estão em:

```text
store/tests/test_serializers.py
```

Eles verificam:

- aceitação de dados válidos;
- validação de campos obrigatórios;
- rejeição de preço negativo;
- rejeição de e-mail inválido;
- campos retornados pelos serializers;
- representação de `Category` dentro de `Product`;
- representação de produtos dentro de `Order`;
- criação de objetos e persistência dos relacionamentos.

## Instalação

```bash
cd modulo13_bookstore
poetry install
```

## Banco e migrations

```bash
poetry run python manage.py migrate
```

## Executar os testes

Conforme solicitado na atividade:

```bash
poetry run python manage.py test
```

Também é possível validar se há migrations pendentes:

```bash
poetry run python manage.py makemigrations --check --dry-run
```

## Executar o projeto

```bash
poetry run python manage.py runserver
```
