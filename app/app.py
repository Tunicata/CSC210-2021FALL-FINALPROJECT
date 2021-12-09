from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, flash
from flask_login import current_user
from .models import Products, Cart, User, Order
from . import db
from flask_login import login_required
from datetime import datetime

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


@app.route('/top_up', methods=['GET', 'POST'])
@login_required
def top_up_user():
    return redirect(url_for('app.index'))


@app.route("/cart")
@login_required
def cart():
    curr_cart = Cart.query.filter_by(user_id=current_user.id).order_by(Cart.add_time)
    return render_template('cart.html', cart=curr_cart, Products=Products)


@app.route("/cart_add/<string:curr_product_id>")
@login_required
def cart_add(curr_product_id):
    try:
        cart = Cart.query.filter_by(products_id=curr_product_id).first()
        product = Products.query.filter_by(id=curr_product_id).first()

        if cart:
            cart.number = cart.number + 1

        else:
            cart = Cart(
                products_id=curr_product_id,
                user_id=current_user.id,
                number=1,
                add_time=datetime.now()
            )
            db.session.add(cart)

        if cart.number > product.stockAmount:
            flash("Insufficient Stock!")
        else:
            db.session.commit()

        return redirect(url_for('app.index'))

    except:
        return render_template('error.html')


@app.route("/cart_modify_num/<string:cart_id>")
@login_required
def cart_modify_num(cart_id):
    try:
        target = Cart.query.filter_by(id=abs(int(cart_id))).first()
        product = Products.query.filter_by(id=target.products_id).first()

        if int(cart_id) > 0:
            target.number = target.number + 1
        else:
            target.number = target.number - 1
        if not target.number:
            db.session.delete(target)

        if target.number > product.stockAmount:
            flash("Insufficient Stock!")
        else:
            db.session.commit()

        return redirect(url_for('app.cart'))
    except:
        return render_template('error.html')


@app.route("/cart_delete/<string:cart_id>")
@login_required
def cart_delete(cart_id):
    try:
        target = Cart.query.filter_by(id=cart_id).first()
        db.session.delete(target)
        db.session.commit()
        return redirect(url_for('app.cart'))
    except:
        return render_template('error.html')


@app.route("/clear_cart")
@login_required
def clear_cart():
    try:
        targets = Cart.query.filter_by(user_id=current_user.id).all()
        [db.session.delete(target) for target in targets]
        db.session.commit()
        return redirect(url_for('app.cart'))
    except:
        return render_template('error.html')


@app.route("/check_out/<float:total_price>")
@login_required
def check_out(total_price):
    insufficient_stock = []
    try:
        if total_price:
            if current_user.wallet >= total_price:
                curr_cart = Cart.query.filter_by(user_id=current_user.id).order_by(Cart.add_time)
                orders = []
                for cart_item in curr_cart:
                    product = Products.query.filter_by(id=cart_item.products_id).first()
                    if cart_item.number <= product.stockAmount:
                        product.stockAmount -= cart_item.number
                        for i in range(cart_item.number):
                            order = Order(
                                user_id=cart_item.user_id,
                                product_id=cart_item.products_id,
                                place_time=datetime.now(),
                                cdk=""
                            )
                            orders.append(order)
                            db.session.add(order)
                        current_user.wallet = current_user.wallet - product.originalPrice
                    else:
                        insufficient_stock.append(product.title)
                    db.session.delete(cart_item)
                db.session.commit()
                if insufficient_stock:
                    flash("the following orders are incomplete yet due to insufficient stock: " + str(insufficient_stock))
                return render_template('purchase_success.html', orders=orders, products=Products)
            else:
                flash("Insufficient balance!")
        else:
            flash("Your Cart is Empty!")
        return redirect(url_for('app.cart'))
    except:
        return render_template('error.html')
