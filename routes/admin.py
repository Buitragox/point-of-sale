from flask import Blueprint, render_template, request, flash, redirect, url_for
from utils.db import db
from models.product import Product
from models.user import UserAccount
from sqlalchemy import text, update
import hashlib

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
        md5Pass = hashlib.md5(password.encode()).hexdigest() 
        
        
        message = "¡¡¡La contraseña no coincide!!!"
        alert = "alert alert-danger"
        if password == passCheck:
            newUser = UserAccount(user, str(md5Pass), 1, 1)
            
            db.session.add(newUser)
            db.session.commit()
            message = "¡¡¡Se registro correctamente!!!"
            alert = "alert alert-success"

        return render_template("add_seller.jinja", message = message, alert = alert)
    else: 
        return render_template("add_seller.jinja")

@admin.route('/delete_user/<id>')
def delete_user(id):
    
    query = text(f"SELECT * FROM account.user_account WHERE user_id='{id}' ")
    result = db.session.execute(query).first()
    
    if result.user_state == 0:
        db.session.query(UserAccount).filter(UserAccount.UUID_user == str(id)).update({UserAccount.user_status : '1'}, synchronize_session = False)
    else:
        db.session.query(UserAccount).filter(UserAccount.UUID_user == str(id)).update({UserAccount.user_status : '0 '}, synchronize_session = False)
    
    db.session.commit()
    '''
    #print(query2)
    #result = db.session.execute(query, parametros)
    #print(result)
    db.session.commit()
    '''
    return redirect(url_for('admin.update_user'))



@admin.route('/update_user', methods=['GET'])
def update_user():
    query = text(f"SELECT * FROM account.user_account")
    users = db.session.execute(query).all()

    return render_template('update_user.jinja', users = users)