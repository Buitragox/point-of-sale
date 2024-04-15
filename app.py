import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

from flask import Flask, render_template, request, redirect, flash, session
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

        return render_template("test.jinja", rows=result)
    
    @app.route('/add_admin/<username>&<password>')
    def add_admin(username, password):
        # Execute a raw SQL statement 
        prod = UserAccount(username, password, 0, 1)
        db.session.add(prod)
        db.session.commit()
        return redirect("/test")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # Execute a raw SQL statement 
        if request.method == 'POST':
            #quit session
            session.pop("user_name", None)
            session.pop("user_role", None)
            session.pop("user_id", None)

            next_template = 'login.jinja' # return to login by default
            user = request.form['username']
            password = request.form['password']

            md5_pass = hashlib.md5(password.encode()).hexdigest()

            query = text(f"SELECT * FROM account.user_account WHERE user_name='{user}' AND user_password='{str(md5_pass)}'")

            result = db.session.execute(query).first()
            
            # If user_name doesn't exist or password doesn't match
            if result is None: 
                flash("Usuario y/o contrasena incorrectos")
            elif result.user_state == 0:
                flash("Usuario deshabilitado")
            else:
                session["user_name"] = result.user_name
                session["user_role"] = result.user_role
                session["user_id"] = result.user_id
                if result.user_role == 0: # Admin
                    next_template = 'admin.jinja'
                elif result.user_role == 1: # Seller
                    next_template = 'seller.jinja'

            return render_template(next_template)
        else:   
            return render_template('login.jinja')
    
    @app.route('/')
    def index():
        return render_template("login.jinja")
    
    return app

