# Bookstore - EBAC - Token Authentication

Projeto desenvolvido em continuidade às atividades de serializers, ViewSets e paginação do Bookstore com Django REST Framework.

## Objetivo

Adicionar autenticação por token ao fluxo de pedidos (`OrderViewSet`), mantendo a consulta de produtos aberta, conforme o cenário de e-commerce apresentado na atividade.

## Regras de autenticação

### Produtos

Os endpoints de produtos permanecem públicos. Não é necessário informar token para listar ou visualizar produtos.

```text
GET /api/products/
GET /api/products/<id>/
```

### Pedidos

Os endpoints de pedidos utilizam `TokenAuthentication` e exigem usuário autenticado.

```text
GET/POST /api/orders/
GET/PATCH/DELETE /api/orders/<id>/
```

Além da autenticação, cada pedido é associado ao usuário que o criou. O `OrderViewSet` filtra o queryset para que o usuário autenticado visualize apenas os próprios pedidos.

## Obter token

Foi disponibilizado o endpoint:

```text
POST /api/token/
```

Exemplo de corpo:

```json
{
  "username": "julio",
  "password": "sua-senha"
}
```

Resposta:

```json
{
  "token": "seu-token"
}
```

Nas chamadas protegidas, envie o cabeçalho:

```text
Authorization: Token seu-token
```

## Implementação

- `rest_framework.authtoken` incluído em `INSTALLED_APPS`;
- `TokenAuthentication` aplicado ao `OrderViewSet`;
- `IsAuthenticated` aplicado ao `OrderViewSet`;
- `ProductViewSet` mantido com acesso público;
- `Order` relacionado ao usuário criador;
- criação de pedido associa automaticamente `request.user`;
- queryset de pedidos limitado ao usuário autenticado;
- endpoint para obtenção de token;
- paginação das atividades anteriores preservada.

## Testes

Os testes validam:

- acesso público aos produtos;
- bloqueio de pedidos sem token;
- rejeição de token inválido;
- acesso de usuário autenticado aos próprios pedidos;
- impedimento de acesso ao pedido de outro usuário;
- associação automática do pedido ao usuário autenticado;
- geração/obtenção de token;
- CRUD já existente de Category, Product e Order.

Execute:

```bash
cd modulo13_bookstore
poetry install
poetry run python manage.py migrate
poetry run python manage.py test
```

Para iniciar o servidor:

```bash
poetry run python manage.py runserver
```
