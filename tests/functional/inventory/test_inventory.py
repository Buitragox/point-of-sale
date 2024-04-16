from flask.testing import FlaskClient
from models.product import Product

def test_add_product(admin_client: FlaskClient):
    response = admin_client.post('/admin/add_product', data={
        "name": "papa",
        "amount": "20",
        "price": "10000",
    })
    assert bytes('Se registró el producto', 'utf-8') in response.get_data()

def test_add_product_invalid_price(admin_client: FlaskClient):
    response = admin_client.post('/admin/add_product', data={
        "name": "adsada",
        "amount": "20",
        "price": "-3",
    })
    assert bytes('Parametros inválidos', 'utf-8') in response.get_data()

def test_search_products(inv_client: FlaskClient):
    prod : Product = Product.query.filter_by(product_name='Papa').first()
    response = inv_client.post('/admin/search', data={
        "value": prod.product_id,
        "option": 1,
    })
    assert b"Papa" in response.get_data()

def test_search_products(inv_client: FlaskClient):
    response = inv_client.post('/admin/search', data={
        "value": 999999,
        "option": 1,
    })
    assert bytes("No se encontró el producto.", 'utf-8') in response.get_data()

def test_edit_products(inv_client: FlaskClient):
    prod : Product = Product.query.filter_by(product_name='Papa').first()
    response = inv_client.post('/admin/edit', data={
        "id": prod.product_id,
        "name": "Papita genial",
        "amount": 300000,
        "price": 500,
    })
    assert bytes("Se guardó correctamente.", 'utf-8') in response.get_data()