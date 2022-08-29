# SaagaGreenFarms E-Commerce Website
Easelife is company which sells the medical products for customers

LINK : https://primemedicare.in/

VIDEO LINK Customer : https://cdn5.f-cdn.com/files/download/168249095/PrimeMediCare%20_%20Sign%20In-costomer.mp4

VIDEO LINK ADMIN:  https://cdn3.f-cdn.com/files/download/168248961/PrimeMediCare%20_%20admin.mp4
***
## Getting started
###  - Requirements
 - Python 3.6+
 - pip
 - virtualenv 
 - Redis server(broker)

### - Installation
```python
# Clone the repository
git clone https://github.com/Abhishek-Gawade-programmer/life-easy-shoping-website.git

# Enter into the directory
cd shopping_life_easy/

# Create virtual environment 
virtualenv life_easy_env

# Activate virtual environment 
 source life_easy_env/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Apply migrations.
python manage.py migrate
```
### - Configuration
Create `.env` file in cwd and add the following
```python
#Stripe Payments credential 
STRIPE_PUBLIC_KEY = ''
STRIPE_SECRET_KEY = ''
STRIPE_WEBHOOK_SECRET = ''

#Email Settings
EMAIL_BACKEND=''
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''

#celery Settings
CELERY_BROKER_URL=''
CELERY_RESULT_BACKEND=''
```
### - Starting the application
```python
# Create a superuser account (follow the prompts afterwards)
python manage.py createsuperuser
python manage.py runserver
```
### - Start redis Broker 
``` bash
cd redis
src/redis-server
#redis server will start at localhost:6863
```


### - Start Celery Task Queue
``` bash
#open new terminal with same dir that project and virtualenv activated
celery -A shopping_life_easy worker -l INFO
```
***
## What Technology Used
### - FrontEnd
 - HTML5
 - CSS
 - Javascript
 - MDBootstrap  snippets
 - Jquery 


### - Backend
 - Django Python Web Framework
 - PostgreSQL for Database
 - Celery  of Task and Queue
 - Redis server as a broker
 - Google Email API for sending Emails
 -  Google Oauth for signing with Google 

***
## Features 
### - For Customer 
 - All products are display in cards with the available and other details 
 - Ihe available and rating are also added to get more details in one look 
 - In product details view there is `Add to cart` and `Remove from cart` Buttons for quick access
 -  Description and rating to product is also added 
 - In cart view the all details are display in from of table that gives quick summary 
 - The Checkout form is also added with online payment and COD is also added - 


### - For Administer  
 - All products info and details are displayed with graphs and statistic details  
 - All costumers is also with details 
 - our monthly Sales and yearly sales with graphs
 - email and costumers details for shipment of their products
 - email notification when admin creates a new product and verify.. etc the orders
 - email to admin is user craete a new order 
 - report the order as a spam so that admin can delete annotating order
 - verification ans authentication of users by Django Allaulth
 ***






