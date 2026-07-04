-- ============================================
-- AskSQL — Northwind Sample Data
-- Realistic business data for text-to-SQL demos
-- ============================================

-- Categories
INSERT INTO categories (category_name, description) VALUES
('Beverages', 'Soft drinks, coffees, teas, beers, and ales'),
('Condiments', 'Sweet and savory sauces, relishes, spreads, and seasonings'),
('Confections', 'Desserts, candies, and sweet breads'),
('Dairy Products', 'Cheeses and milk-based products'),
('Grains/Cereals', 'Breads, crackers, pasta, and cereal'),
('Meat/Poultry', 'Prepared meats and poultry products'),
('Produce', 'Dried fruit, vegetables, and bean curd'),
('Seafood', 'Seaweed, fish, and shellfish');

-- Suppliers
INSERT INTO suppliers (company_name, contact_name, contact_title, city, country, phone) VALUES
('Exotic Liquids', 'Charlotte Cooper', 'Purchasing Manager', 'London', 'UK', '(171) 555-2222'),
('New Orleans Cajun Delights', 'Shelley Burke', 'Order Administrator', 'New Orleans', 'USA', '(100) 555-4822'),
('Grandma Kelly''s Homestead', 'Regina Murphy', 'Sales Representative', 'Ann Arbor', 'USA', '(313) 555-5735'),
('Tokyo Traders', 'Yoshi Nagase', 'Marketing Manager', 'Tokyo', 'Japan', '(03) 3555-5011'),
('Cooperativa de Quesos Las Cabras', 'Antonio del Valle Saavedra', 'Export Administrator', 'Oviedo', 'Spain', '(98) 598 76 54'),
('Mayumi''s', 'Mayumi Ohno', 'Marketing Representative', 'Osaka', 'Japan', '(06) 431-7877'),
('Pavlova Ltd.', 'Ian Devling', 'Marketing Manager', 'Melbourne', 'Australia', '(03) 444-2343'),
('Specialty Biscuits Ltd.', 'Peter Wilson', 'Sales Representative', 'Manchester', 'UK', '(161) 555-4448'),
('PB Knäckebröd AB', 'Lars Peterson', 'Sales Agent', 'Göteborg', 'Sweden', '031-987 65 43'),
('Formaggi Fortini s.r.l.', 'Elio Rossi', 'Sales Representative', 'Ravenna', 'Italy', '(0544) 60323');

-- Shippers
INSERT INTO shippers (company_name, phone) VALUES
('Speedy Express', '(503) 555-9831'),
('United Package', '(503) 555-3199'),
('Federal Shipping', '(503) 555-9931');

-- Employees
INSERT INTO employees (last_name, first_name, title, birth_date, hire_date, city, country, phone) VALUES
('Davolio', 'Nancy', 'Sales Representative', '1968-12-08', '2022-05-01', 'Seattle', 'USA', '(206) 555-9857'),
('Fuller', 'Andrew', 'Vice President Sales', '1962-02-19', '2020-08-14', 'Tacoma', 'USA', '(206) 555-9482'),
('Leverling', 'Janet', 'Sales Representative', '1973-08-30', '2022-04-01', 'Kirkland', 'USA', '(206) 555-3412'),
('Peacock', 'Margaret', 'Sales Representative', '1957-09-19', '2021-05-03', 'Redmond', 'USA', '(206) 555-8122'),
('Buchanan', 'Steven', 'Sales Manager', '1965-03-04', '2021-10-17', 'London', 'UK', '(71) 555-4848'),
('Suyama', 'Michael', 'Sales Representative', '1983-07-02', '2023-10-17', 'London', 'UK', '(71) 555-7773'),
('King', 'Robert', 'Sales Representative', '1980-05-29', '2024-01-02', 'London', 'UK', '(71) 555-5598'),
('Callahan', 'Laura', 'Inside Sales Coordinator', '1978-01-09', '2024-03-05', 'Seattle', 'USA', '(206) 555-1189'),
('Dodsworth', 'Anne', 'Sales Representative', '1986-01-27', '2024-11-15', 'London', 'UK', '(71) 555-4444');

