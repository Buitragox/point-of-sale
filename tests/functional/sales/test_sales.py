from flask.testing import FlaskClient
from utils.db import db
from models.user import UserAccount
from models.product import Product

def test_add_sale(seller_client: FlaskClient):
    response = seller_client.post('/seller/process_sale', data={
        "product_id[]": [2, 3],
        "amount[]": [5, 8],
        "client_id": 1234,
    }, follow_redirects=True)
    assert bytes('Venta exitosa', 'utf-8') in response.get_data()

def test_add_sale_invalid_id(seller_client: FlaskClient):
    response = seller_client.post('/seller/process_sale', data={
        "product_id[]": [999, 3],
        "amount[]": [1, 1],
        "client_id": 1234,
    }, follow_redirects=True)
    assert bytes('ID de producto invalido', 'utf-8') in response.get_data()
