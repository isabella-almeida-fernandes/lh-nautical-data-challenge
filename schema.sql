-- ==============================================
-- DDL SCHEMA GERADO AUTOMATICAMENTE - POSTGRESQL
-- Data de Geracao: 2026-08-14 15:05:52
-- ==============================================

DROP TABLE IF EXISTS addresses CASCADE;
CREATE TABLE addresses (
    id INTEGER,
    customer_id INTEGER,
    address_type VARCHAR(255),
    postal_code VARCHAR(255),
    street VARCHAR(255),
    number INTEGER,
    complement VARCHAR(255),
    district VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    country VARCHAR(255),
    is_primary BOOLEAN
);

DROP TABLE IF EXISTS attributes CASCADE;
CREATE TABLE attributes (
    id INTEGER,
    name VARCHAR(255),
    data_type VARCHAR(255)
);

DROP TABLE IF EXISTS brands CASCADE;
CREATE TABLE brands (
    id INTEGER,
    name VARCHAR(255),
    country VARCHAR(255),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

DROP TABLE IF EXISTS categories CASCADE;
CREATE TABLE categories (
    id INTEGER,
    name VARCHAR(255),
    slug VARCHAR(255),
    parent_category_id INTEGER,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

DROP TABLE IF EXISTS customers CASCADE;
CREATE TABLE customers (
    id INTEGER,
    person_type VARCHAR(255),
    legal_name VARCHAR(255),
    trade_name VARCHAR(255),
    tax_id INTEGER,
    state_registration VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(255),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

DROP TABLE IF EXISTS employees CASCADE;
CREATE TABLE employees (
    id INTEGER,
    full_name VARCHAR(255),
    cpf INTEGER,
    email VARCHAR(255),
    role VARCHAR(255),
    primary_location_id INTEGER,
    hire_date DATE,
    termination_date DATE,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

DROP TABLE IF EXISTS fiscal_invoices CASCADE;
CREATE TABLE fiscal_invoices (
    id INTEGER,
    order_id INTEGER,
    nfe_number VARCHAR(255),
    nfe_access_key INTEGER,
    series INTEGER,
    issued_at TIMESTAMP,
    status VARCHAR(255),
    total_amount NUMERIC(15, 2),
    xml_storage_uri VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

DROP TABLE IF EXISTS goods_receipt_items CASCADE;
CREATE TABLE goods_receipt_items (
    id INTEGER,
    goods_receipt_id INTEGER,
    purchase_order_item_id INTEGER,
    quantity_received NUMERIC(15, 2)
);

DROP TABLE IF EXISTS goods_receipts CASCADE;
CREATE TABLE goods_receipts (
    id INTEGER,
    purchase_order_id INTEGER,
    received_by_employee_id INTEGER,
    received_at TIMESTAMP,
    notes VARCHAR(255),
    created_at TIMESTAMP
);

DROP TABLE IF EXISTS locations CASCADE;
CREATE TABLE locations (
    id INTEGER,
    name VARCHAR(255),
    location_type VARCHAR(255),
    postal_code VARCHAR(255),
    street VARCHAR(255),
    number INTEGER,
    complement VARCHAR(255),
    district VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    country VARCHAR(255),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

DROP TABLE IF EXISTS order_items CASCADE;
CREATE TABLE order_items (
    id INTEGER,
    order_id INTEGER,
    product_variant_id INTEGER,
    quantity INTEGER,
    unit_price NUMERIC(15, 2),
    icms_rate NUMERIC(15, 2),
    ipi_rate NUMERIC(15, 2),
    line_total NUMERIC(15, 2)
);

DROP TABLE IF EXISTS orders CASCADE;
CREATE TABLE orders (
    id INTEGER,
    order_number VARCHAR(255),
    channel VARCHAR(255),
    customer_id INTEGER,
    salesperson_id INTEGER,
    location_id INTEGER,
    status VARCHAR(255),
    subtotal NUMERIC(15, 2),
    discount_amount NUMERIC(15, 2),
    total NUMERIC(15, 2),
    placed_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

DROP TABLE IF EXISTS payments CASCADE;
CREATE TABLE payments (
    id INTEGER,
    order_id INTEGER,
    method VARCHAR(255),
    installments INTEGER,
    amount NUMERIC(15, 2),
    status VARCHAR(255),
    paid_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

DROP TABLE IF EXISTS product_suppliers CASCADE;
CREATE TABLE product_suppliers (
    product_variant_id INTEGER,
    supplier_id INTEGER,
    supplier_sku VARCHAR(255),
    last_quoted_cost NUMERIC(15, 2),
    lead_time_days INTEGER,
    is_preferred BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

DROP TABLE IF EXISTS product_variants CASCADE;
CREATE TABLE product_variants (
    id INTEGER,
    product_id INTEGER,
    sku VARCHAR(255),
    barcode_ean INTEGER,
    sale_price NUMERIC(15, 2),
    cost_price NUMERIC(15, 2),
    weight_kg NUMERIC(15, 2),
    icms_rate NUMERIC(15, 2),
    ipi_rate NUMERIC(15, 2),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

DROP TABLE IF EXISTS products CASCADE;
CREATE TABLE products (
    id INTEGER,
    name VARCHAR(255),
    description VARCHAR(255),
    brand_id INTEGER,
    category_id INTEGER,
    ncm_code INTEGER,
    unit_of_measure VARCHAR(255),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

DROP TABLE IF EXISTS purchase_order_items CASCADE;
CREATE TABLE purchase_order_items (
    id INTEGER,
    purchase_order_id INTEGER,
    product_variant_id INTEGER,
    quantity_ordered INTEGER,
    unit_cost NUMERIC(15, 2),
    line_total NUMERIC(15, 2)
);

DROP TABLE IF EXISTS purchase_orders CASCADE;
CREATE TABLE purchase_orders (
    id INTEGER,
    po_number VARCHAR(255),
    supplier_id INTEGER,
    buyer_id INTEGER,
    destination_location_id INTEGER,
    status VARCHAR(255),
    currency VARCHAR(255),
    subtotal NUMERIC(15, 2),
    total NUMERIC(15, 2),
    placed_at TIMESTAMP,
    expected_delivery_at DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

DROP TABLE IF EXISTS return_items CASCADE;
CREATE TABLE return_items (
    id INTEGER,
    return_id INTEGER,
    order_item_id INTEGER,
    quantity NUMERIC(15, 2),
    action VARCHAR(255),
    exchange_variant_id INTEGER,
    unit_refund_amount NUMERIC(15, 2)
);

DROP TABLE IF EXISTS returns CASCADE;
CREATE TABLE returns (
    id INTEGER,
    return_number VARCHAR(255),
    order_id INTEGER,
    customer_id INTEGER,
    received_at_location_id INTEGER,
    status VARCHAR(255),
    reason VARCHAR(255),
    total_refund_amount NUMERIC(15, 2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

DROP TABLE IF EXISTS stock_levels CASCADE;
CREATE TABLE stock_levels (
    product_variant_id INTEGER,
    location_id INTEGER,
    quantity_on_hand NUMERIC(15, 2),
    reorder_point VARCHAR(255),
    updated_at TIMESTAMP
);

DROP TABLE IF EXISTS stock_movements CASCADE;
CREATE TABLE stock_movements (
    id INTEGER,
    product_variant_id INTEGER,
    location_id INTEGER,
    movement_type VARCHAR(255),
    quantity NUMERIC(15, 2),
    reference_table VARCHAR(255),
    reference_id INTEGER,
    employee_id INTEGER,
    notes VARCHAR(255),
    occurred_at TIMESTAMP,
    created_at TIMESTAMP
);

DROP TABLE IF EXISTS suppliers CASCADE;
CREATE TABLE suppliers (
    id INTEGER,
    legal_name VARCHAR(255),
    trade_name VARCHAR(255),
    country VARCHAR(255),
    tax_id VARCHAR(255),
    tax_id_type VARCHAR(255),
    email VARCHAR(255),
    phone INTEGER,
    contact_name VARCHAR(255),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

DROP TABLE IF EXISTS variant_attribute_values CASCADE;
CREATE TABLE variant_attribute_values (
    product_variant_id INTEGER,
    attribute_id INTEGER,
    value VARCHAR(255)
);

