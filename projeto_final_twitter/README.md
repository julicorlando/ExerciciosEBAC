# Projeto Final EBAC — Twitter Clone

Projeto final em Python/Django que implementa uma rede social de microblog inspirada no Twitter/X, com interface web integrada ao Django e API REST com Django REST Framework.

## Requisitos atendidos

### Autenticação e criação de conta

- cadastro de novos usuários;
- login e logout usando o sistema de autenticação do Django;
- senhas armazenadas com hash pelo Django;
- endpoint REST para cadastro;
- autenticação da API por TokenAuthentication e SessionAuthentication.

### Perfil

O usuário pode alterar de forma independente:

- nome;
- sobrenome;
- e-mail;
- biografia;
- foto de perfil;
- senha.

Nenhum desses campos precisa ser alterado obrigatoriamente.

### Seguir usuários e feed

- seguir e deixar de seguir outros usuários;
- impedir que o usuário siga a si mesmo;
- visualizar lista de seguidores;
- visualizar lista de pessoas seguidas;
- feed ordenado do mais recente para o mais antigo;
- o feed exibe somente posts de pessoas que o usuário segue.

### Posts e interações

- criação de posts de até 280 caracteres;
- leitura de posts;
- edição dos próprios posts;
- exclusão dos próprios posts;
- curtidas com alternância curtir/descurtir;
- uma curtida por usuário em cada post;
- comentários de até 280 caracteres;
- contagem de curtidas e comentários.

### API REST

Principais rotas:

```text
POST   /api/register/
POST   /api/token/
GET    /api/users/
GET    /api/profiles/
PATCH  /api/profiles/<id>/
GET    /api/posts/
POST   /api/posts/
GET    /api/posts/<id>/
PATCH  /api/posts/<id>/
DELETE /api/posts/<id>/
GET    /api/posts/feed/
POST   /api/posts/<id>/like/
POST   /api/posts/<id>/comment/
GET    /api/follows/
POST   /api/follows/
DELETE /api/follows/<id>/
GET    /api/users/<username>/followers/
GET    /api/users/<username>/following/
```

Para obter um token:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -d "username=seu_usuario&password=sua_senha"
```

Depois envie:

```text
Authorization: Token SEU_TOKEN
```

## Banco de dados

O projeto funciona com SQLite por padrão para facilitar a execução local. Quando `POSTGRES_HOST` estiver definido, o Django utiliza PostgreSQL automaticamente.

## Rodar localmente

```bash
cd projeto_final_twitter
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

## Docker + PostgreSQL

Com Docker instalado:

```bash
docker compose up --build
```

A aplicação ficará disponível em:

```text
http://localhost:8000/
```

Para criar um superusuário no container:

```bash
docker compose exec web python manage.py createsuperuser
```

## Testes automatizados

```bash
python manage.py test
```

A suíte cobre:

- criação automática de perfil;
- feed somente com usuários seguidos;
- seguir e deixar de seguir;
- bloqueio de auto-follow;
- CRUD de posts;
- curtidas;
- comentários;
- alteração de perfil;
- alteração de senha;
- cadastro REST;
- feed REST;
- proteção de autoria nos posts;
- interações via API.

O GitHub Actions também executa `makemigrations --check`, `manage.py check`, todos os testes, valida o Docker Compose e constrói a imagem Docker.

## Deploy no PythonAnywhere

O projeto está preparado para deploy usando WSGI.

1. Clone o repositório no PythonAnywhere.
2. Entre na pasta:

```bash
cd ExerciciosEBAC/projeto_final_twitter
```

3. Crie e ative o virtualenv e instale as dependências.
4. Execute:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

5. Configure o Web App como `Manual configuration` e use o arquivo `pythonanywhere_wsgi.py.example` como referência.
6. Configure as variáveis:

```text
DJANGO_SECRET_KEY=<chave forte>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=SEU_USUARIO.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://SEU_USUARIO.pythonanywhere.com
```

7. Configure os diretórios de arquivos estáticos e mídia no painel do PythonAnywhere.
8. Recarregue o Web App.

O link final deverá seguir o formato:

```text
https://SEU_USUARIO.pythonanywhere.com
```

> A URL pública depende da conta do aluno no serviço de hospedagem. Não coloque senhas, tokens ou chaves secretas no GitHub.

## Estrutura

```text
projeto_final_twitter/
├── social/                 # domínio social, API, modelos e testes
├── twitterclone/           # settings e URLs principais
├── templates/              # front-end Django
├── static/css/             # interface responsiva
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
```
