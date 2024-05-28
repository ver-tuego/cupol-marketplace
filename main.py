import os

import flask_login
import requests
from sqlalchemy import and_
from flask import Flask, render_template, redirect, url_for, jsonify, request
from data import db_session
from data.product import Product
from data.review import Review
from data.user import User
from data.buyer import Buyer
from data.seller import Seller
from data.basket import Basket
from data.admin import Admin
from data.emails import Emails
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.edit import EditForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.db_functions import new_buyer, new_seller, new_admin, new_product, new_review, new_basket
from tools import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
tokens = []


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/about_us')
def about_us():
    params = {
        'css_style': url_for('static', filename='css/main_page.css')
    }
    return render_template('about_us.html', **params)


@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    print(email)
    return jsonify({'message': 'Вы успешно подписались!'}), 200


@app.route('/')
def main_page():
    params = {
        'css_style': url_for('static', filename='css/main_page.css')
    }
    return render_template('main_page.html', **params)


@app.route('/basket', methods=['GET'])
def get_basket():
    user_id = current_user.id
    basket_data = {
        "items": [],
        "total": 0
    }
    db_sess = db_session.create_session()
    products = db_sess.query(Basket).filter(Basket.buyer_id == user_id)
    for i in products:
        prd = db_sess.query(Product).filter(Product.id == i.product_id).first()
        bask_str = db_sess.query(Basket).filter(
            and_(Basket.product_id == i.product_id, Basket.buyer_id == user_id)).first()
        basket_data['items'].append({
            'image': get_photos_from_id(i.product_id, 'products')[0],
            'name': prd.name,
            'price': prd.price,
            'quantity': bask_str.quantity
        })
    basket_data['total'] = sum([int(i['price']) * int(i['quantity']) for i in basket_data['items']])
    return jsonify(basket_data)


@app.route('/payment', methods=['POST'])
def process_payment():
    user_id = current_user.id
    db_sess = db_session.create_session()
    products = db_sess.query(Basket).filter(Basket.buyer_id == user_id).all()
    for i in products:
        product = db_sess.query(Product).filter(Product.id == i.product_id).first()
        # product.selling += i.quantity
        product.quantity -= i.quantity
    for row in products:
        db_sess.delete(row)
    db_sess.commit()
    return '', 200


@app.route('/basket_add', methods=['POST'])
def basket_add():
    try:
        product_id = request.form['product']
        user_id = current_user.id
        db_sess = db_session.create_session()

        data = db_sess.query(Basket).all()
        users_ids = [usr.buyer_id for usr in data]
        products_ids = [prd.product_id if prd.buyer_id == user_id else None for prd in data]
        product_to_by = db_sess.query(Product).filter(Product.id == product_id).first()
        if int(user_id) in users_ids and int(product_id) in products_ids:
            db_basket_product = db_sess.query(Basket).filter(
                and_(Basket.product_id == product_id, Basket.buyer_id == user_id)).first()
            db_basket_product.quantity = min(db_basket_product.quantity + 1, product_to_by.quantity)
            db_sess.commit()
        else:
            if product_to_by.quantity == 0:
                return jsonify({'message': 'Продукта нет на складе'}), 400
            new_basket(user_id, product_id, 1)
        return jsonify({'message': 'Данные успешно обновлены!'}), 200
    except Exception as ex:
        print(ex)
        return jsonify({'error': str(ex)}), 500


@login_required
@app.route('/add_review/<product_id>')
def add_review(product_id):
    try:
        user_id = current_user.id
    except Exception:
        params = {
            'is_not_buyer': True,
            'product_exist': True,
            'css_style': url_for('static', filename='css/main_page.css')
        }
        return render_template('add_review.html', **params)
    db_sess = db_session.create_session()
    products_ids = db_sess.query(Product).all()
    products_ids = [prd.id for prd in products_ids]
    buyers_ids = db_sess.query(Buyer).all()
    buyers_ids = [int(buyer.id) for buyer in buyers_ids]
    params = {
        'is_not_buyer': user_id not in buyers_ids,
        'products_not_exists': int(product_id) not in products_ids,
        'css_style': url_for('static', filename='css/main_page.css')
    }
    return render_template('add_review.html', **params)


@login_required
@app.route('/submit-review', methods=['POST'])
def submit_review():
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
        for i in photos:
            if i.filename.split('.')[-1] not in ('png', 'jpg', 'bmp', 'jpeg'):
                return redirect('/')
        for photo in range(len(photos)):
            photos[photo].save(os.path.join(f'static/photos/reviews/{latest_review}', f'{photo}.png'))
    average_reviews = count_average(db_sess.query(Review).filter(Review.product_id == product_id).all())
    db_product = db_sess.query(Product).filter(Product.id == product_id).first()
    db_product.rating = average_reviews
    db_sess.commit()
    return redirect('/')


