from flask import Blueprint, render_template
from utils.db import db
from models.product import Product

seller = Blueprint("seller", __name__, static_folder="static", template_folder="templates")

@seller.route('/login')
def seller_login():
    home_page = '/'
    return render_template("seller_login.jinja", home_page=home_page)