from flask import Flask 

def create_app():
    app = Flask(__name__)

    #app.config.from_pyfile('settings.py')

    @app.route('/hello')
    def index():
        return '<h1>Hello World!</h1>'

    return app

