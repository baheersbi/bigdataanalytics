select Name, Price, Quantity from Products where Price between 15.00 AND 40;

SELECT * FROM Employees where Name like 'J%';

select * from Employees;
SELECT * FROM Employees where SupervisorID is null;

SELECT * FROM Employees where Name like '%e';

SELECT * FROM Employees where Name like '%m%';

SELECT * FROM Employees where Name like '_m%';

SELECT * from Employees where Name REGEXP '^O';
SELECT * from Employees where Name REGEXP 'm$';

SELECT * FROM Employees;

create view EmployeeStore as
SELECT EmployeeID, SSN, Name, Position, Stores.StoreID, StoreName
FROM Employees
         INNER JOIN Stores
                    ON Employees.AffiliateStore = Stores.StoreID;

SELECT Name, StoreName FROM EmployeeStore;


SELECT *
FROM Employees
         LEFT JOIN Stores
                    ON Employees.AffiliateStore = Stores.StoreID;

SELECT *
FROM Employees
         RIGHT JOIN Stores
                   ON Employees.AffiliateStore = Stores.StoreID;

SELECT *
FROM Employees
          CROSS JOIN Stores;

SELECT A.Name AS EmployeeName1, B.Name AS EmployeeName2, A.SupervisorID
FROM Employees A, Employees B
WHERE A.EmployeeID <> B.EmployeeID
  AND A.SupervisorID = B.SupervisorID
ORDER BY A.SupervisorID;


########Using Case##########



SELECT
    Name,
    Price,
    CASE
        WHEN Price < 10 THEN 'Cheap'
        WHEN Price >= 10 AND Price <= 50 THEN 'Moderate'
        ELSE 'Expensive'
        END AS PriceCategory
FROM
    Products;


SELECT
    Name,
    Quantity,
    CASE
        WHEN Quantity = 0 THEN 'Out of Stock'
        ELSE 'In Stock'
        END AS StockStatus
FROM
    Products;


SELECT
    Name,
    Price,
    VendorName,
    CASE VendorName
        WHEN 'Pet Paradise' THEN Price * 0.9 -- 10% discount for VendorA
        WHEN 'Ready Tools' THEN Price * 0.85 -- 15% discount for VendorB
        ELSE Price
        END AS DiscountedPrice
FROM
    Products;


SELECT
    Name,
    Quantity,
    CASE
        WHEN Quantity = 0 THEN 'Currently unavailable'
        WHEN Quantity <= 5 THEN 'Limited stock available'
        ELSE 'Available in ample quantity'
        END AS StockDescription
FROM
    Products;


SELECT
    Name,
    Price,
    Quantity,
    CASE
        WHEN Quantity = 0 AND Price > 50 THEN 'High priced and out of stock'
        WHEN Quantity > 10 AND Price < 20 THEN 'Affordable and well-stocked'
        ELSE 'Varies'
        END AS ProductStatus
FROM
    Products;
