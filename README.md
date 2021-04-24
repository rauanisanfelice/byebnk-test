# Byebank Test

Conforme proposto no [Desafio técnico backend - Byebnk](https://gitlab.com/byebnk/desafio-backend), foi realizado o projeto com as seguintes bibliotecas:

* django
* djangorestframework
* django-filter
* drf-yasg
* markdown
* pyyaml
* python-decouple
* psycopg2-binary

![API](./static/img/API_Byebnk.png?raw=true)

## Instruções

1. Virtualenv
2. Arquivos dist
3. Docker Compose
4. Aplicação
5. Testes

### Virtualenv

```bash
sudo apt install virtualenv -y
virtualenv -p python3 env
```


### Arquivos dist

```bash
sudo cp .env.dist .env
sudo cp docker-compose.yml.dist docker-compose.yml
```

### Docker Compose

```bash
docker-compose up -d
```

### Aplicação

```bash
python manage.py runserver 0.0.0.0:8000
```

### Testes

```bash
python manage.py test --noinput
```