@login_required
@app.route('/add_product')
def add_product():
    try:
        seller_id = current_user.id
    except Exception:
        params = {
            'is_not_seller': True,
            'css_style': url_for('static', filename='css/main_page.css')
        }
        return render_template('add_product.html', **params)
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
        if not os.path.exists(f'static/photos/products/{latest_product}'):
            os.makedirs(f'static/photos/products/{latest_product}')
        if any(photos):
            for i in photos:
                if i.filename.split('.')[-1] not in ('png', 'jpg', 'bmp', 'jpeg'):
                    return redirect('/')
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
    db_sess = db_session.create_session()
    current_user = flask_login.current_user
    user_id = current_user.id
    buyers_ids = db_sess.query(Buyer).all()
    buyers_ids = [buyer.id for buyer in buyers_ids]
    if user_id not in buyers_ids:
        params = {
            'is_not_buyer': True,
            'css_style': url_for('static', filename='css/main_page.css')
        }
        return render_template('add_review.html', **params)
    params = {
        'css_style': url_for('static', filename='css/main_page.css')
    }
    return render_template('cart.html', **params)


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
    return jsonify(data)


@app.route('/search/<query>')
def search_result(query):
    params = {
        'css_style': url_for('static', filename='css/main_page.css')
    }
    return render_template('search.html', **params)


@app.route('/product/<product_id>')
def product(product_id):
    db_sess = db_session.create_session()
    reviews = db_sess.query(Review).filter(Review.product_id == product_id).all()
    product = db_sess.query(Product).filter(Product.id == product_id).first()
    seller = db_sess.query(Seller).filter(Seller.id == product.seller_id).first()
    reviews_info = []
    for i in reviews:
        try:
            user = (f"{db_sess.query(Buyer).filter(Buyer.id == i.buyer_id).first().name} "
                    f"{db_sess.query(Buyer).filter(Buyer.id == i.buyer_id).first().surname}")
        except Exception as err:
            user = "DELETED"
        reviews_info.append(
            {'username': user,
             'rating': i.rating,
             'text': i.text,
             'photos': get_photos_from_id(i.id, 'reviews')
             })

    params = {
        'css_style': url_for('static', filename='css/main_page.css'),
        'reviews': reviews_info,
        'product': {'id': product_id, 'name': product.name, 'seller_name': seller.name,
                    'description': product.description,
                    'price': product.price,
                    'rating': product.rating,
                    'photos': get_photos_from_id(product_id, 'products')}
    }
    return render_template('product.html', **params)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    params = {
        'css_style': url_for('static', filename='css/main_page.css')
    }
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", **params)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Указанная почта занята", **params)
        if not 14 < form.age.data < 200:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Недопустимый возраст", **params)
        if form.type.data == "buyer":
            user = new_buyer(form.name.data, form.surname.data, form.email.data, form.password.data,
                             form.gender.data, form.age.data)
        else:
            user = new_seller(form.name.data, form.surname.data, form.email.data, form.password.data,
                              form.gender.data, form.age.data)
        db_sess.add(user)
        login_user(db_sess.query(User).get(user.id))
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form, **params)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    params = {
        'css_style': url_for('static', filename='css/main_page.css')
    }
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            if db_sess.query(eval(db_sess.query(User).get(user.id).type.capitalize())).get(user.id).check_password:
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, **params)
    return render_template('login.html', title='Авторизация', form=form, **params)


@app.route('/account')
def account():
    user = current_user.get_user()
    rating = 0.0
    if current_user.type == "seller":
        db_sess = db_session.create_session()
        all_products = db_sess.query(Product).filter(Product.seller_id == current_user.id).all()
        rating = count_average(all_products)
    params = {
        'css_style': url_for('static', filename='css/main_page.css'),
        'rating': rating
    }
    return render_template('account.html', user=user, **params)


@app.route('/account/edit', methods=['GET', 'POST'])
@login_required
def edit_account():
    form = EditForm()
    if request.method == "GET":
        user = current_user.get_user()
        form.name.data = user.name
        form.surname.data = user.surname
        form.email.data = user.email
        form.password.data = user.password
        form.gender.data = user.gender
        form.age.data = user.age
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('edit.html', title='Изменение аккаунта',
                                   form=form,
                                   message="Пароли не совпадают")
        if not 14 < form.age.data < 200:
            return render_template('edit.html', title='Изменение аккаунта',
                                   form=form,
                                   message="Недопустимый возраст")
        db_sess = db_session.create_session()
        user = current_user.get_user()
        user.name = form.name.data
        user.surname = form.surname.data
        user.email = form.email.data
        user.set_password(form.password.data)
        user.gender = form.gender.data
        user.age = form.age.data
        user_ = db_sess.query(User).get(current_user.id)
        user_.email = form.email.data
        db_sess.commit()
        return redirect('/account')
    params = {
        'css_style': url_for('static', filename='css/main_page.css'),
    }
    return render_template('edit.html', title='Изменение аккаунта', form=form, **params)