-- Update reports_to
UPDATE employees SET reports_to = 2 WHERE employee_id IN (1, 3, 4, 5, 8);
UPDATE employees SET reports_to = 5 WHERE employee_id IN (6, 7, 9);

-- Customers
INSERT INTO customers (customer_id, company_name, contact_name, contact_title, city, region, country, phone) VALUES
('ALFKI', 'Alfreds Futterkiste', 'Maria Anders', 'Sales Representative', 'Berlin', NULL, 'Germany', '030-0074321'),
('ANATR', 'Ana Trujillo Emparedados', 'Ana Trujillo', 'Owner', 'México D.F.', NULL, 'Mexico', '(5) 555-4729'),
('ANTON', 'Antonio Moreno Taquería', 'Antonio Moreno', 'Owner', 'México D.F.', NULL, 'Mexico', '(5) 555-3932'),
('AROUT', 'Around the Horn', 'Thomas Hardy', 'Sales Representative', 'London', NULL, 'UK', '(171) 555-7788'),
('BERGS', 'Berglunds snabbköp', 'Christina Berglund', 'Order Administrator', 'Luleå', NULL, 'Sweden', '0921-12 34 65'),
('BLAUS', 'Blauer See Delikatessen', 'Hanna Moos', 'Sales Representative', 'Mannheim', NULL, 'Germany', '0621-08460'),
('BLONP', 'Blondel père et fils', 'Frédérique Citeaux', 'Marketing Manager', 'Strasbourg', NULL, 'France', '88.60.15.31'),
('BOLID', 'Bólido Comidas preparadas', 'Martín Sommer', 'Owner', 'Madrid', NULL, 'Spain', '(91) 555 22 82'),
('BONAP', 'Bon app''', 'Laurence Lebihan', 'Owner', 'Marseille', NULL, 'France', '91.24.45.40'),
('BOTTM', 'Bottom-Dollar Markets', 'Elizabeth Lincoln', 'Accounting Manager', 'Tsawwassen', 'BC', 'Canada', '(604) 555-4729'),
('BSBEV', 'B''s Beverages', 'Victoria Ashworth', 'Sales Representative', 'London', NULL, 'UK', '(171) 555-1212'),
('CACTU', 'Cactus Comidas para llevar', 'Patricio Simpson', 'Sales Agent', 'Buenos Aires', NULL, 'Argentina', '(1) 135-5555'),
('CHOPS', 'Chop-suey Chinese', 'Yang Wang', 'Owner', 'Bern', NULL, 'Switzerland', '0452-076545'),
('COMMI', 'Comércio Mineiro', 'Pedro Afonso', 'Sales Associate', 'São Paulo', 'SP', 'Brazil', '(11) 555-7647'),
('CONSH', 'Consolidated Holdings', 'Elizabeth Brown', 'Sales Representative', 'London', NULL, 'UK', '(171) 555-2282'),
('DRACD', 'Drachenblut Delikatessen', 'Sven Ottlieb', 'Order Administrator', 'Aachen', NULL, 'Germany', '0241-039123'),
('DUMON', 'Du monde entier', 'Janine Labrune', 'Owner', 'Nantes', NULL, 'France', '40.67.88.88'),
('EASTC', 'Eastern Connection', 'Ann Devon', 'Sales Agent', 'London', NULL, 'UK', '(171) 555-0297'),
('ERNSH', 'Ernst Handel', 'Roland Mendel', 'Sales Manager', 'Graz', NULL, 'Austria', '7675-3425'),
('FAMIA', 'Familia Arquibaldo', 'Aria Cruz', 'Marketing Assistant', 'São Paulo', 'SP', 'Brazil', '(11) 555-9857'),
('FOLIG', 'Folies gourmandes', 'Martine Rancé', 'Assistant Sales Agent', 'Lille', NULL, 'France', '20.16.10.16'),
('FRANK', 'Frankenversand', 'Peter Franken', 'Marketing Manager', 'München', NULL, 'Germany', '089-0877310'),
('FRANR', 'France restauration', 'Carine Schmitt', 'Marketing Manager', 'Nantes', NULL, 'France', '40.32.21.21'),
('GALED', 'Galería del gastrónomo', 'Eduardo Saavedra', 'Marketing Manager', 'Barcelona', NULL, 'Spain', '(93) 203 4560'),
('GOURL', 'Gourmet Lanchonetes', 'André Fonseca', 'Sales Associate', 'Campinas', 'SP', 'Brazil', '(11) 555-9482'),
('GREAL', 'Great Lakes Food Market', 'Howard Snyder', 'Marketing Manager', 'Eugene', 'OR', 'USA', '(503) 555-7555'),
('HANAR', 'Hanari Carnes', 'Mario Pontes', 'Accounting Manager', 'Rio de Janeiro', 'RJ', 'Brazil', '(21) 555-0091'),
('HILAA', 'HILARIÓN-Abastos', 'Carlos Hernández', 'Sales Representative', 'San Cristóbal', 'Táchira', 'Venezuela', '(5) 555-1340'),
('HUNGC', 'Hungry Coyote Import Store', 'Yoshi Latimer', 'Sales Representative', 'Elgin', 'OR', 'USA', '(503) 555-6874'),
('ISLAT', 'Island Trading', 'Helen Bennett', 'Marketing Manager', 'Cowes', NULL, 'UK', '(198) 555-8888');

