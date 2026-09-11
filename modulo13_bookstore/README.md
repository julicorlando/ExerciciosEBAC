# Bookstore - EBAC Módulo 13

Projeto criado do zero para o exercício do módulo 13 do curso Backend Python da EBAC.

## Objetivo

Iniciar o projeto Bookstore com Django, configurar o ambiente com Poetry e adicionar o Django REST Framework.

## Tecnologias

- Python 3.12+
- Django
- Django REST Framework
- Poetry
- Pytest / pytest-django

## Instalação

```bash
cd modulo13_bookstore
poetry install
```

Caso queira reproduzir a criação da dependência principal do exercício:

```bash
poetry add django
poetry add djangorestframework
```

## Validação

```bash
poetry run python manage.py check
poetry run pytest
```

## Execução

```bash
poetry run python manage.py migrate
poetry run python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/api/health/
```

Resposta esperada:

```json
{
  "status": "ok",
  "project": "bookstore"
}
```

## Integração com DRF

O pacote `djangorestframework` está declarado no `pyproject.toml` e `rest_framework` está registrado em `INSTALLED_APPS`. O endpoint `/api/health/` utiliza `APIView` e `Response` do Django REST Framework para comprovar a integração.
