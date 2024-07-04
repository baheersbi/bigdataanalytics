INSERT INTO Stores (StoreName, Location, Contact) VALUES ('Sunset Mart', '123 Sunset Blvd, Sunnydale', '555-1234');
INSERT INTO Stores (StoreName, Location, Contact) VALUES ('Moonlight Goods', '456 Moon St, Nightville', '555-5678');
INSERT INTO Stores (StoreName, Location, Contact) VALUES ('Starlight Store', '789 Star Ave, Star City', '555-9012');
INSERT INTO Stores (StoreName, Location, Contact) VALUES ('River Mart', '321 River Rd, River Town', '555-3456');
INSERT INTO Stores (StoreName, Location, Contact) VALUES ('Ocean Retail', '654 Ocean Drive, Oceanview', '555-7890');
INSERT INTO Stores (StoreName, Location, Contact) VALUES ('Forest Outfitters', '987 Forest Lane, Green Forest', '555-2345');
INSERT INTO Stores (StoreName, Location, Contact) VALUES ('Mountain Market', '654 Mountain Peak, High Mountain', '555-6789');
INSERT INTO Stores (StoreName, Location, Contact) VALUES ('Valley Shop', '321 Valley Road, Deep Valley', '555-4321');
INSERT INTO Stores (StoreName, Location, Contact) VALUES ('Lake Commerce', '852 Lake Ave, Lake City', '555-8765');
INSERT INTO Stores (StoreName, Location, Contact) VALUES ('Desert Depot', '963 Desert Sands, Dry Desert', '555-6543');



INSERT INTO Employees (SSN, Name, Gender, DoB, Position, Salary, AffiliateStore, SupervisorID) VALUES ('123-45-6789', 'John Doe', 'M', '1980-05-15', 'Manager', 55000.00, 1, NULL);
INSERT INTO Employees (SSN, Name, Gender, DoB, Position, Salary, AffiliateStore, SupervisorID) VALUES ('987-65-4321', 'Jane Smith', 'F', '1979-07-28', 'Supervisor', 47000.00, 2, 1);
INSERT INTO Employees (SSN, Name, Gender, DoB, Position, Salary, AffiliateStore, SupervisorID) VALUES ('111-22-3333', 'Jim Beam', 'M', '1985-11-30', 'Sales Associate', 32000.00, 3, 2);
INSERT INTO Employees (SSN, Name, Gender, DoB, Position, Salary, AffiliateStore, SupervisorID) VALUES ('222-33-4444', 'Emma Wilson', 'F', '1990-09-15', 'Cashier', 30000.00, 4, 2);
INSERT INTO Employees (SSN, Name, Gender, DoB, Position, Salary, AffiliateStore, SupervisorID) VALUES ('333-44-5555', 'Olivia Jones', 'F', '1988-12-20', 'Stock Manager', 36000.00, 5, 1);
INSERT INTO Employees (SSN, Name, Gender, DoB, Position, Salary, AffiliateStore, SupervisorID) VALUES ('444-55-6666', 'Noah Davis', 'M', '1982-04-09', 'Assistant Manager', 42000.00, 6, 1);
INSERT INTO Employees (SSN, Name, Gender, DoB, Position, Salary, AffiliateStore, SupervisorID) VALUES ('555-66-7777', 'Liam Brown', 'M', '1986-01-23', 'Customer Service', 34000.00, 7, 3);
INSERT INTO Employees (SSN, Name, Gender, DoB, Position, Salary, AffiliateStore, SupervisorID) VALUES ('666-77-8888', 'Sophia Miller', 'F', '1992-03-30', 'HR Manager', 45000.00, 8, 4);
INSERT INTO Employees (SSN, Name, Gender, DoB, Position, Salary, AffiliateStore, SupervisorID) VALUES ('777-88-9999', 'Lucas Moore', 'M', '1983-07-17', 'IT Specialist', 52000.00, 9, 4);
INSERT INTO Employees (SSN, Name, Gender, DoB, Position, Salary, AffiliateStore, SupervisorID) VALUES ('888-99-0000', 'Mia Taylor', 'F', '1985-06-11', 'Marketing Coordinator', 38000.00, 10, 2);