-- Products
INSERT INTO products (product_name, supplier_id, category_id, quantity_per_unit, unit_price, units_in_stock, units_on_order, reorder_level, discontinued) VALUES
('Chai', 1, 1, '10 boxes x 20 bags', 18.00, 39, 0, 10, false),
('Chang', 1, 1, '24 - 12 oz bottles', 19.00, 17, 40, 25, false),
('Aniseed Syrup', 1, 2, '12 - 550 ml bottles', 10.00, 13, 70, 25, false),
('Chef Anton''s Cajun Seasoning', 2, 2, '48 - 6 oz jars', 22.00, 53, 0, 0, false),
('Chef Anton''s Gumbo Mix', 2, 2, '36 boxes', 21.35, 0, 0, 0, true),
('Grandma''s Boysenberry Spread', 3, 2, '12 - 8 oz jars', 25.00, 120, 0, 25, false),
('Uncle Bob''s Organic Dried Pears', 3, 7, '12 - 1 lb pkgs.', 30.00, 15, 0, 10, false),
('Northwoods Cranberry Sauce', 3, 2, '12 - 12 oz jars', 40.00, 6, 0, 0, false),
('Mishi Kobe Niku', 4, 6, '18 - 500 g pkgs.', 97.00, 29, 0, 0, true),
('Ikura', 4, 8, '12 - 200 ml jars', 31.00, 31, 0, 0, false),
('Queso Cabrales', 5, 4, '1 kg pkg.', 21.00, 22, 30, 30, false),
('Queso Manchego La Pastora', 5, 4, '10 - 500 g pkgs.', 38.00, 86, 0, 0, false),
('Konbu', 6, 8, '2 kg box', 6.00, 24, 0, 5, false),
('Tofu', 6, 7, '40 - 100 g pkgs.', 23.25, 35, 0, 0, false),
('Genen Shouyu', 6, 2, '24 - 250 ml bottles', 15.50, 39, 0, 5, false),
('Pavlova', 7, 3, '32 - 500 g boxes', 17.45, 29, 0, 10, false),
('Alice Mutton', 7, 6, '20 - 1 kg tins', 39.00, 0, 0, 0, true),
('Carnarvon Tigers', 7, 8, '16 kg pkg.', 62.50, 42, 0, 0, false),
('Teatime Chocolate Biscuits', 8, 3, '10 boxes x 12 pieces', 9.20, 25, 0, 5, false),
('Sir Rodney''s Marmalade', 8, 3, '30 gift boxes', 81.00, 40, 0, 0, false),
('Sir Rodney''s Scones', 8, 3, '24 pkgs. x 4 pieces', 10.00, 3, 40, 5, false),
('Gustaf''s Knäckebröd', 9, 5, '24 - 500 g pkgs.', 21.00, 104, 0, 25, false),
('Tunnbröd', 9, 5, '12 - 250 g pkgs.', 9.00, 61, 0, 25, false),
('Guaraná Fantástica', 10, 1, '12 - 355 ml cans', 4.50, 20, 0, 0, true),
('NuNuCa Nuß-Nougat-Creme', 10, 3, '20 - 450 g glasses', 14.00, 76, 0, 30, false);

