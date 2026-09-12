# Bookstore - EBAC - Paginação com Django REST Framework

Projeto desenvolvido em continuidade às atividades de serializers e ViewSets do Bookstore.

## Objetivo

Adicionar paginação às APIs do Django REST Framework e configurar o Django Debug Toolbar para auxiliar na análise de desempenho e quantidade de consultas executadas durante o desenvolvimento.

## Paginação

A paginação está centralizada em:

```text
store/pagination.py
```

Foi criada a classe `BookstorePagination`, baseada em `PageNumberPagination`, com:

- 5 registros por página por padrão;
- parâmetro `page` para navegar entre páginas;
- parâmetro `page_size` para alterar a quantidade de registros;
- limite máximo de 10 registros por página.

Exemplos:

```text
/api/products/?page=2
/api/products/?page_size=10
/api/categories/?page=2&page_size=5
```

As respostas de listagem seguem o padrão do DRF:

```json
{
  "count": 12,
  "next": "http://127.0.0.1:8000/api/categories/?page=2",
  "previous": null,
  "results": []
}
```

## Django Debug Toolbar

O projeto inclui `django-debug-toolbar` para uso em ambiente de desenvolvimento.

Com `DEBUG=True`, a toolbar é disponibilizada em:

```text
/__debug__/
```

Ela permite acompanhar informações de profiling, tempo de resposta e consultas SQL executadas durante as requisições.

## Endpoints

```text
/api/categories/
/api/categories/<id>/
/api/products/
/api/products/<id>/
/api/orders/
/api/orders/<id>/
```

## Testes

Além dos testes de serializers e CRUD dos ViewSets, foram adicionados testes específicos para validar:

- estrutura paginada com `count`, `next`, `previous` e `results`;
- tamanho padrão de 5 registros;
- navegação para a segunda página;
- customização com `page_size=10`;
- limite máximo de 10 registros por página.

Execute:

```bash
cd modulo13_bookstore
poetry install
poetry run python manage.py test
```

## Executar o projeto

```bash
poetry run python manage.py migrate
poetry run python manage.py runserver
```

Depois acesse, por exemplo:

```text
http://127.0.0.1:8000/api/products/
```
