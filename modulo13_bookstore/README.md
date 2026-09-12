# Bookstore - EBAC - Continuous Integration e Code Review

Projeto desenvolvido em continuidade às atividades anteriores do Bookstore com Django REST Framework, Docker e PostgreSQL.

## Objetivo desta atividade

Configurar uma esteira de Continuous Integration utilizando GitHub Actions para validar automaticamente as alterações enviadas ao projeto por meio de Pull Requests.

A pipeline foi organizada para validar qualidade de código, integridade do Django, testes automatizados e build Docker antes da aprovação das alterações.

## GitHub Actions

O workflow desta atividade está em:

```text
.github/workflows/modulo20-ci-code-review.yml
```

A automação é executada em Pull Requests que alterem o projeto Bookstore e também em pushes na branch da atividade.

## Code Review automatizado

A primeira etapa da pipeline é o job:

```text
Code Review automatizado
```

Ele executa:

- instalação das dependências com Poetry;
- análise estática do código com Ruff;
- verificação de migrations pendentes;
- `python manage.py check`.

O Ruff utiliza o formato de saída do GitHub para que problemas encontrados apareçam como anotações no próprio workflow/Pull Request.

## Testes automatizados

Somente após o Code Review automatizado ser aprovado, o workflow executa:

```bash
python manage.py test
```

Isso ajuda a impedir que alterações que quebrem comportamentos existentes avancem na esteira.

## Build Docker

Após os testes, a pipeline também valida a infraestrutura utilizada nas atividades anteriores:

```bash
docker compose -f modulo13_bookstore/docker-compose.yml config
docker build -t bookstore-ebac:ci ./modulo13_bookstore
docker run --rm bookstore-ebac:ci python manage.py check
```

Assim, além do código Python, o processo confirma que a aplicação continua podendo ser construída e executada como imagem Docker.

## Fluxo da esteira

```text
Pull Request / Push
        |
        v
Code Review automatizado
        |
        v
Testes automatizados
        |
        v
Build e validação Docker
```

Se qualquer uma das etapas falhar, as etapas dependentes não avançam.

## Checklist de Pull Request

Também foi criado:

```text
.github/pull_request_template.md
```

O template inclui verificações de qualidade, testes, migrations, Docker, segurança de credenciais e retrocompatibilidade para apoiar o processo de revisão por pares.

## Executar as verificações localmente

Entre na pasta do projeto:

```bash
cd modulo13_bookstore
```

Instale as dependências:

```bash
poetry install
```

Execute o Django check:

```bash
poetry run python manage.py check
```

Execute os testes:

```bash
poetry run python manage.py test
```

Para uma análise equivalente ao Code Review automatizado:

```bash
pip install ruff
ruff check bookstore store
```

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
- PostgreSQL em container separado;
- rede Docker explícita com driver `bridge`.
