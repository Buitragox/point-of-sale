import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
    db = SQLAlchemy(app)
    
    #app.config.from_pyfile('settings.py')
    @app.route('/test')
    def test():
        # Execute a raw SQL statement 
        result = db.session.execute(text('SELECT * FROM account.role_account'))
        
        for row in result:
            print(row)

        return "aaaaaa"

    @app.route('/')
    def index():
        return '<h1>Hello!!</h1>'

    return app

