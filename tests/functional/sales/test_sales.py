from flask.testing import FlaskClient
from utils.db import db
from models.user import UserAccount
from models.product import Product
from random import sample

def test_add_sale(seller_client: FlaskClient):
    products = db.session.query(Product).all()
    test_products = sample(products, 2)
    product_ids = list(map(lambda p: p.product_id, test_products))
    response = seller_client.post('/seller/process_sale', data={
        "product_id[]": product_ids,
        "amount[]": [5, 8],
        "client_id": 1234,
    }, follow_redirects=True)
    assert bytes('Venta exitosa', 'utf-8') in response.get_data()

def test_add_sale_invalid_id(seller_client: FlaskClient):
    response = seller_client.post('/seller/process_sale', data={
        "product_id[]": [999999, 3333333],
        "amount[]": [1, 1],
        "client_id": 1234,
    }, follow_redirects=True)
    assert bytes('ID de producto invalido', 'utf-8') in response.get_data()
