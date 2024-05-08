-- in and not out

CREATE TABLE IF NOT EXISTS users (
	id INT NOT NULL PRIMARY KEY AUTO_increment,
	email VARCHAR(255) NOT NULL UNIQUE,
	name CHAR(255),
	country ENUM('US', 'CO', 'TN') DEFAULT 'US' NOT NULL
);
