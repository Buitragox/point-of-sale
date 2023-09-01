from flask import Blueprint, render_template
from utils.db import db
from models.product import Product

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
    return render_template("admin_login.jinja", home_page=home_page)
