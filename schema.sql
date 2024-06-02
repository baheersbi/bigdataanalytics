
use penpulse;

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

