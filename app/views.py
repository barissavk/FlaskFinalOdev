from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import Product

@app.route('/')
def index():
    products = Product.query.all()
    print(products)
    return render_template('index.html', products=products)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/client')
def client():
    return render_template('client.html')

@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

"""@app.route("/purchase/<int:id>")
def purchase_movie(id):
    movie = Movie.query.get_or_404(id)
    return render_template("purchase.html")"""

@app.route("/cart")
def cart(id):
    pass