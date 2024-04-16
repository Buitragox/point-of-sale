import os
import pytest
from app import create_app, db
from models.user import RoleAccount, UserAccount
from models.product import Product
from models.product_sale import ProductSale
from sqlalchemy import text, delete
import sqlalchemy
from flask.testing import FlaskClient


def _create_all_schemas():
    # get all the tables defined in your models
    tables = db.Model.metadata.tables.values()

    # group the tables by schema
    schemas = {}
    for table in tables:
        schema_name = table.schema
        if schema_name not in schemas:
            schemas[schema_name] = []
        schemas[schema_name].append(table)

    # create the schemas
    with db.engine.connect() as conn:
        for schema_name, tables in schemas.items():
            if not conn.dialect.has_schema(conn, schema_name):
                conn.execute(sqlalchemy.schema.CreateSchema(schema_name))

        conn.commit()

@pytest.fixture(scope='module')
def client():
    # Set the Testing configuration prior to creating the Flask application
    db_uri = os.getenv('DB_URI')
    last_slash = db_uri.rfind('/')

    os.environ['DB_URI'] = db_uri[:last_slash] + '/point_of_sale_test'
    flask_app = create_app()
    flask_app.config.update({
        "TESTING": True,
    })

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            _create_all_schemas()
            db.create_all()
            db.session.add_all([RoleAccount(0, 'Admin'), RoleAccount(1, 'Seller')])
            db.session.add_all([UserAccount('admin', 'admin', 0, 1), UserAccount('seller', 'seller', 1, 1)])
            db.session.commit()

            yield testing_client  # this is where the testing happens!

            db.session.remove()
            db.drop_all()

@pytest.fixture(scope='module')
def admin_client(client: FlaskClient):
    user = UserAccount.query.filter_by(user_name = "admin").first()
    with client.session_transaction() as session:
        session["user_name"] = user.user_name
        session["user_role"] = user.user_role
        session["user_id"] = user.user_id

    yield client

    with client.session_transaction() as session:
        session.pop("user_name", None)
        session.pop("user_role", None)
        session.pop("user_id", None)

@pytest.fixture(scope='module')
def inv_client(admin_client: FlaskClient):
    products = [Product('Papa', 20, 5000), Product('Arroz', 15, 10000), Product('Chicle', 120, 2000)]
    db.session.add_all(products)
    db.session.commit()

    yield admin_client

    for p in products:
        db.session.delete(p)

    db.session.commit()


@pytest.fixture(scope='module')
def seller_client(client: FlaskClient):
    user = UserAccount.query.filter_by(user_name = "seller").first()
    with client.session_transaction() as session:
        session["user_name"] = user.user_name
        session["user_role"] = user.user_role
        session["user_id"] = user.user_id

    products = [Product('Papa', 20, 5000), Product('Arroz', 15, 10000), Product('Chicle', 120, 2000)]
    db.session.add_all(products)
    db.session.commit()

    yield client

    ProductSale.query.delete()

    for p in products:
        db.session.delete(p)

    db.session.commit()

    with client.session_transaction() as session:
        session.pop("user_name", None)
        session.pop("user_role", None)
        session.pop("user_id", None)
