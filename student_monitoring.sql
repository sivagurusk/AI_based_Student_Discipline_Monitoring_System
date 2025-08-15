CREATE DATABASE IF NOT EXISTS student_monitoring;

USE student_monitoring;

CREATE TABLE IF NOT EXISTS dress_code_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    shirt_status VARCHAR(50),
    shoe_status VARCHAR(50),
    hair_status VARCHAR(50)
);
