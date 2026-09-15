# Bookstore - EBAC - Projeto Final / Continuous Delivery

Projeto Bookstore desenvolvido ao longo das atividades de Django REST Framework, testes, Docker, PostgreSQL, Docker Networks, Continuous Integration e Continuous Delivery.

## Objetivo desta etapa

Preparar o Bookstore para publicação no PythonAnywhere e automatizar a atualização da aplicação através de um webhook do GitHub.

O material do projeto final da EBAC utiliza o PythonAnywhere como plataforma de hospedagem e orienta que um push no repositório possa acionar a atualização do servidor por webhook.

## O que foi adicionado

- dependência `GitPython`;
- configuração de `ALLOWED_HOSTS` para o domínio do PythonAnywhere;
- configuração de produção por variáveis de ambiente;
- diretório de templates do Django;
- rota `/hello/` para visualizar a versão publicada;
- rota `/update_server/` para receber o webhook do GitHub;
- atualização do repositório no servidor através do GitPython;
- suporte opcional à assinatura `X-Hub-Signature-256` do GitHub;
- atualização do arquivo WSGI após um deploy;
- exemplo de WSGI para o PythonAnywhere;
- testes automatizados do fluxo de Continuous Delivery;
- workflow final de validação no GitHub Actions.

## Dependências

Na raiz do projeto:

```bash
poetry install
```

A dependência usada para manipular o repositório Git no servidor é:

```text
GitPython
```

## Configuração local

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

No PowerShell:

```powershell
Copy-Item .env.example .env
```

As principais variáveis da etapa final são:

```text
DJANGO_SECRET_KEY=troque-esta-chave-em-producao
DJANGO_DEBUG=0
PYTHONANYWHERE_HOST=seu_usuario.pythonanywhere.com
GITHUB_REPOSITORY=julicorlando/ExerciciosEBAC
DEPLOY_BRANCH=main
GITHUB_WEBHOOK_SECRET=defina-um-segredo-no-github
PYTHONANYWHERE_WSGI_FILE=/var/www/seu_usuario_pythonanywhere_com_wsgi.py
```

Nunca publique o valor real de `DJANGO_SECRET_KEY` ou `GITHUB_WEBHOOK_SECRET` no repositório.

## Rotas da etapa final

Página utilizada para verificar a versão publicada:

```text
/hello/
```

Webhook utilizado pelo GitHub:

```text
/update_server/
```

Health check da API:

```text
/api/health/
```

Exemplo de listagem de produtos:

```text
/api/products/
```

## Publicação no PythonAnywhere

### 1. Criar a conta

Crie uma conta no PythonAnywhere e abra um console Bash.

### 2. Clonar o projeto

```bash
git clone https://github.com/julicorlando/ExerciciosEBAC.git
cd ExerciciosEBAC/modulo13_bookstore
```

### 3. Criar o ambiente virtual

Utilize uma versão de Python compatível com o projeto e crie o ambiente virtual. Exemplo:

```bash
python3.12 -m venv ~/env
source ~/env/bin/activate
python -m pip install --upgrade pip
pip install poetry
poetry install
```

Confirme o caminho do ambiente:

```bash
pwd
```

### 4. Criar o Web App

No painel do PythonAnywhere:

1. abra **Web**;
2. escolha **Add a new web app**;
3. selecione **Manual configuration**;
4. selecione uma versão de Python compatível com o ambiente criado;
5. configure o **Source code** para o diretório `ExerciciosEBAC/modulo13_bookstore`;
6. configure o **Virtualenv** com o caminho do ambiente criado.

### 5. Configurar o WSGI

Existe um exemplo no projeto:

```text
deploy/pythonanywhere_wsgi.py.example
```

Copie a configuração correspondente para o arquivo WSGI criado pelo PythonAnywhere e substitua `SEU_USUARIO` pelo usuário correto.

O caminho do projeto deve apontar para:

```text
/home/SEU_USUARIO/ExerciciosEBAC/modulo13_bookstore
```

### 6. Variáveis de ambiente

Configure no ambiente do PythonAnywhere as variáveis descritas em `.env.example`, principalmente:

