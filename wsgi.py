# wsgi.py
from flask import Flask, request, render_template
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from models import Product

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # Order is important here!
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema, product_schema


@app.route('/')
def home():
    products = db.session.query(Product).all()

    return render_template('home.html', products=products)

@app.route('/<int:id>')
def product_html(id):
    product = db.session.query(Product).get(id)
    return render_template('product.html', product=product)

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/products')
def products():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return products_schema.jsonify(products)

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = db.session.query(Product).get(id) # SQLAlchemy request => 'SELECT * FROM products WHERE products.id = "1"'
    return product_schema.jsonify(product)

@app.route('/products', methods=['POST'])
def create_product():
    body = request.get_json()
    product = Product(name=body['name'])
    db.session.add(product) # SQLAlchemy request => 'INSERT values'
    db.session.commit()
    return product_schema.jsonify(product)

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = db.session.query(Product).get(id)
    db.session.delete(product) # SQLAlchemy request => 'DELETE values'
    db.session.commit()
    return product_schema.jsonify(product)

@app.route('/products', methods=['PATCH'])
def update_product():
    body = request.get_json()
    product = db.session.query(Product).get(body['id'])
    product.name = body['name']
    product.description = body['description']
    db.session.commit()
    return product_schema.jsonify(product)
