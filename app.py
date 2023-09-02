import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, request
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

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # Execute a raw SQL statement 
        if request.method == 'POST':
            usr = request.form['username']
            pswrd = request.form['password']
            result = db.session.execute(text('SELECT * FROM account.user_account WHERE user_name ='+ usr))
            tmp = result.fetchall()
            if len(tmp) == 0: print("No hay resultados para esa busqueda.")
            elif tmp[0][1] == 0:
                print(usr,pswrd)
                print("Contrasena correcta.")
            else: print("Usuario y/o contrasena incorrectos")
        return render_template('login.jinja')
    
    @app.route('/')
    def index():
        return render_template("login.jinja")
    return app

