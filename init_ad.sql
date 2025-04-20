<<<<<<< HEAD
CREATE DATABASE IF NOT EXISTS XUSSIO_AD;

USE XUSSIO_AD;

CREATE TABLE IF NOT EXISTS students (
    studentId VARCHAR(20) PRIMARY KEY,
    fullName VARCHAR(100),
    course VARCHAR(100),
    yearLevel VARCHAR(10),
    email VARCHAR(100),
    contactNumber VARCHAR(15),
    address VARCHAR(255)
);

INSERT INTO students (studentId, fullName, course, yearLevel, email, contactNumber, address)
VALUES (
    '202310123',
    'Juan Dela Cruz',
    'BS Information Technology',
    '3',
    'juan.delacruz@xu.edu.ph',
    '09171234567',
    'Cagayan de Oro City'
)
ON DUPLICATE KEY UPDATE fullName = VALUES(fullName);
=======
CREATE DATABASE IF NOT EXISTS ActiveDirectoryDB;
USE ActiveDirectoryDB;

CREATE TABLE IF NOT EXISTS students (
    studentId VARCHAR(20) PRIMARY KEY,
    fullName VARCHAR(100) NOT NULL,
    course VARCHAR(100),
    yearLevel VARCHAR(10),
    email VARCHAR(100),
    contactNumber VARCHAR(20),
    address VARCHAR(255)
);
>>>>>>> f1d7af53b2ec1c899a873523aef130c85bdfcbd5