-- Orders (spanning multiple months for interesting date queries)
INSERT INTO orders (customer_id, employee_id, order_date, required_date, shipped_date, shipper_id, freight, ship_name, ship_city, ship_country) VALUES
('ALFKI', 1, '2025-07-04', '2025-08-01', '2025-07-16', 1, 32.38, 'Alfreds Futterkiste', 'Berlin', 'Germany'),
('ALFKI', 3, '2025-08-25', '2025-09-22', '2025-09-02', 2, 11.61, 'Alfreds Futterkiste', 'Berlin', 'Germany'),
('ANATR', 2, '2025-07-08', '2025-08-05', '2025-07-15', 1, 65.83, 'Ana Trujillo Emparedados', 'México D.F.', 'Mexico'),
('ANTON', 4, '2025-08-12', '2025-09-09', '2025-08-20', 2, 41.34, 'Antonio Moreno Taquería', 'México D.F.', 'Mexico'),
('AROUT', 1, '2025-09-15', '2025-10-13', '2025-09-25', 3, 25.36, 'Around the Horn', 'London', 'UK'),
('BERGS', 3, '2025-07-22', '2025-08-19', '2025-07-30', 1, 122.46, 'Berglunds snabbköp', 'Luleå', 'Sweden'),
('BLAUS', 5, '2025-08-05', '2025-09-02', '2025-08-12', 2, 69.53, 'Blauer See Delikatessen', 'Mannheim', 'Germany'),
('BLONP', 6, '2025-09-20', '2025-10-18', '2025-09-28', 1, 55.09, 'Blondel père et fils', 'Strasbourg', 'France'),
('BOLID', 7, '2025-10-01', '2025-10-29', '2025-10-08', 3, 22.98, 'Bólido Comidas preparadas', 'Madrid', 'Spain'),
('BONAP', 2, '2025-07-15', '2025-08-12', '2025-07-21', 2, 96.72, 'Bon app''', 'Marseille', 'France'),
('BOTTM', 4, '2025-08-30', '2025-09-27', '2025-09-06', 1, 43.90, 'Bottom-Dollar Markets', 'Tsawwassen', 'Canada'),
('BSBEV', 1, '2025-09-10', '2025-10-08', '2025-09-18', 3, 14.01, 'B''s Beverages', 'London', 'UK'),
('CACTU', 3, '2025-10-05', '2025-11-02', '2025-10-14', 2, 33.27, 'Cactus Comidas para llevar', 'Buenos Aires', 'Argentina'),
('CHOPS', 5, '2025-07-30', '2025-08-27', '2025-08-07', 1, 87.09, 'Chop-suey Chinese', 'Bern', 'Switzerland'),
('COMMI', 8, '2025-08-18', '2025-09-15', '2025-08-25', 2, 28.45, 'Comércio Mineiro', 'São Paulo', 'Brazil'),
('CONSH', 6, '2025-09-25', '2025-10-23', '2025-10-02', 3, 9.76, 'Consolidated Holdings', 'London', 'UK'),
('DRACD', 9, '2025-10-10', '2025-11-07', '2025-10-18', 1, 48.29, 'Drachenblut Delikatessen', 'Aachen', 'Germany'),
('DUMON', 7, '2025-07-12', '2025-08-09', '2025-07-19', 2, 76.56, 'Du monde entier', 'Nantes', 'France'),
('EASTC', 4, '2025-08-22', '2025-09-19', '2025-08-29', 1, 12.34, 'Eastern Connection', 'London', 'UK'),
('ERNSH', 1, '2025-09-05', '2025-10-03', '2025-09-12', 3, 140.51, 'Ernst Handel', 'Graz', 'Austria'),
('FAMIA', 2, '2025-10-15', '2025-11-12', '2025-10-22', 2, 58.43, 'Familia Arquibaldo', 'São Paulo', 'Brazil'),
('FOLIG', 3, '2025-07-18', '2025-08-15', '2025-07-26', 1, 31.29, 'Folies gourmandes', 'Lille', 'France'),
('FRANK', 5, '2025-08-10', '2025-09-07', '2025-08-17', 2, 89.00, 'Frankenversand', 'München', 'Germany'),
('GALED', 8, '2025-09-28', '2025-10-26', '2025-10-05', 3, 18.40, 'Galería del gastrónomo', 'Barcelona', 'Spain'),
('GREAL', 6, '2025-10-20', '2025-11-17', '2025-10-28', 1, 105.65, 'Great Lakes Food Market', 'Eugene', 'USA'),
('HANAR', 9, '2025-07-25', '2025-08-22', '2025-08-01', 2, 45.97, 'Hanari Carnes', 'Rio de Janeiro', 'Brazil'),
('HILAA', 4, '2025-08-15', '2025-09-12', '2025-08-22', 1, 73.21, 'HILARIÓN-Abastos', 'San Cristóbal', 'Venezuela'),
('HUNGC', 7, '2025-09-18', '2025-10-16', '2025-09-25', 3, 19.55, 'Hungry Coyote Import Store', 'Elgin', 'USA'),
('ISLAT', 1, '2025-10-25', '2025-11-22', '2025-11-01', 2, 37.22, 'Island Trading', 'Cowes', 'UK'),
('ALFKI', 2, '2025-10-30', '2025-11-27', '2025-11-06', 1, 29.46, 'Alfreds Futterkiste', 'Berlin', 'Germany'),
('ERNSH', 5, '2025-11-02', '2025-11-30', NULL, 3, 154.20, 'Ernst Handel', 'Graz', 'Austria'),
('FRANK', 3, '2025-11-05', '2025-12-03', NULL, 1, 67.88, 'Frankenversand', 'München', 'Germany'),
('BONAP', 8, '2025-11-08', '2025-12-06', NULL, 2, 82.15, 'Bon app''', 'Marseille', 'France'),
('GREAL', 4, '2025-11-10', '2025-12-08', NULL, 3, 93.44, 'Great Lakes Food Market', 'Eugene', 'USA'),
('BLAUS', 1, '2025-11-12', '2025-12-10', NULL, 1, 44.67, 'Blauer See Delikatessen', 'Mannheim', 'Germany');

