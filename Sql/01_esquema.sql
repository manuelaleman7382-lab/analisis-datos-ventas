-- =====================================================================
-- Esquema de la base de datos Superstore (SQLite)
-- Modelo: 5 tablas relacionadas
--   regions (1) --- (N) orders (1) --- (N) order_items (N) --- (1) products
--   customers (1) --- (N) orders
-- =====================================================================

-- Se borran primero las tablas hijas, para poder volver a ejecutar el script.
DROP VIEW  IF EXISTS vw_pedidos;
DROP VIEW  IF EXISTS vw_ventas;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS regions;

CREATE TABLE regions (
    region            TEXT PRIMARY KEY,
    regional_manager  TEXT NOT NULL
);

CREATE TABLE customers (
    customer_id    TEXT PRIMARY KEY,
    customer_name  TEXT NOT NULL,
    segment        TEXT NOT NULL CHECK (segment IN ('Consumer', 'Corporate', 'Home Office'))
);

CREATE TABLE products (
    product_id    TEXT PRIMARY KEY,
    product_name  TEXT NOT NULL,
    category      TEXT NOT NULL,
    sub_category  TEXT NOT NULL
);

-- order_key es una llave propia: algunos order_id se repiten con clientes distintos.
-- Las fechas se guardan como texto ISO (AAAA-MM-DD), que SQLite compara y ordena bien.
CREATE TABLE orders (
    order_key       INTEGER PRIMARY KEY,
    order_id        TEXT    NOT NULL,
    customer_id     TEXT    NOT NULL REFERENCES customers (customer_id),
    order_date      TEXT    NOT NULL,
    ship_date       TEXT    NOT NULL,
    ship_mode       TEXT    NOT NULL CHECK (ship_mode IN ('Standard Class', 'Second Class', 'First Class', 'Same Day')),
    country_region  TEXT    NOT NULL,
    city            TEXT    NOT NULL,
    state_province  TEXT    NOT NULL,
    postal_code     TEXT    NOT NULL,
    region          TEXT    NOT NULL REFERENCES regions (region),
    is_returned     INTEGER NOT NULL DEFAULT 0 CHECK (is_returned IN (0, 1)),
    UNIQUE (order_id, customer_id),
    CHECK (ship_date >= order_date)
);

CREATE TABLE order_items (
    row_id       INTEGER PRIMARY KEY,
    order_key    INTEGER NOT NULL REFERENCES orders (order_key),
    product_id   TEXT    NOT NULL REFERENCES products (product_id),
    sales        REAL    NOT NULL CHECK (sales > 0),
    quantity     INTEGER NOT NULL CHECK (quantity > 0),
    discount     REAL    NOT NULL CHECK (discount >= 0 AND discount <= 1),
    profit       REAL    NOT NULL
);

-- Índices en las columnas que se usan para unir y filtrar
CREATE INDEX idx_orders_customer    ON orders (customer_id);
CREATE INDEX idx_orders_order_date  ON orders (order_date);
CREATE INDEX idx_orders_region      ON orders (region);
CREATE INDEX idx_items_order        ON order_items (order_key);
CREATE INDEX idx_items_product      ON order_items (product_id);
