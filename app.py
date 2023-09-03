import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, request, redirect, flash
from utils.db import db
from sqlalchemy import text

# Models
from models.product import Product
from models.user import UserAccount

# Routes
from routes.admin import admin
from routes.seller import seller


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")

    # TODO Change this to .env with another key.
    app.config['SECRET_KEY'] = "4e041161ab1f2548591d829ecdeb58bd3921a59462c714e2ccddbe02b69216d4"
    db.init_app(app)
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(seller, url_prefix="/seller")
    
    @app.route('/test')
    def test():
        # Execute a raw SQL statement 
        result = db.session.execute(text('SELECT * FROM account.user_account')).all()
        #result = db.session.execute(text('SELECT * FROM account.role_account'))

        # rows = []
        
        # for row in result:
        #     rows.append(row)

        return render_template("test.jinja", rows=result)
    
    @app.route('/add_admin/<username>&<password>')
    def add_admin(username, password):
        # Execute a raw SQL statement 
        prod = UserAccount(username, password, 0)
        db.session.add(prod)
        db.session.commit()
        return redirect("/test")


    @app.route('/hello')
    def hello():
        return '<h1>Hello!!</h1>'

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # Execute a raw SQL statement 
        if request.method == 'POST':
            next_template = 'login.jinja' # return to login by default
            user = request.form['username']
            password = request.form['password']

            query = text(f"SELECT * FROM account.user_account WHERE user_name='{user}' AND user_password='{password}'")
            result = db.session.execute(query).first()

            # If user_name doesn't exist or password doesn't match
            if result is None: 
                flash("Usuario y/o contrasena incorrectos")

            elif result.user_password == password:
                if result.user_role == 0: # Admin
                    next_template = 'admin.jinja'
                elif result.user_role == 1: # Seller
                    next_template = 'seller.jinja'

            return render_template(next_template)
        else:   
            return render_template('login.jinja')
    
    @app.route('/')
    def index():
        return render_template("index.jinja")
    
    return app