@app.route('/account/delete')
@login_required
def delete_account():
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    user_ = user.get_user(db_sess)
    db_sess.delete(user)
    db_sess.delete(user_)
    db_sess.commit()
    return redirect('/')


@app.route('/account/leave')
@login_required
def leave_account():
    logout_user()
    return redirect('/')


@app.route('/admin/list_of_buyers')
def list_of_buyers():
    db_sess = db_session.create_session()
    buyers = db_sess.query(Buyer).all()
    user = current_user.get_user()
    return render_template("list_of_buyers.html", buyers=buyers, user=user)


@app.route('/admin/list_of_sellers')
def list_of_sellers():
    db_sess = db_session.create_session()
    sellers = db_sess.query(Seller).all()
    user = current_user.get_user()
    return render_template("list_of_sellers.html", sellers=sellers, user=user)


@app.route('/admin/list_of_admins')
def list_of_admins():
    db_sess = db_session.create_session()
    admins = db_sess.query(Admin).all()
    user = current_user.get_user()
    return render_template("list_of_admins.html", admins=admins, user=user)


@app.route('/admin/delete/<int:id>')
def delete_account_for_admin(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    type = user.type
    user_ = user.get_user(db_sess)
    db_sess.add(user_)
    db_sess.delete(user)
    db_sess.delete(user_)
    db_sess.commit()
    return redirect(f'/admin/list_of_{type}s')


@app.route('/admin/give_admin/<int:id>')
def give_admin(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    type = user.type
    user_ = user.get_user(db_sess)
    id = user_.id
    name = user_.name
    surname = user_.surname
    email = user_.email
    password = user_.password
    gender = user_.gender
    age = user_.age
    date = user_.date
    db_sess.delete(user_)
    admin = Admin()
    admin.id = id
    admin.name = name
    admin.surname = surname
    admin.email = email
    admin.set_password(password)
    admin.gender = gender
    admin.age = age
    admin.date = date
    db_sess.add(admin)
    user.type = "admin"
    db_sess.commit()
    return redirect(f'/admin/list_of_{type}s')


@app.route('/admin/give_buyer/<int:id>')
def give_buyer(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    user_ = user.get_user(db_sess)
    id = user_.id
    name = user_.name
    surname = user_.surname
    email = user_.email
    password = user_.password
    gender = user_.gender
    age = user_.age
    date = user_.date
    db_sess.delete(user_)
    buyer = Buyer()
    buyer.id = id
    buyer.name = name
    buyer.surname = surname
    buyer.email = email
    buyer.set_password(password)
    buyer.gender = gender
    buyer.age = age
    buyer.date = date
    db_sess.add(buyer)
    user.type = "buyer"
    db_sess.commit()
    return redirect('/admin/list_of_admins')


@app.route('/get_seller_products', methods=['GET'])
def get_seller_products():
    current_user = flask_login.current_user
    user_id = current_user.id
    products = []
    db_sess = db_session.create_session()
    all_products = db_sess.query(Product).filter(Product.seller_id == user_id).all()
    for el in all_products:
        product_data = {}
        product_data['id'] = el.id
        product_data['name'] = el.name
        product_data['price'] = el.price
        product_data['image'] = get_photos_from_id(el.id, 'products')[0]
        product_data['quantity'] = el.quantity
        product_data['rating'] = el.rating
        products.append(product_data)
    return jsonify(products)


db_session.global_init("db/db.db")
'''

new_product(2, "Сармат", "Настоящий", 999999999999.99, 1)

new_review(1, 1, 5, "Реально настоящий")

new_buyer("Покупатель", "С фамилией", "buyer@mail.ru", "buyer", "male", 19)

new_seller("Продавец", "Без фамилией", "seller@mail.ru", "seller", "male", 99)

new_admin("Дмитрий", "Кривошея", "krivosheya_da@mail.ru", "03092008", "male", 15, True)
new_admin("Сармат", "Сакиев", "sarmat@mail.ru", "hard_password", "male", 16, True)
new_admin("Матвей", "Верташов", "matvey@mail.ru", "123", "male", 16, True)
'''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3555', debug=False)
