from flask.testing import FlaskClient
from utils.db import db
from models.user import UserAccount

def test_show_login_page(client: FlaskClient):
    response = client.get('/')
    assert response.content_type == 'text/html; charset=utf-8'
    assert response.status_code == 200
    assert bytes('Inicie sesión', 'utf-8') in response.get_data()

def test_login_valid_credentials(client: FlaskClient):
    response = client.post('/login', data={
        "username": "admin",
        "password": "admin",
    })
    assert bytes('Soy Admin', 'utf-8') in response.get_data()

def test_login_invalid(client: FlaskClient):
    response = client.post('/login', data={
        "username": "asdf",
        "password": "asdf",
    })
    assert bytes('Usuario y/o contrasena incorrectos', 'utf-8') in response.get_data()

def test_login_disabled(client: FlaskClient):
    user = UserAccount("test", "test", 0, 0)
    db.session.add(user)
    db.session.commit()
    response = client.post('/login', data={
        "username": user.user_name,
        "password": "test",
    })
    assert bytes('Usuario deshabilitado', 'utf-8') in response.get_data()