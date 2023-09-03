from flask import Blueprint, render_template, request, flash
from utils.db import db
from models.product import Product
from models.user import UserAccount
from sqlalchemy import text

admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")


@admin.route('/')
def home():
    return render_template("admin.jinja")


@admin.route('/add_product', methods = ['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        name = request.form["name"]
        amount = int(request.form['amount'])
        price = float(request.form['price'])

        if len(name) != 0 and amount >= 0 and price >= 0:
            new_product = Product(name, amount, price)
            db.session.add(new_product)
            db.session.commit()
            flash("Se registró el producto")
        else:
            flash("Parametros inválidos")

        return render_template("add_product.jinja")
    else: 
        return render_template("add_product.jinja")


@admin.route('/list_products', methods=['GET'])
def list_products():
    query = text(f"SELECT * FROM inventory.product")
    result = db.session.execute(query).all()
    return render_template("test.jinja", rows=result)


@admin.route('/add_seller', methods=['POST', 'GET'])
def new_seller():
    if request.method == 'POST':
        user = request.form["user"]
        password = request.form['password']
        passCheck = request.form['pass_check']
        
        message = "¡¡¡La contraseña no coincide!!!"
        if password == passCheck:
            newUser = UserAccount(user, password, 1)
            
            db.session.add(newUser)
            db.session.commit()
            message = "¡¡¡Se registro correctamente!!!"

        return render_template("add_seller.jinja", message = message)
    else: 
        return render_template("add_seller.jinja")

