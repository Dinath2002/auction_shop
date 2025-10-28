# 🛒 Online Auction & E-Commerce Shopping System

A full-stack web application built with **Django**, **MySQL**, **HTML**, and **CSS**.  
Users can browse products, bid on auctions, manage their carts, and place orders.  
Admins can control users, products, and auction listings through the Django Admin interface.

## 🚀 Features
- User registration and authentication  
- Product catalog with search and categories  
- Real-time auction bidding  
- Shopping cart and checkout system  
- Admin management for listings and users  

## 🧰 Tech Stack
- **Backend:** Django (Python)  
- **Database:** MySQL  
- **Frontend:** HTML, CSS, Bootstrap  
- **Tools:** PyCharm, Git, Fedora Linux  

## ⚙️ Setup
```bash
git clone https://github.com/Dinath2002/auction_shop.git
cd auction_shop
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
