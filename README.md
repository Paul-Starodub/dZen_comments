# dZen_comments
Do you like to express your opinion? Then this application is for you! No pre-registration is required - just remember the unique combination of your username and email (the application will use it to determine that it is you).You can either create new comments or reply to any comment. You can also use the following allowed HTML tags in messages: `<a href=”” title=””> </a> <code> </code> <i> </i> <strong> </strong>`

### Features
- Admin panel /admin/

## Installing using GitHub
```
git clone https://github.com/Paul-Starodub/dZen_comments
cd dZEN_comments
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## .env file
Open file .env.sample and change environment variables to yours. Also rename file extension to .env
***
## Run on local server
- Install PostgreSQL, create DB and superuser from terminal
- Connect DB
- Run:
```
python manage.py migrate
python manage.py runserver
```
- You can download test fixture:
```
python manage.py dumpdata --indent 4 > comments_data.json
```
***
## Run with Docker
Docker should be already installed
```
docker-compose up --build
```
***
### Create superuser(optional):
- docker exec -it comments bash 
- python manage.py createsuperuser
### Getting access
You can use following:
- superuser:
  - username: admin
  - Email: admin@gmail.com
  - Password: vovk7777(necessary only for admin page)
- user:
  - Email: red@gmail.com
  - username: red

### Testing with docker
- docker exec -it comments bash 
- python manage.py test
***
## Stop server
```
docker-compose down
```
