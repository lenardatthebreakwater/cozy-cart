# Cozy Cart

A simple ecommerce application that uses Flask, Sqlite and Paymongo Checkout API for the backend and HTML and Bulma for the frontend.

![cozy_cart_preview](https://github.com/lenardatthebreakwater/cozy-cart/assets/142602437/0e10b67a-bfe9-48ee-814f-76efdd14400b)


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
This will create a sqlite database, a .env file and a shop/static/product_images directory. Inside the .env file edit the value of SECRET_KEY with a value of your own. As for the PAYMONGO_SECRET, replace it's value with the secret key that can be found in the developer tab of your Paymongo account.

## Usage

To run this application, execute:

```bash
python run.py
```
You should be able to access this application at `http://127.0.0.1:8080`. Internet connection is needed in order to load Bulma and to send requests to the Paymongo Checkout API.

## Admin Dashboard

To create an Admin Acount go to `http://127.0.0.1:8080/admin/register`.

![cozy_cart_admin_register](https://github.com/lenardatthebreakwater/cozy-cart/assets/142602437/f2ed7a1f-2811-4ba6-972e-1e68260650b9)

Once created you can now go to `http://127.0.0.1:8080/admin/login` in order to login.

![cozy_cart_admin_login](https://github.com/lenardatthebreakwater/cozy-cart/assets/142602437/a70196b9-6ab4-41dc-a56a-5a4a4f4c8177)

Once logged in you will be redirected to `http://127.0.0.1:8080/admin/dashboard`.

![cozy_cart_admin_dashboard](https://github.com/lenardatthebreakwater/cozy-cart/assets/142602437/30d208db-38bc-402d-a1f1-04d85aed50f7)
