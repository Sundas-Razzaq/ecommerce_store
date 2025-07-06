# E-commerce Store

A fully functional multi-vendor e-commerce web application built using Django. This project includes buyer and seller panels, product management, cart and wishlist systems, checkout flow, profile modules, and more — all with a clean frontend and modular backend.

## Project Structure

ecommerce_store/
├── cart/               # Cart functionalities  
├── checkout/           # Checkout and order processing  
├── core/               # Home, search, and shared includes  
├── ecommerce_store/    # Project settings and URLs  
├── media/              # Uploaded product, profile, and shop images  
│   ├── product_images/  
│   ├── profiles/  
│   └── shops/logos/  
├── products/           # Product models, views, templates  
├── profiles/           # Buyer and seller profile modules  
├── seller/             # Seller-specific views and dashboard  
├── static/             # Static files (CSS, JS, images)  
│   ├── css/  
│   ├── js/  
│   └── img/  
├── templates/          # Account (authentication) templates  
│   └── account/  
└── manage.py  

### Backend
- Python 3.x
- Django 4.x
- Django ORM

### Frontend
- HTML5, CSS3, JavaScript, Bootstrap 5
- jQuery, FontAwesome, Alertify.js

### Database
- MySQL (configured via MySQL Workbench)

## Features

- User Registration and Authentication (via django-allauth)
- Buyer and Seller Profile Setup
- Product Listing with Filtering and Search
- Cart and Wishlist Management
- Checkout and Payment Handling
- Seller Dashboard with prodcut creation and order management
- Order Tracking per Seller
- Fully Responsive UI

## Installation Guide

Note: Python and MySQL must be pre-installed.

1. Clone the repository
git clone https://github.com/Sundas-Razzaq/ecommerce_store.git  
cd ecommerce_store

2. Create a virtual environment
python -m venv venv  
On Windows:  
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt
If requirements.txt is missing, you can generate it using:

pip freeze > requirements.txt

4. Configure MySQL Database
Create a MySQL database using MySQL Workbench and update your ecommerce_store/settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

5. Apply Migrations
python manage.py makemigrations  
python manage.py migrate

6. Create Superuser (Optional)
python manage.py createsuperuser

7. Run the server
python manage.py runserver

Now open your browser and go to:  
http://localhost:8000

## Requirements
requirements.txt:

Django>=4.2  
mysqlclient  
django-allauth  
Pillow  
django-crispy-forms  
crispy-bootstrap5

## Developer

Sundas Razzaq  
GitHub: https://github.com/Sundas-Razzaq

This project is licensed under the MIT License. Feel free to use and modify it for educational or commercial purposes.