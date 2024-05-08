-- creating a table 

CREATE TABLE IF NOT EXISTS users (
	id INT PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	name char(255)
);
