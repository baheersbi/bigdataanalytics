create database bugbond;

use bugbond;

CREATE TABLE Stores (
    StoreID INT AUTO_INCREMENT PRIMARY KEY,
    StoreName VARCHAR(255) NOT NULL,
    Location VARCHAR(255) NOT NULL,
    Contact VARCHAR(255)
);

show tables;

-- Creating the Employees table
CREATE TABLE Employees (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    SSN CHAR(11) NOT NULL UNIQUE,
    Name VARCHAR(255) NOT NULL,
    Gender ENUM('M', 'F', 'O') NOT NULL,
    DoB DATE NOT NULL,
    Position VARCHAR(255),
    Salary DECIMAL(10, 2),
    AffiliateStore INT,
    SupervisorID INT,
    FOREIGN KEY (AffiliateStore) REFERENCES Stores(StoreID),
    FOREIGN KEY (SupervisorID) REFERENCES Employees(EmployeeID)
) ENGINE=INNODB;

-- Creating the Vendors table
CREATE TABLE Vendors (
    VendorName VARCHAR(255) PRIMARY KEY,
    Address VARCHAR(255) NOT NULL,
    ContactPerson VARCHAR(255) NOT NULL
);

-- Creating the Products table
CREATE TABLE Products (
    Name VARCHAR(255) PRIMARY KEY,
    Price DECIMAL(10, 2) NOT NULL,
    Quantity INT NOT NULL,
    Description TEXT,
    VendorName VARCHAR(255),
    FOREIGN KEY (VendorName) REFERENCES Vendors(VendorName)
) ENGINE=INNODB;

-- Associative table for many-to-many relationship between Stores and Products
CREATE TABLE StoreProducts (
    StoreID INT,
    ProductName VARCHAR(255),
    PRIMARY KEY (StoreID, ProductName),
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID),
    FOREIGN KEY (ProductName) REFERENCES Products(Name)
) ENGINE=INNODB;
