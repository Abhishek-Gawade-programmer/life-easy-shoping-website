# EaseLife E-Commerce Website
Easelife is company which sells the medical products for customers

LINK: http://gymwebsite.pythonanywhere.com/

## Getting started
###  - Requirements
 - Python 3.6+
 - pip
 - virtualenv 
 - Redis server(broker)

### - Installation
```python
# Clone the repository
git clone https://github.com/OmGDahale/business-website.git

# Enter into the directory
cd business-website/

# Create virtual environment 
python3 -m venv .venv

# Activate virtual environment 
source .venv/bin/activate

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
 - All user is also with daetr
 - Celery  of Task and Queue
 - Redis server as a broker
 - Google Email API for sending Emails
 ***