-- Order Details (line items — creating realistic revenue data)
INSERT INTO order_details (order_id, product_id, unit_price, quantity, discount) VALUES
-- Order 1 (ALFKI)
(1, 1, 18.00, 12, 0.00),
(1, 2, 19.00, 10, 0.05),
(1, 16, 17.45, 5, 0.00),
-- Order 2 (ALFKI)
(2, 4, 22.00, 6, 0.10),
(2, 14, 23.25, 3, 0.00),
-- Order 3 (ANATR)
(3, 3, 10.00, 24, 0.00),
(3, 6, 25.00, 6, 0.05),
(3, 20, 81.00, 2, 0.00),
-- Order 4 (ANTON)
(4, 9, 97.00, 3, 0.00),
(4, 10, 31.00, 15, 0.10),
(4, 18, 62.50, 4, 0.00),
-- Order 5 (AROUT)
(5, 1, 18.00, 20, 0.00),
(5, 11, 21.00, 8, 0.05),
-- Order 6 (BERGS)
(6, 12, 38.00, 10, 0.00),
(6, 22, 21.00, 40, 0.10),
(6, 25, 14.00, 20, 0.00),
-- Order 7 (BLAUS)
(7, 7, 30.00, 8, 0.00),
(7, 15, 15.50, 12, 0.05),
(7, 23, 9.00, 25, 0.00),
-- Order 8 (BLONP)
(8, 5, 21.35, 6, 0.00),
(8, 16, 17.45, 15, 0.00),
-- Order 9 (BOLID)
(9, 4, 22.00, 20, 0.10),
(9, 8, 40.00, 5, 0.00),
-- Order 10 (BONAP)
(10, 2, 19.00, 30, 0.00),
(10, 13, 6.00, 50, 0.15),
(10, 19, 9.20, 40, 0.00),
-- Order 11 (BOTTM)
(11, 20, 81.00, 3, 0.00),
(11, 21, 10.00, 10, 0.00),
-- Order 12 (BSBEV)
(12, 1, 18.00, 15, 0.05),
(12, 24, 4.50, 30, 0.00),
-- Order 13 (CACTU)
(13, 3, 10.00, 18, 0.00),
(13, 14, 23.25, 8, 0.10),
-- Order 14 (CHOPS)
(14, 9, 97.00, 5, 0.00),
(14, 17, 39.00, 10, 0.05),
(14, 22, 21.00, 20, 0.00),
-- Order 15 (COMMI)
(15, 6, 25.00, 12, 0.00),
(15, 10, 31.00, 6, 0.00),
-- Order 16 (CONSH)
(16, 11, 21.00, 5, 0.00),
(16, 25, 14.00, 15, 0.10),
-- Order 17 (DRACD)
(17, 7, 30.00, 14, 0.00),
(17, 12, 38.00, 8, 0.05),
-- Order 18 (DUMON)
(18, 18, 62.50, 6, 0.00),
(18, 20, 81.00, 4, 0.10),
-- Order 19 (EASTC)
(19, 15, 15.50, 20, 0.00),
(19, 23, 9.00, 30, 0.00),
-- Order 20 (ERNSH)
(20, 9, 97.00, 8, 0.00),
(20, 4, 22.00, 30, 0.05),
(20, 18, 62.50, 10, 0.00),
-- Order 21 (FAMIA)
(21, 2, 19.00, 20, 0.10),
(21, 16, 17.45, 12, 0.00),
-- Order 22 (FOLIG)
(22, 1, 18.00, 25, 0.00),
(22, 8, 40.00, 8, 0.05),
-- Order 23 (FRANK)
(23, 3, 10.00, 40, 0.00),
(23, 13, 6.00, 60, 0.10),
(23, 21, 10.00, 20, 0.00),
-- Order 24 (GALED)
(24, 5, 21.35, 10, 0.00),
(24, 19, 9.20, 25, 0.05),
-- Order 25 (GREAL)
(25, 14, 23.25, 15, 0.00),
(25, 22, 21.00, 30, 0.10),
(25, 25, 14.00, 40, 0.00),
-- Order 26 (HANAR)
(26, 6, 25.00, 20, 0.00),
(26, 10, 31.00, 10, 0.05),
-- Order 27 (HILAA)
(27, 17, 39.00, 12, 0.00),
(27, 4, 22.00, 15, 0.10),
-- Order 28 (HUNGC)
(28, 12, 38.00, 6, 0.00),
(28, 15, 15.50, 18, 0.00),
-- Order 29 (ISLAT)
(29, 2, 19.00, 14, 0.05),
(29, 20, 81.00, 3, 0.00),
-- Order 30 (ALFKI, repeat customer)
(30, 1, 18.00, 8, 0.00),
(30, 7, 30.00, 5, 0.10),
-- Order 31 (ERNSH, pending)
(31, 9, 97.00, 10, 0.00),
(31, 18, 62.50, 8, 0.05),
-- Order 32 (FRANK, pending)
(32, 22, 21.00, 25, 0.00),
(32, 3, 10.00, 50, 0.10),
-- Order 33 (BONAP, pending)
(33, 6, 25.00, 15, 0.00),
(33, 8, 40.00, 10, 0.05),
(33, 16, 17.45, 20, 0.00),
-- Order 34 (GREAL, pending)
(34, 14, 23.25, 20, 0.00),
(34, 25, 14.00, 35, 0.10),
-- Order 35 (BLAUS, pending)
(35, 11, 21.00, 12, 0.00),
(35, 4, 22.00, 18, 0.05);
