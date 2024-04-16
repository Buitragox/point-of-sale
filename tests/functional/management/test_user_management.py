from flask.testing import FlaskClient
from utils.db import db
from models.user import UserAccount
from time import sleep

def test_add_seller_valid_credentials(admin_client: FlaskClient):
    response = admin_client.post('/admin/add_seller', data={
        "user": "newseller",
        "password": "newseller",
        "pass_check": "newseller",
    })
    assert bytes('Se registró correctamente!', 'utf-8') in response.get_data()

def test_add_seller_invalid_passcheck(admin_client: FlaskClient):
    response = admin_client.post('/admin/add_seller', data={
        "user": "newseller",
        "password": "newseller",
        "pass_check": "not_equal",
    })
    assert bytes('La contraseña no coincide!', 'utf-8') in response.get_data()

def test_deactivate_user(admin_client: FlaskClient):
    user = UserAccount.query.filter_by(user_name='seller').first()
    response = admin_client.get('/admin/delete_user/' + str(user.user_id))
    db.session.refresh(user)
    assert user.user_state == 0
