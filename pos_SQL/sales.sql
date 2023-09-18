CREATE TABLE IF NOT EXISTS sales.sale(
    sale_id UUID PRIMARY KEY,
    sale_price FLOAT,
    seller_id UUID NOT NULL,
    client_id TEXT,
    CONSTRAINT fk_seller_id FOREIGN KEY (seller_id) REFERENCES account.user_account(user_id)
);

CREATE TABLE IF NOT EXISTS sales.product_sale(
    sale_id UUID NOT NULL,
    product_id INTEGER NOT NULL,
    amount INTEGER,
    CONSTRAINT pk_sale_product PRIMARY KEY (sale_id, product_id),
    CONSTRAINT fk_sale_id FOREIGN KEY (sale_id) REFERENCES sales.sale(sale_id),
    CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES inventory.product(product_id)
);