INSERT INTO Vendors (VendorName, Address, ContactPerson) VALUES ('Quality Electronics', '123 Tech Blvd, Silicon Valley', 'Tom Harris');
INSERT INTO Vendors (VendorName, Address, ContactPerson) VALUES ('Farm Fresh Produce', '456 Farm Road, Countryside', 'Sally Field');
INSERT INTO Vendors (VendorName, Address, ContactPerson) VALUES ('Ready Tools', '789 Tool Dr, Hardware City', 'Bob Builder');
INSERT INTO Vendors (VendorName, Address, ContactPerson) VALUES ('Office Supplies Co.', '321 Paper St, Business Town', 'Alice Keys');
INSERT INTO Vendors (VendorName, Address, ContactPerson) VALUES ('Health & Wellness', '654 Health Ave, Wellness City', 'Gary Fit');
INSERT INTO Vendors (VendorName, Address, ContactPerson) VALUES ('Gourmet Foods', '987 Gourmet Ln, Tasty City', 'Gordon Cook');
INSERT INTO Vendors (VendorName, Address, ContactPerson) VALUES ('Quick Clothing', '654 Fashion St, Stylish City', 'Anna Cloth');
INSERT INTO Vendors (VendorName, Address, ContactPerson) VALUES ('Home Essentials', '321 Home Rd, Comfort Town', 'Laura Nest');
INSERT INTO Vendors (VendorName, Address, ContactPerson) VALUES ('Toy World', '852 Play Ave, Kids Town', 'Jess Play');
INSERT INTO Vendors (VendorName, Address, ContactPerson) VALUES ('Pet Paradise', '963 Pet Blvd, Animal City', 'Pat Friend');


INSERT INTO Products (Name, Price, Quantity, Description, VendorName) VALUES ('Laptop', 1200.00, 30, 'High performance personal laptop.', 'Quality Electronics');
INSERT INTO Products (Name, Price, Quantity, Description, VendorName) VALUES ('Apples', 0.75, 150, 'Fresh organic apples.', 'Farm Fresh Produce');
INSERT INTO Products (Name, Price, Quantity, Description, VendorName) VALUES ('Hammer', 25.00, 45, 'Heavy duty claw hammer.', 'Ready Tools');
INSERT INTO Products (Name, Price, Quantity, Description, VendorName) VALUES ('Printer Paper', 5.00, 200, '500 sheets of white printer paper.', 'Office Supplies Co.');
INSERT INTO Products (Name, Price, Quantity, Description, VendorName) VALUES ('Yoga Mat', 20.00, 50, 'Eco-friendly yoga mat.', 'Health & Wellness');
INSERT INTO Products (Name, Price, Quantity, Description, VendorName) VALUES ('Gourmet Cheese', 15.00, 40, 'Imported from France.', 'Gourmet Foods');
INSERT INTO Products (Name, Price, Quantity, Description, VendorName) VALUES ('T-Shirt', 10.00, 100, 'Cotton graphic tee.', 'Quick Clothing');
INSERT INTO Products (Name, Price, Quantity, Description, VendorName) VALUES ('Bed Sheets', 40.00, 30, 'King size cotton bed sheets.', 'Home Essentials');
INSERT INTO Products (Name, Price, Quantity, Description, VendorName) VALUES ('Toy Train', 30.00, 60, 'Battery operated toy train.', 'Toy World');
INSERT INTO Products (Name, Price, Quantity, Description, VendorName) VALUES ('Cat Food', 1.50, 100, 'Dry cat food, 5 lb bag.', 'Pet Paradise');


-- Assuming StoreID and ProductName match existing records. Adjust as necessary.
INSERT INTO StoreProducts (StoreID, ProductName) VALUES (1, 'Laptop');
INSERT INTO StoreProducts (StoreID, ProductName) VALUES (2, 'Apples');
INSERT INTO StoreProducts (StoreID, ProductName) VALUES (3, 'Hammer');
INSERT INTO StoreProducts (StoreID, ProductName) VALUES (4, 'Printer Paper');
INSERT INTO StoreProducts (StoreID, ProductName) VALUES (5, 'Yoga Mat');
INSERT INTO StoreProducts (StoreID, ProductName) VALUES (6, 'Gourmet Cheese');
INSERT INTO StoreProducts (StoreID, ProductName) VALUES (7, 'T-Shirt');
INSERT INTO StoreProducts (StoreID, ProductName) VALUES (8, 'Bed Sheets');
INSERT INTO StoreProducts (StoreID, ProductName) VALUES (9, 'Toy Train');
INSERT INTO StoreProducts (StoreID, ProductName) VALUES (10, 'Cat Food');