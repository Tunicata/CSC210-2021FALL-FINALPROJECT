from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, flash
from flask_login import current_user
from .models import Products, Cart, User
from . import db
from flask_login import login_required

app = Blueprint('app', __name__)

filters = ["Price (ascending)", "Price (descending)"]
filters.sort()


def get_category_func(category):
    temp = None
    if category == "70s Video Games":
        temp = 'app.index'
    elif category == "80s Video Games":
        temp = 'app.index'
    return temp


@app.route('/', methods=['GET', 'POST'])
def index():
    filter_by = "Price (ascending)"
    category = "All"
    products = Products.query.order_by(Products.originalPrice).all()
    categorys = Products.query.with_entities(Products.category).distinct().all()
    categorys = [i[0] for i in categorys]
    categorys.sort()
    if request.method == "GET":
        if request.args.get('filter'):
            filter_by = request.args.get('filter')
        if request.args.get('category'):
            category = request.args.get('category')
    elif request.method == "POST":
        filter_by = request.form['filter']
        category = request.form['category']
    if filter_by == "Price (ascending)":
        if category != "All":
            products = Products.query.filter_by(category=category).order_by(Products.originalPrice).all()
        else:
            products = Products.query.order_by(Products.originalPrice).all()
    elif filter_by == "Price (descending)":
        if category != "All":
            products = Products.query.filter_by(category=category).order_by(Products.originalPrice.desc()).all()
        else:
            products = Products.query.order_by(Products.originalPrice.desc()).all()
    return render_template('home.html', function='app.index', products=products, filters=filters, filter_by=filter_by,
                           category=category, categorys=categorys)


@app.route('/create_items', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == "POST":
        title = request.form['title']
        category = request.form['category']
        amount = request.form['amount']
        price = request.form['price']
        link = request.form['link']
        listing = Products(title=title, category=category, stockAmount=amount, originalPrice=price, imgLink=link)
        try:
            db.session.add(listing)
            db.session.commit()
            return redirect(url_for('app.table'))
        except:
            return render_template('error.html')
    else:
        return render_template('create.html')


@app.route('/update_items', methods=['GET', 'POST'])
@login_required
def table():
    if current_user.admin:
        search = ""
        products = Products.query.order_by(Products.id)
        if request.method == "POST":
            search = request.form['search']
            products = Products.query.filter(Products.title.contains(search)).order_by(Products.id).all()
        return render_template('table.html', products=products)
    else:
        flash('Current login user is not an Administrator.')
        return redirect(url_for('app.index'))


@app.route('/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    delete = Products.query.filter_by(id=id).first()
    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect(url_for('app.table'))
    except:
        return render_template('error.html')


@app.route('/update/<string:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    update = Products.query.filter_by(id=id).first()
    if request.method == "POST":
        try:
            update.title = request.form['title']
            update.category = request.form['category']
            update.id = request.form['id']
            update.stockAmount = request.form['amount']
            update.originalPrice = request.form['price']
            update.imgLink = request.form['link']
            db.session.commit()
            return redirect(url_for('app.table'))
        except:
            return render_template('error.html')
    else:
        return render_template('update.html', update=update)


@app.route('/item/<string:id>', methods=['GET', 'POST'])
def item(id):
    item = Products.query.filter_by(id=id).first()
    category = get_category_func(item.category)
    return render_template('item.html', item=item, category=category)


@app.route('/user_management', methods=['GET', 'POST'])
@login_required
def user_table():
    if current_user.admin:
        users = User.query.order_by(User.id)
        return render_template('user_table.html', users=users)
    else:
        flash('Current login user is not an Administrator.')
        return redirect(url_for('app.index'))


@app.route('/user_delete/<string:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    target = User.query.filter_by(id=user_id).first()
    try:
        db.session.delete(target)
        db.session.commit()
        return redirect(url_for('app.user_table'))
    except:
        return render_template('error.html')


@app.route('/top_up/<string:user_id>', methods=['GET', 'POST'])
@login_required
def top_up_user(user_id):
    pass


@app.route("/cart_add/")
def cart_add():
    # cart = Cart(
    #     products_id=request.args.get('products_id'),
    #     number=request.args.get('number'),
    #     user_id=session.get('user_id', 0)
    # )

    # db.session.add(cart)
    # db.session.commit()
    return redirect(url_for('app.index'))
