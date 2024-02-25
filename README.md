# Cozy Cart

A simple ecommerce application that uses Flask, Waitress, Sqlite and Paymongo Checkout API for the backend and HTML, Bulma, and JS for the frontend.


## Requirements
* Python (any version close to 3.11.4)
* Paymongo Account

## Installation

* Clone this repo 

```bash
git clone https://github.com/lenardatthebreakwater/cozy-cart.git
```

* Change Directory

```bash
cd cozy-cart
```

* Run Pip Install

```bash
pip install -r requirements.txt
```

* Configuration

```bash
python setup.py
```
This will create a sqlite database, a .env file and a shop/static/product_images directory.\
\
Inside the .env file edit the value of SECRET_KEY with a value of your own. As for the PAYMONGO_SECRET, replace it's value with the secret key that can be found in the developer tab of your Paymongo account.

## Usage

To run this application, execute:

```bash
python run.py
```

You should be able to access this application at `http://127.0.0.1:8080`\
\
Internet connection is needed in order to load Bulma and to send requests to the Paymongo Checkout API.

* Admin Dashboard

To create an Admin Acount go to `http://127.0.0.1:8080/admin/register`.\

Once created you can now go to `http://127.0.0.1:8080/admin/login` in order to login.\

Once logged in you will be redirected to `http://127.0.0.1:8080/admin/dashboard` \
