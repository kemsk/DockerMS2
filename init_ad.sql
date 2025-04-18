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
