from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from utils.db import db
from models.product import Product
from models.user import UserAccount
from sqlalchemy import text, update

admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

@admin.before_request
def before_request():
    if not "user_name" in session or session["user_role"] != 0:
        return redirect(url_for("login"))

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
    result = Product.query.all()
    # query = text(f"SELECT * FROM inventory.product")
    # result = db.session.execute(query).all()
    return render_template("products.jinja", rows=result)


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
                else:
                    return render_template("edit.jinja", rows=result)
            else:
                flash("El ID es un valor numerico.")
                return render_template("search.jinja")
        elif int(option) == 2:
                query = text(f"SELECT * FROM inventory.product WHERE product_name='{str(value)}'")
                result = db.session.execute(query).first()
                if result is None:
                    flash("No se encontró el producto.")
                    return render_template("search.jinja")
                else:
                    return render_template("edit.jinja", rows=result)
    else:
        return render_template("search.jinja")

@admin.route('/add_seller', methods=['POST', 'GET'])
def new_seller():
    if request.method == 'POST':
        user = request.form["username"]
        password = request.form['password']
        pass_check = request.form['pass_check']

        message = "La contraseña no coincide!"
        alert = "alert alert-danger"

        if password == pass_check:
            newUser = UserAccount(user, password, 1, 1)

            db.session.add(newUser)
            db.session.commit()
            message = "Se registró correctamente!"
            alert = "alert alert-success"

        return render_template("add_seller.jinja", message=message, alert=alert)
    else:
        return render_template("add_seller.jinja")

@admin.route('/delete_user/<id>', methods=['GET'])
def delete_user(id):
    result = UserAccount.query.filter_by(user_id=id).first()

    if result.user_state == 0:
        db.session.execute(update(UserAccount).where(UserAccount.user_id == str(id)).values(user_state=1).execution_options(synchronize_session="auto"))
    else:
        db.session.execute(update(UserAccount).where(UserAccount.user_id == str(id)).values(user_state=0).execution_options(synchronize_session="auto"))

    db.session.commit()

    return redirect(url_for('admin.update_user'))



@admin.route('/update_user', methods=['GET'])
def update_user():
    users = UserAccount.query.all()

    return render_template('update_user.jinja', users = users)