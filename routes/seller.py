from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from utils.db import db
from models.sale import Sale
from models.product_sale import ProductSale
from sqlalchemy import text
from uuid import uuid4

seller = Blueprint("seller", __name__, static_folder="static", template_folder="templates")

class DataError(Exception):
    pass

@seller.before_request
def before_request():
    if not "user_name" in session or session["user_role"] != 1:
        return redirect(url_for("login"))
    
@seller.route('/')
def home():
    return render_template("seller.jinja")

@seller.route('/add_sale')
def add_sale():
    return render_template("add_sale.jinja")

@seller.route('/process_sale', methods=['POST'])
def process_sale():
    str_ids = request.form.getlist("product_id[]")
    str_amounts = request.form.getlist("amount[]")
    amounts: list[int] = []
    client_id = request.form.get("client_id")

    try:
        if client_id is None or client_id.isspace() or not client_id.isalnum():
            raise DataError("ID del cliente invalido")

        if len(str_ids) == 0:
            raise DataError("No se ingresaron productos.")

        # Check for valid values
        for product_id, amount in zip(str_ids, str_amounts):
            if not product_id.isnumeric():
                raise DataError("El ID de un producto no puede ser vacio.")
            
            elif not amount.isnumeric():
                raise DataError("Las cantidades deben ser enteros positivos mayores a 0.")
            
            amounts.append(int(amount))
        
        # Get all products with the user provided IDs
        values = ','.join(str_ids)
        query = text(f'SELECT * FROM inventory.product WHERE product_id IN ({values})')
        result = db.session.execute(query).all()

        # If missing IDS, an invalid ID was inserted
        if len(result) != len(str_ids):
            for i in str_ids:
                if i not in result:
                    raise DataError(f"ID de producto invalido: {i}")

        # tuple (id, amount)
        form_data = list(map(lambda x: (int(x[0]), x[1]), list(zip(str_ids, amounts))))
        form_data.sort(key=lambda x: x[0])

        # Calculate sale price and check for valid amount
        total_price = 0
        sale_products: list[ProductSale] = []
        sale_id = uuid4()
        for row, data in zip(result, form_data):
            if row.product_amount < data[1]:
                raise DataError(f"La cantidad comprada de {row.product_name} excede el inventario.\
                                Cantidad Disponible: ({row.product_amount}).")
                
            total_price += row.product_price * data[1]
            sale_products.append(ProductSale(sale_id=sale_id, product_id=row.product_id, amount=data[1]))

        sale = Sale(sale_id, total_price, session["user_id"], client_id)
        db.session.add(sale)
        db.session.commit()
        db.session.add_all(sale_products)
        db.session.commit()
        
        flash("Venta exitosa")

    except DataError as e:
        flash(str(e))

    except Exception as e:
        flash("Ha ocurrido un error inesperado.")
        print(e)

    return redirect(url_for("seller.add_sale"))