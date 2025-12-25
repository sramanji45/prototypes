CREATE DATABASE IF NOT EXISTS master_replicas_db;

USE master_replicas_db;

CREATE TABLE IF NOT EXISTS Bahubali (id INT AUTO_INCREMENT PRIMARY KEY, fname VARCHAR(100) NOT NULL, lname VARCHAR(100) NOT NULL, role VARCHAR(100), salary DECIMAL(10, 2));

INSERT INTO Bahubali (fname, lname, role, salary) VALUES ('Prabhas', 'Raju', 'Actor', 50000.00);
INSERT INTO Bahubali (fname, lname, role, salary) VALUES ('Rana', 'Dhaggubati', 'Actor', 50000.00);
INSERT INTO Bahubali (fname, lname, role, salary) VALUES ('Rajamouli', 'SS', 'Director', 175000.00);
INSERT INTO Bahubali (fname, lname, role, salary) VALUES ('Keeravani', 'MM', 'MusicDirector', 75000.00);
