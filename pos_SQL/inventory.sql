CREATE TABLE IF NOT EXISTS inventory.product(
    product_id SERIAL PRIMARY KEY,
    product_name TEXT NOT NULL,
    product_amount INTEGER,
    product_price FLOAT
    product_state INT
);

