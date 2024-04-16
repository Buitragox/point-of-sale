from flask.testing import FlaskClient

def test_login_valid_credentials(client: FlaskClient):
    response = client.post('/login', data={
        "username": "seller",
        "password": "seller",
    })
    assert bytes('Soy Vendedor', 'utf-8') in response.get_data()


def test_login_invalid_password(client: FlaskClient):
    response = client.post('/login', data={
        "username": "seller",
        "password": "asdf",
    })
    assert bytes('Usuario y/o contrasena incorrectos', 'utf-8') in response.get_data()

def test_login_invalid_username(client: FlaskClient):
    response = client.post('/login', data={
        "username": "asdf",
        "password": "asdf",
    })
    assert bytes('Usuario y/o contrasena incorrectos', 'utf-8') in response.get_data()
