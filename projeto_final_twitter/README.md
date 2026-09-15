# Projeto Final EBAC — Twitter Clone

Projeto final em Python/Django que implementa uma rede social de microblog inspirada no Twitter/X, com interface web integrada ao Django e API REST com Django REST Framework.

## Deploy público

O deploy principal será realizado no PythonAnywhere, usando a conta `julicorlando`.

URL pública prevista após a ativação do Web App:

```text
https://julicorlando.pythonanywhere.com/
```

Health check:

```text
https://julicorlando.pythonanywhere.com/health/
```

O front-end é renderizado por Django Templates e o back-end/API REST é executado pelo mesmo projeto Django.

> A URL só deve ser considerada entregue quando o Web App estiver criado/recarregado no painel do PythonAnywhere e responder publicamente.

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

O projeto funciona com SQLite por padrão. No PythonAnywhere, o SQLite fica em:

```text
/home/julicorlando/ExerciciosEBAC/projeto_final_twitter/db.sqlite3
```

Esse arquivo é persistente no filesystem da conta e é suficiente para a entrega acadêmica. Se `POSTGRES_HOST` estiver definido, o Django utiliza PostgreSQL automaticamente.

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

A suíte cobre cadastro, autenticação, criação automática de perfil, seguidores, feed, CRUD de posts, curtidas, comentários, alteração de perfil, alteração de senha, API REST e proteção de autoria.

O GitHub Actions também executa `makemigrations --check`, `manage.py check`, todos os testes, valida o Docker Compose e constrói a imagem Docker.

## Deploy principal no PythonAnywhere — usuário `julicorlando`

### 1. Clonar o projeto

Abra uma **Bash console** no PythonAnywhere e execute:

```bash
cd ~
git clone -b projeto-final-twitter-clone https://github.com/julicorlando/ExerciciosEBAC.git
cd ~/ExerciciosEBAC/projeto_final_twitter
```

Se o repositório já existir:

```bash
cd ~/ExerciciosEBAC
git fetch origin
git checkout projeto-final-twitter-clone
git pull origin projeto-final-twitter-clone
cd projeto_final_twitter
```

### 2. Criar o virtualenv

Use Python 3.12 para combinar com o projeto:

```bash
mkvirtualenv --python=python3.12 twitterclone
pip install -r requirements.txt
```

Em novos consoles, ative com:

```bash
workon twitterclone
```

### 3. Preparar banco e arquivos estáticos

```bash
cd ~/ExerciciosEBAC/projeto_final_twitter
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check
```

Opcionalmente crie um administrador:

```bash
python manage.py createsuperuser
```

### 4. Gerar uma SECRET_KEY

Na Bash console:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copie o valor gerado. Não salve a chave no GitHub.

### 5. Criar o Web App

No painel do PythonAnywhere:

1. Abra **Web**.
2. Clique em **Add a new web app**.
3. Escolha `julicorlando.pythonanywhere.com`.
4. Selecione **Manual configuration**.
5. Escolha a mesma versão de Python usada no virtualenv, preferencialmente Python 3.12.

No campo **Virtualenv**, informe:

```text
/home/julicorlando/.virtualenvs/twitterclone
```

### 6. Configurar o WSGI

Abra o arquivo WSGI indicado na aba **Web**, apague o conteúdo e use:

```python
import os
import sys

project_path = "/home/julicorlando/ExerciciosEBAC/projeto_final_twitter"
if project_path not in sys.path:
    sys.path.insert(0, project_path)

os.environ["DJANGO_SETTINGS_MODULE"] = "twitterclone.settings"
os.environ["PYTHONANYWHERE_USERNAME"] = "julicorlando"
os.environ["DJANGO_ALLOWED_HOSTS"] = "julicorlando.pythonanywhere.com"
os.environ["CSRF_TRUSTED_ORIGINS"] = "https://julicorlando.pythonanywhere.com"
os.environ["DJANGO_DEBUG"] = "False"
os.environ["DJANGO_SECRET_KEY"] = "COLE_AQUI_A_CHAVE_GERADA_NO_PASSO_4"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 7. Configurar Static Files

Na aba **Web > Static files**, crie:

```text
URL:  /static/
Path: /home/julicorlando/ExerciciosEBAC/projeto_final_twitter/staticfiles
```

Para uploads de foto de perfil, crie também:

```text
URL:  /media/
Path: /home/julicorlando/ExerciciosEBAC/projeto_final_twitter/media
```

### 8. Recarregar e validar

Clique em **Reload** na aba Web e teste:

```text
https://julicorlando.pythonanywhere.com/
https://julicorlando.pythonanywhere.com/cadastro/
https://julicorlando.pythonanywhere.com/login/
https://julicorlando.pythonanywhere.com/health/
```

O `/health/` deve responder:

```json
{"status":"ok","project":"twitter-clone"}
```

Se houver erro, consulte na aba Web o **Error log** e use o traceback para corrigir a causa.

## Atualização futura do deploy

Depois que o Web App estiver configurado, uma atualização pode ser publicada com:

```bash
cd ~/ExerciciosEBAC
git checkout projeto-final-twitter-clone
git pull origin projeto-final-twitter-clone
workon twitterclone
cd projeto_final_twitter
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check
```

Depois clique em **Reload** no PythonAnywhere.

> Não coloque senhas, tokens ou chaves secretas no GitHub.

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
├── pythonanywhere_wsgi.py.example
├── vercel.json             # alternativa de deploy, não é o alvo principal
└── manage.py
```
