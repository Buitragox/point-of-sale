from flask import Blueprint, render_template, request
from utils.db import db
from models.product import Product
from models.user import UserAccount

admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

@admin.route('/add_product')
def add_product():
    prod = Product("Leche", 5, 15000)
    db.session.add(prod)
    db.session.commit()
    return "creacion exitosa"

@admin.route('/login')
def admin_login():
    home_page = '/'
    addSeller = '/admin/add_seller'
    return render_template("admin_login.jinja", home_page=home_page, add_seller=addSeller)


@admin.route('/add_seller', methods = ['POST', 'GET'])
def new_seller():

    if request.method == 'POST':
        user = request.form["user"]
        password = request.form['password']
        passCheck = request.form['pass_check']
        
        mensaje = "¡¡¡La contraseña no coincide!!!"
        if password == passCheck:
            newUser = UserAccount(user, password, 1)
            
            db.session.add(newUser)
            db.session.commit()
            mensaje = "¡¡¡Se registro correctamente!!!"

        return render_template("add_seller.jinja", mensaje = mensaje)
    else: 
        return render_template("add_seller.jinja")

