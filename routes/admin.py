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

from models.product import Product
@admin.route('/edit', methods = ['POST'])
def edit():
    if request.method == 'POST':
        id = request.form["id"]
        name = request.form["name"]
        amount = request.form["amount"]
        price = request.form["price"]
        db.session.query(Product).filter(Product.product_id == int(id)).update(
            {Product.product_name : str(name), Product.product_amount : int(amount), Product.product_price : float(price)}, synchronize_session = False)
        db.session.commit()
        return render_template("search.jinja", message = "Se guardó correctamente.")

@admin.route('/search', methods=['POST', 'GET'])
def search_products():
    if request.method == 'POST':
        value = request.form["value"]
        option = request.form["option"]
        print(value, option)
        if len(option) > 1:
            flash("Debe seleccionar una opción de búsqueda válida")
            return render_template("search.jinja")
        if int(option) == 1:
            if value.isdigit():
                query = text(f"SELECT * FROM inventory.product WHERE product_id='{int(value)}'")
                result = db.session.execute(query).first()
                if result is None: 
                    flash("No se encontró el producto.")
                    return render_template("search.jinja")
                else: return render_template("edit.jinja", rows=result)
            else: 
                flash("El ID es un valor numerico.")
                return render_template("search.jinja")
        elif int(option) == 2:
                query = text(f"SELECT * FROM inventory.product WHERE product_name='{str(value)}'")
                result = db.session.execute(query).first()
                if result is None: 
                    flash("No se encontró el producto.")
                    return render_template("search.jinja")
                else: return render_template("edit.jinja", rows=result)
    else:
        return render_template("search.jinja")

@admin.route('/add_seller', methods=['POST', 'GET'])
def new_seller():
    if request.method == 'POST':
        user = request.form["user"]
        password = request.form['password']
        passCheck = request.form['pass_check']
        
        message = "¡¡¡La contraseña no coincaide!!!"
        if password == passCheck:
            newUser = UserAccount(user, password, 1)
            
            db.session.add(newUser)
            db.session.commit()
            message = "¡¡¡Se registro correctamente!!!"

        return render_template("add_seller.jinja", message = message)
    else: 
        return render_template("add_seller.jinja")

