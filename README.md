# Social Networking App

Before running the app assuming that **python 3.8.xx** is installed on development machine

1. Create virtual environment with python3.8.xx
```shell
python3.8 -m venv env
```
2. Activate the virtual environment
```shell
source env/bin/activate
```
3. Install requisite packages:
```shell
sh scripts/install_requirements.sh
```

4. Run the migrations to reflect the django models to database (sqlite for test)
```shell
python manage.py migrate
```

5. Run Server Locally
```shell
python manage.py runserver
```

6. Create Superuser for Admin-panel
```shell
python manage.py createsuperuser
```

7. Run Tests
```shell
python manage.py test
```

8. API Documentation:

```shell
http://localhost:8000/swagger/  (swagger documentation)


http://localhost:8000/users/ (POST) (Add User)
http://localhost:8000/login/ (POST) (Login)
http://localhost:8000/posts/ (POST) (Create New Post)
http://localhost:8000/posts/ (GET) (Get all posts)
http://localhost:8000/users/1/ (PUT) (Update a post)
http://localhost:8000/users/1/ (DELETE) (Delete Post)
http://localhost:8000/posts_like/ (POST) (Like/Dislike post)
http://localhost:8000/posts_like/ (GET) (get Liked/Disliked posts)
http://localhost:8000/posts_like/1/ (GET) (get Liked/Disliked posts)
```