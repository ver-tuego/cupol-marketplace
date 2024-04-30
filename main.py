import os

import flask_login
import requests
from flask import Flask, render_template, redirect, url_for, jsonify, request
from data import db_session
from data.product import Product
from data.review import Review
from data.user import User
from data.buyer import Buyer
from data.seller import Seller
from data.admin import Admin
from forms.register import RegisterForm
from forms.login import LoginForm
from flask_login import LoginManager, login_user, login_required
from data.db_functions import new_buyer, new_seller, new_admin, new_product, new_review
from difflib import SequenceMatcher

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
tokens = []


def similar(p1, p2):
    return SequenceMatcher(None, p1, p2).ratio()


def get_photos_from_id(id, mode):
    try:
        arr = os.listdir(f'static/photos/{mode}/{id}')
        arr = list(map(lambda x: f'static/photos/{mode}/{id}/{x}', arr))
        return arr
    except Exception as ex:
        print(ex)
        return []


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main_page():
    current_user = flask_login.current_user
    params = {
        'css_style': url_for('static', filename='css/main_page.css')
    }
    return render_template('main_page.html', **params)


@login_required
@app.route('/add_review/<product_id>')
def add_review(product_id):
    current_user = flask_login.current_user
    user_id = current_user.id
    db_sess = db_session.create_session()
    buyers_ids = db_sess.query(Buyer).all()
    buyers_ids = [buyer.id for buyer in buyers_ids]
    params = {
        'is_not_buyer': user_id not in buyers_ids,
        'css_style': url_for('static', filename='css/main_page.css')
    }
    return render_template('add_review.html', **params)


@login_required
@app.route('/submit-review', methods=['POST'])
def submit_review():
    current_user = flask_login.current_user
    user_id = current_user.id
    db_sess = db_session.create_session()
    buyers_ids = db_sess.query(Buyer).all()
    buyers_ids = [buyer.id for buyer in buyers_ids]
    rating = request.form['rating']
    review_text = request.form['review']
    photos = request.files.getlist('photos')
    product_id = request.form['product_id']
    if user_id not in buyers_ids:
        params = {
            'is_not_buyer': user_id not in buyers_ids,
            'css_style': url_for('static', filename='css/main_page.css')
        }
        return render_template('add_review.html', **params)

    new_review(product_id, current_user.id, int(rating), review_text)
    db_sess = db_session.create_session()
    latest_review = db_sess.query(Review).order_by(Review.id.desc()).first().id
    if not os.path.exists(f'static/photos/reviews/{latest_review}'):
        os.makedirs(f'static/photos/reviews/{latest_review}')
    if any(photos):
        for photo in range(len(photos)):
            photos[photo].save(os.path.join(f'static/photos/reviews/{latest_review}', f'{photo}.png'))
    return redirect('/')


@login_required
@app.route('/add_product')
def add_product():
    current_user = flask_login.current_user
    seller_id = current_user.id
    db_sess = db_session.create_session()
    sellers_ids = db_sess.query(Seller).all()
    sellers_ids = [seller.id for seller in sellers_ids]
    params = {
        'is_not_buyer': seller_id not in sellers_ids,
        'css_style': url_for('static', filename='css/main_page.css')
    }
    return render_template('add_product.html', **params)


@login_required
@app.route('/submit-product', methods=['POST'])
def submit_product():
    current_user = flask_login.current_user
    photos = request.files.getlist('product_images')
    seller_id = current_user.id
    name = request.form['product_name']
    description = request.form['product_description']
    price = request.form['product_price']
    quanity = request.form['product_quanity']

    db_sess = db_session.create_session()
    sellers_ids = db_sess.query(Seller).all()
    sellers_ids = [seller.id for seller in sellers_ids]
    if seller_id in sellers_ids:
        new_product(seller_id, name, description, price, quanity)
        latest_product = db_sess.query(Product).order_by(Product.id.desc()).first().id
        print(latest_product)
        if not os.path.exists(f'static/photos/products/{latest_product}'):
            os.makedirs(f'static/photos/products/{latest_product}')
        if any(photos):
            for photo in range(len(photos)):
                photos[photo].save(os.path.join(f'static/photos/products/{latest_product}', f'{photo}.png'))
        return redirect('/')
    params = {
        'is_not_buyer': True,
        'css_style': url_for('static', filename='css/main_page.css')
    }
    return render_template('add_product.html', **params)


