# DJANGO MINI PROJECT - MICHAL WILKOSZ

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
* Post Images `http://localhost:9010/home/api-create-image/`

## RUNNING DOCKER COMPOSE 
* Not implemented yet

## DEPLOYMENT WITH DOCKER
* Not implemented

## EXTRAS
