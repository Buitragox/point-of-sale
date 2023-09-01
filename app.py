import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template
from utils.db import db
from sqlalchemy import text
from models.product import Product

# Routes
from routes.admin import admin
from routes.seller import seller


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
    db.init_app(app)
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(seller, url_prefix="/seller")
    
    @app.route('/test')
    def test():
        # Execute a raw SQL statement 
        result = db.session.execute(text('SELECT * FROM account.role_account'))

        roles = []
        
        for row in result:
            roles.append(row)

        return render_template("test.jinja", roles=(roles))

    @app.route('/hello')
    def hello():
        return '<h1>Hello!!</h1>'
    
    @app.route('/')
    def index():
        admin = '/admin/login'
        seller = '/seller/login'
        return render_template("index.jinja", admin=admin, seller=seller)

    return app