```text
DJANGO_DEBUG=0
PYTHONANYWHERE_HOST=SEU_USUARIO.pythonanywhere.com
GITHUB_REPOSITORY=julicorlando/ExerciciosEBAC
DEPLOY_BRANCH=main
PYTHONANYWHERE_WSGI_FILE=/var/www/SEU_USUARIO_pythonanywhere_com_wsgi.py
```

É recomendado definir também `GITHUB_WEBHOOK_SECRET` e utilizar o mesmo valor no cadastro do webhook no GitHub.

### 7. Testar a aplicação

Após configurar o WSGI e clicar em **Reload** no PythonAnywhere, acesse:

```text
https://SEU_USUARIO.pythonanywhere.com/hello/
```

A página deve exibir `Bookstore online` e o hash curto do commit em execução.

## Acesso Git pelo PythonAnywhere

Para permitir que o servidor faça `git pull`, configure o acesso do PythonAnywhere ao GitHub.

No terminal do PythonAnywhere:

```bash
ssh-keygen -t ed25519 -C "SEU_EMAIL_DO_GITHUB"
cat ~/.ssh/id_ed25519.pub
```

Copie somente a **chave pública** e cadastre-a no GitHub em **Settings > SSH and GPG keys > New SSH key**.

Depois configure o remote do clone para SSH, se necessário:

```bash
git remote set-url origin git@github.com:julicorlando/ExerciciosEBAC.git
git pull origin main
```

Nunca envie a chave privada `~/.ssh/id_ed25519`.

## Webhook para deploy automático

Depois que a aplicação estiver funcionando no PythonAnywhere, abra o GitHub do projeto e acesse:

```text
Settings > Webhooks > Add webhook
```

Configure o **Payload URL** como:

```text
https://SEU_USUARIO.pythonanywhere.com/update_server/
```

Configuração recomendada:

```text
Content type: application/json
Event: Just the push event
Active: marcado
```

Se utilizar `GITHUB_WEBHOOK_SECRET`, informe no campo **Secret** exatamente o mesmo valor configurado no servidor.

Quando houver um push na branch definida por `DEPLOY_BRANCH` (por padrão `main`), o endpoint:

1. valida o evento;
2. valida o repositório de origem;
3. valida a assinatura do webhook quando um segredo foi configurado;
4. executa o pull da branch de deploy;
5. toca o arquivo WSGI configurado para recarregar a aplicação;
6. retorna a página com o commit atualizado.

## Continuous Integration

O projeto mantém a esteira criada na atividade anterior e adiciona:

```text
.github/workflows/modulo21-continuous-delivery.yml
```

Ela executa:

```text
migrations check
       |
Django check
       |
testes automatizados
       |
check de configuração de produção
```

O workflow é executado nos Pull Requests relacionados ao Bookstore e também em pushes para `main` e para a branch desta atividade.

## Fluxo final CI/CD

```text
Nova alteração
      |
      v
Pull Request
      |
      v
GitHub Actions / CI
      |
      v
Merge ou push na main
      |
      v
Webhook do GitHub
      |
      v
/update_server/
      |
      v
Git pull no PythonAnywhere
      |
      v
Reload do WSGI
      |
      v
Nova versão publicada
```

## Testes

Execute localmente:

```bash
poetry run python manage.py check
poetry run python manage.py test
```

## Funcionalidades desenvolvidas ao longo do projeto

- Django REST Framework;
- serializers de Category, Product e Order;
- ViewSets e CRUD REST;
- paginação;
- Django Debug Toolbar;
- TokenAuthentication nos pedidos;
- produtos públicos;
- pedidos restritos ao usuário autenticado;
- Dockerfile;
- Docker Compose;
- PostgreSQL;
- Docker Network com driver `bridge`;
- Continuous Integration com GitHub Actions;
- Code Review automatizado;
- Continuous Delivery preparado para PythonAnywhere através de webhook.

## Importante

Os arquivos do repositório deixam a aplicação preparada para a etapa final, mas a URL pública só passa a existir depois que a conta e o Web App forem criados e configurados no PythonAnywhere. O endereço final depende do usuário cadastrado na plataforma.
