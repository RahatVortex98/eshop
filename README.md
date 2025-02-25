Django eCommerce Project

This is a fully functional eCommerce web application built with Django and PostgreSQL. The project features product management, order processing, payment integration with SSLCommerz, and a dynamic admin panel.

🚀 Features

User Authentication (Register, Login, Logout)

Product Management (CRUD operations)

Shopping Cart

Order Processing

SSLCommerz Payment Integration

PostgreSQL Database Support

Django Admin Panel for managing users, products, and orders

🛠️ Technologies Used

Backend: Django, Django REST Framework (DRF)

Database: PostgreSQL

Frontend: HTML, CSS, JavaScript (template-based)

Authentication: Django's built-in authentication

Payment Gateway: SSLCommerz

Docker Support: Optional for deployment

📦 Installation Guide

1️⃣ Clone the Repository

$ git clone https://github.com/your-username/eshop.git
$ cd eshop

2️⃣ Set Up Virtual Environment

$ python -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate

3️⃣ Install Dependencies

$ pip install -r requirements.txt

4️⃣ Set Up PostgreSQL Database

Install PostgreSQL (Download Here)

Create a database:

$ psql -U postgres
CREATE DATABASE eshop;

Update the .env file with your database credentials:

DB_NAME=eshop
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

5️⃣ Apply Migrations

$ python manage.py migrate

6️⃣ Create Superuser (Admin Panel Access)

$ python manage.py createsuperuser

7️⃣ Run the Development Server

$ python manage.py runserver

Visit: http://127.0.0.1:8000/

🔗 API Endpoints

Authentication

POST /api/auth/register/ – Register a new user

POST /api/auth/login/ – Login user

POST /api/auth/logout/ – Logout user

Products

GET /api/products/ – List all products

GET /api/products/<id>/ – Retrieve a specific product

Orders

POST /api/orders/ – Create an order

GET /api/orders/ – Get all orders (Admin Only)

GET /api/orders/<id>/ – Get a specific order

PUT /api/orders/<id>/ – Update an order

DELETE /api/orders/<id>/ – Delete an order

📜 Environment Variables

Create a .env file in the root directory and add:

SECRET_KEY=your_secret_key
DEBUG=True

# PostgreSQL Database
DB_NAME=eshop
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# SSLCommerz Payment Gateway
SSLCOMMERZ_STORE_ID=your_store_id
SSLCOMMERZ_STORE_PASS=your_store_password
SSLCOMMERZ_IS_SANDBOX=True

🛒 Payment Integration (SSLCommerz)

We have integrated SSLCommerz for online payments.

Steps to Enable Payments:

Get STORE_ID and STORE_PASS from SSLCommerz

Add credentials in the .env file.

Test using the provided sandbox environment before going live.

🐳 Docker Setup (Optional)

If you want to containerize the project using Docker, follow these steps:

Build and run the container:

$ docker-compose up --build

Open your browser and visit http://127.0.0.1:8000/
