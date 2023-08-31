import os

from flask import Flask, render_template
from utils.db import db
from sqlalchemy import text
from models.product import Product

from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
    db.init_app(app)
    
    #app.config.from_pyfile('settings.py')
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
    
    @app.route('/add_product')
    def add_product():
        prod = Product("Leche", 5, 15000)
        db.session.add(prod)
        db.session.commit()
        return "creacion exitosa"
    
    @app.route('/')
    def index():
        return render_template("index.jinja")

    return app

