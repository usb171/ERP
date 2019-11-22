# Sistema Integrado de Gestão Empresarial ERP #
O ERP é um website desenvolvido em aplicações, sua base é pensada em futuras agragações de serviços.

## Tecnologias ##

**Back-End**

* Python 3.6.7
* Django Framework
* Gunicorn
* MySQL

**Front-End**

* AdminLTE https://adminlte.io/

**Admin Django**

 ```
 pip install https://github.com/darklow/django-suit/tarball/v2
 ```
 


##Ambiente de desenvolvimento

**Dependências do Sistema**

``sudo apt python3-pip python3-dev libpq-dev postgresql postgresql-contrib
`` 

**Banco**

```
sudo -u postgres psql
CREATE DATABASE erp_dev;
CREATE USER nome_maquina WITH PASSWORD 'senha';
ALTER ROLE nome_maquina SET client_encoding TO 'utf8';
ALTER ROLE nome_maquina SET default_transaction_isolation TO 'read committed';
ALTER ROLE nome_maquina SET timezone TO 'America/Fortaleza';
GRANT ALL PRIVILEGES ON DATABASE erp_dev TO nome_maquina;
ALTER USER nome_maquina WITH SUPERUSER;
```

**Criar Ambiente Virtual**

``virtualenv --python=python3 env``

**Ativar Ambiente Virtual**

``source env/bin/activate``

**Dependências do Projeto**
```
(env) pip install --upgrade pip
(env) pip install django
(env) pip install psycopg2
(env) pip install python-decouple
(env) pip install https://github.com/darklow/django-suit/tarball/v2
```

**Criar Arquivo de Ambiente do Projeto**

`` nano ERP/.env ``

Copiar variáveis para o arquivo .env

* Mudar key, nome_maquina e senha

```
DEBUG=True
SECRET_KEY='key'
ENGINE='django.db.backends.postgresql_psycopg2'
NAME='erp_dev'
USER='nome_maquina'
PASSWORD='senha'
HOST='localhost'
PORT=''
```

##Ambiente de Produção

**Gunicorn**

* Criar arquivo de configuração e copiar os seguintes parametros

``nano /etc/supervisor/conf.d/erp.conf``

```
[program:erp]
command=/home/SERVER_CRM/env/bin/gunicorn --access-logfile - --workers 3 --bind localhost:8001 ERP.wsgi:application
directory=/home/SERVER_CRM/ERP
user=crm
group=www-data
autostart=true
autorestart=true
killasgroup=true
stdout_logfile=/home/SERVER_CRM/ERP/supervisor.log
redirect_stderr=True
environment=DJANGO_SETTINGS_MODULE="ERP.settings", LANG="en_US.utf8", LC_ALL="en_US.UTF-8", LC_LANG="en_US.UTF-8"
```

