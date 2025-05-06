# 🛒 QuickCart - E-commerce Website

QuickCart is a full-featured e-commerce web application built with Django. It supports product listings, user accounts, shopping cart, order management, and more.
--------------------------

## 📸 Project Preview
![Home Page](https://your-image-url.com/homepage.png)
![Product Page](https://your-image-url.com/productpage.png)
![Cart Page](https://your-image-url.com/cartpage.png)

## 1. Install required softwares
> 🐍 Python version
- 3.12.3

> 📂 PostgreSQL version
- psql (PostgreSQL) 16.6 (Ubuntu 16.6-0ubuntu0.24.04.1)
  
## 2. Clone the Repository
```bash
=> git clone https://github.com/your-username/QuickCart.git
=> cd QuickCart
```
## 3.⚙️ Setup Instructions

- create a virtual environment :
```bash
=> python -m venv venv
```
## 4. Activate scripts :
```bash
=> venv/scripts/activate
```
## 5. Install Requirements :
```bash
=> pip install -r requirements.txt
```
## 6. Make migrations:

=> python manage.py makemigrations QuickCart

    => python manage.py migrate

    (if having some error of psycopg2 then )

        =>pip install psycopg2 binary

    # redo :  

    => python manage.py makemigrations QuickCart

        => python manage.py migrate

## 7. open runserver:

=> python manage.py runserver
