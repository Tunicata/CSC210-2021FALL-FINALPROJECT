from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from .models import Products
from . import db
from flask_login import login_required

app = Blueprint('app', __name__)

filters = ["Price (ascending)", "Price (descending)"]
filters.sort()

def get_category_func(category):
	temp = None
	if category == "70s Video Games": temp = 'app.index'
	elif category == "80s Video Games": temp = 'app.index'
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
		if request.args.get('filter') != None: filter_by = request.args.get('filter')
		if request.args.get('category') != None: category = request.args.get('category')
	elif request.method == "POST":
		filter_by = request.form['filter']
		category = request.form['category']
	if filter_by == "Price (ascending)":
		if category != "All": products = Products.query.filter_by(category=category).order_by(Products.originalPrice).all()
		else: products = Products.query.order_by(Products.originalPrice).all()
	elif filter_by == "Price (descending)":
		if category != "All": products = Products.query.filter_by(category=category).order_by(Products.originalPrice.desc()).all()
		else: products = Products.query.order_by(Products.originalPrice.desc()).all()
	return render_template('home.html', function='app.index', products=products, filters=filters, filter_by=filter_by, category = category, categorys = categorys)

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
	search = ""
	products = Products.query.order_by(Products.id)
	if request.method == "POST":
		search = request.form['search']
		products = Products.query.filter(Products.title.contains(search)).order_by(Products.id).all()
	return render_template('table.html', products=products)

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