# DJANGO MINI PROJECT - Image Uploads

## INTRODUCTION 
This project has exposes 3 major APIs

* Upload an image with a name
* List all images under a a user 
* Image detail - links of the various thumbnail heights for the image.

All other functionality is handled in the django admin UI. 


## DESCRIPTION 
The project at a higher level, allows uses to upload images through the Django Rest Framework UI, list images under the user including links to the various images listed under the user. 
User management is handled in the admin UI. A user is created, and assigned a particular account tier or Plan. Under the plan associated with the user are various image types the user can access. 

## RUNNING LOCALLY 
* Clone the project 
* Create a virtualenv environment locally 
* From the root directory of the project install the requirements by running `pip install -r requirements.txt`
* Run the migrations `python manage.py makemigrations` 
* Run Migrate `python manage.py migrate` 
* Run the webserver locally `python manage.py runserver`. This defaults to port 8080. If port 8080 is in use by another application or you wish to run on a different port, run the following `python manage.py runserver 0.0.0.0:9010` to run on port 9010 or any other you choose
* Visit the admin page on `http://localhost:9010/admin`
* List images `http://localhost:9010/home/api-list-images`
* Post Images `http://localhost:9010/home/api-upload-image/`
* List Thumbnails `http://localhost:9010/home/api-api-list-image-thumbnail/`
* Generate Temp Link `http://localhost:9010/home/api-generate-temp-link/`

## RUNNING DOCKER COMPOSE 
* To run with docker compose, clone the project to a local environment 
* Create a `.env` file in the root directory of the project with the following 
    - SECRET_KEY=
    - DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    - SQL_ENGINE=django.db.backends.postgresql
    - SQL_DATABASE=postgres
    - SQL_USER=postgres
    - SQL_PASSWORD=postgres
    - SQL_HOST=db
    - SQL_PORT=5432 

* Also have a `config.ini` file in the same location as the settings.py with the following
    ```
    [MAIN_SETTINGS]
    secret_key=xxxxxxxxxxxxxxxxx

    [AWS_CREDENTIALS]
    AWS_ACCESS_KEY_ID=xxxxxxxxxxxxxxxx
    AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxx
    AWS_STORAGE_BUCKET_NAME=xxxxxxxxxxxxxx
    AWS_DEFAULT_ACL = None
    ```
* Build and start with the following command `docker-compose up -d --build` 
* Once the container(s) is/are up, run the following to create a super user to use for the admin `docker-compose exec web python manage.py createsuperuser`. The command will prompt you with the details of the user. 
* Visit the admin site on `http://localhost:9010/admin` and the APIs on `http://localhost:9010/home/api-list-images`, `http://localhost:9010/home/api-upload-image/`, `http://localhost:9010/home/api-api-list-image-thumbnail/` and `http://localhost:9010/home/api-generate-temp-link/`
* To run the `Generate Temp Link` API, the body should contain the following, 
```
{
    "image_id": 2,
    "alive_duration": 300
}
```
 - The `image_id` is the ID in the response of `List Images` API. 
 - The `alive_duration` specifies the time in seconds, after which the link expires. 

## DEPLOYMENT WITH DOCKER
* Not implemented

## RECOMMENDATION
Since this is a mini project, I implemented a function in the models that creates the thumbnails. A more scalable approach will be to use django-celery tasks. 