@app.route('/load-more', methods=['GET'])
def load_more():
    db_sess = db_session.create_session()
    products = db_sess.query(Product).all()
    start = int(request.args.get('start'))
    limit = int(request.args.get('limit'))
    new_products = products[start:start + limit]
    data = []
    for i in new_products:
        data.append({'id': i.id, 'name': i.name, 'image': get_photos_from_id(i.id, 'products')[0], 'price': i.price,
                     'rating': i.rating})
    return jsonify(data)


@app.route('/cart')
def cart():
    return render_template('cart.html')


# Маршрут для загрузки дополнительных карточек товаров при поиске
@app.route('/load-more-search', methods=['GET'])
def load_more_search():
    query = str(request.args.get('query'))
    start = int(request.args.get('start'))
    limit = int(request.args.get('limit'))
    db_sess = db_session.create_session()
    products = db_sess.query(Product).all()
    products = list(filter(lambda x: similar(x.name, query) >= 0.7, products))
    new_products = products[start:start + limit]
    data = []
    for i in new_products:
        data.append({'id': i.id, 'name': i.name, 'image': get_photos_from_id(i.id, 'products')[0], 'price': i.price,
                     'rating': i.rating})
    print(data)
    return jsonify(data)


@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/search/<query>')
def search_result(query):
    current_user = flask_login.current_user
    params = {
        'css_style': url_for('static', filename='css/main_page.css')
    }
    return render_template('search.html', **params)


@app.route('/product/<product_id>')
def product(product_id):
    current_user = flask_login.current_user
    db_sess = db_session.create_session()
    reviews = db_sess.query(Review).filter(Review.product_id == product_id).all()
    product = db_sess.query(Product).filter(Product.id == product_id).first()
    seller = db_sess.query(Seller).filter(Seller.id == product.seller_id).first()
    reviews_info = []
    for i in reviews:
        reviews_info.append({'username': db_sess.query(Buyer).filter(Buyer.id == i.buyer_id).first().name,
                             'rating': i.rating, 'text': i.text, 'photos': get_photos_from_id(i.id, 'reviews')})

    params = {
        'css_style': url_for('static', filename='css/main_page.css'),
        'reviews': reviews_info,
        'product': {'id': product_id, 'name': product.name, 'seller_name': seller.name,
                    'description': product.description,
                    'price': product.price,
                    'rating': product.rating,
                    'photos': get_photos_from_id(product_id, 'products')}
    }
    print(params)
    return render_template('product.html', **params)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Указанная почта занята")
        if not 14 < form.age.data < 200:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Недопустимый возраст")
        if form.type.data == "buyer":
            user = new_buyer(form.name.data, form.surname.data, form.email.data, form.password.data,
                             form.gender.data, form.age.data)
        else:
            user = new_seller(form.name.data, form.surname.data, form.email.data, form.password.data,
                              form.gender.data, form.age.data)
        db_sess.add(user)
        login_user(db_sess.query(User).get(user.id))
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            if db_sess.query(eval(db_sess.query(User).get(user.id).type.capitalize())).get(user.id).check_password:
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


db_session.global_init("db/db.db")

"""
new_product(5, "Сармат", "Настоящий", 999999999999.99, 1, "")

new_review(1, 5, "Реально настоящий")

new_buyer("Покупатель", "С фамилией", "buyer@mail.ru", "buyer", "male", 19)

new_seller("Продавец", "Без фамилией", "seller@mail.ru", "seller", "male", 99)

new_admin("Дмитрий", "Кривошея", "krivosheya_da@mail.ru", "03092008", "male", 15, True)
new_admin("Сармат", "Сакиев", "sarmat@mail.ru", "hard_password", "male", 16, True)
new_admin("Матвей", "Верташов", "matvey@mail.ru", "123", "male", 16, True)
"""

if __name__ == "__main__":
    app.run()
