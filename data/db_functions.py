from data import db_session
from data.product import Product
from data.basket import Basket
from data.review import Review
from data.user import User
from data.buyer import Buyer
from data.seller import Seller
from data.admin import Admin
from data.emails import Emails


def new_product(seller_id, name, description, price, quantity):
    product = Product()
    product.seller_id = seller_id
    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity
    session = db_session.create_session()
    session.add(product)
    session.commit()
    return product


def new_basket(buyer_id, product_id, quantity):
    basket = Basket()
    basket.buyer_id = buyer_id
    basket.product_id = product_id
    basket.quantity = quantity
    session = db_session.create_session()
    session.add(basket)
    session.commit()
    return basket


def new_review(product_id, buyer_id, rating, text):
    review = Review()
    review.product_id = product_id
    review.buyer_id = buyer_id
    review.rating = rating
    review.text = text
    session = db_session.create_session()
    session.add(review)
    session.commit()
    return review


def new_user(type, email):
    user = User()
    user.type = type
    user.email = email
    session = db_session.create_session()
    session.add(user)
    session.commit()
    return user


def new_buyer(name, surname, email, password, gender, age):
    user = new_user("buyer", email)
    session = db_session.create_session()
    session.add(user)
    buyer = Buyer()
    buyer.id = user.id
    buyer.name = name
    buyer.surname = surname
    buyer.email = email
    buyer.set_password(password)
    buyer.gender = gender
    buyer.age = age
    session.add(buyer)
    session.commit()
    return buyer


def new_seller(name, surname, email, password, gender, age):
    user = new_user("seller", email)
    session = db_session.create_session()
    session.add(user)
    seller = Seller()
    seller.id = user.id
    seller.name = name
    seller.surname = surname
    seller.email = email
    seller.set_password(password)
    seller.gender = gender
    seller.age = age
    session.add(seller)
    session.commit()
    return seller


def new_admin(name, surname, email, password, gender, age, is_boss):
    user = new_user("admin", email)
    session = db_session.create_session()
    session.add(user)
    admin = Admin()
    admin.id = user.id
    admin.name = name
    admin.surname = surname
    admin.email = email
    admin.set_password(password)
    admin.gender = gender
    admin.age = age
    admin.is_boss = is_boss
    session.add(admin)
    session.commit()
    return admin


def new_email(email_):
    session = db_session.create_session()
    email = Emails()
    email.email = email_
    session.add(email)
    session.commit()
    return email
