-- ============================================
-- AskSQL — Northwind Database Schema
-- A realistic business database for text-to-SQL demos
-- ============================================

-- Drop existing tables (in dependency order)
DROP TABLE IF EXISTS order_details CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS shippers CASCADE;

-- ============================================
-- Categories: Product categories
-- ============================================
CREATE TABLE categories (
    category_id   SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description   TEXT
);

-- ============================================
-- Customers: Companies that buy products
-- ============================================
CREATE TABLE customers (
    customer_id   VARCHAR(10) PRIMARY KEY,
    company_name  VARCHAR(100) NOT NULL,
    contact_name  VARCHAR(100),
    contact_title VARCHAR(50),
    address       VARCHAR(200),
    city          VARCHAR(100),
    region        VARCHAR(50),
    postal_code   VARCHAR(20),
    country       VARCHAR(100),
    phone         VARCHAR(30),
    fax           VARCHAR(30)
);

-- ============================================
-- Employees: Sales representatives
-- ============================================
CREATE TABLE employees (
    employee_id  SERIAL PRIMARY KEY,
    last_name    VARCHAR(100) NOT NULL,
    first_name   VARCHAR(100) NOT NULL,
    title        VARCHAR(100),
    birth_date   DATE,
    hire_date    DATE,
    address      VARCHAR(200),
    city         VARCHAR(100),
    region       VARCHAR(50),
    postal_code  VARCHAR(20),
    country      VARCHAR(100),
    phone        VARCHAR(30),
    reports_to   INTEGER REFERENCES employees(employee_id)
);

-- ============================================
-- Suppliers: Companies that supply products
-- ============================================
CREATE TABLE suppliers (
    supplier_id   SERIAL PRIMARY KEY,
    company_name  VARCHAR(100) NOT NULL,
    contact_name  VARCHAR(100),
    contact_title VARCHAR(50),
    address       VARCHAR(200),
    city          VARCHAR(100),
    region        VARCHAR(50),
    postal_code   VARCHAR(20),
    country       VARCHAR(100),
    phone         VARCHAR(30),
    fax           VARCHAR(30),
    homepage      TEXT
);

-- ============================================
-- Shippers: Delivery companies
-- ============================================
CREATE TABLE shippers (
    shipper_id   SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    phone        VARCHAR(30)
);

-- ============================================
-- Products: Items available for sale
-- ============================================
CREATE TABLE products (
    product_id        SERIAL PRIMARY KEY,
    product_name      VARCHAR(100) NOT NULL,
    supplier_id       INTEGER REFERENCES suppliers(supplier_id),
    category_id       INTEGER REFERENCES categories(category_id),
    quantity_per_unit  VARCHAR(50),
    unit_price        NUMERIC(10, 2) DEFAULT 0,
    units_in_stock    INTEGER DEFAULT 0,
    units_on_order    INTEGER DEFAULT 0,
    reorder_level     INTEGER DEFAULT 0,
    discontinued      BOOLEAN DEFAULT FALSE
);

-- ============================================
-- Orders: Customer purchases
-- ============================================
CREATE TABLE orders (
    order_id       SERIAL PRIMARY KEY,
    customer_id    VARCHAR(10) REFERENCES customers(customer_id),
    employee_id    INTEGER REFERENCES employees(employee_id),
    order_date     DATE,
    required_date  DATE,
    shipped_date   DATE,
    shipper_id     INTEGER REFERENCES shippers(shipper_id),
    freight        NUMERIC(10, 2) DEFAULT 0,
    ship_name      VARCHAR(100),
    ship_address   VARCHAR(200),
    ship_city      VARCHAR(100),
    ship_region    VARCHAR(50),
    ship_postal_code VARCHAR(20),
    ship_country   VARCHAR(100)
);

-- ============================================
-- Order Details: Line items in each order
-- ============================================
CREATE TABLE order_details (
    order_id   INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    unit_price NUMERIC(10, 2) NOT NULL,
    quantity   INTEGER NOT NULL DEFAULT 1,
    discount   NUMERIC(4, 2) DEFAULT 0,
    PRIMARY KEY (order_id, product_id)
);

-- ============================================
-- Indexes for performance
-- ============================================
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_employee ON orders(employee_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_supplier ON products(supplier_id);
CREATE INDEX idx_order_details_product ON order_details(product_id);
