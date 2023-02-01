CREATE TABLE IF NOT EXISTS users (
    user_id INT NOT NULL,
    name VARCHAR(255) DEFAULT NULL,
    gender VARCHAR(255) DEFAULT NULL,
    address VARCHAR(255) DEFAULT NULL,
    date_of_birth VARCHAR(255) DEFAULT NULL,
    email_address VARCHAR(255) DEFAULT NULL,
    height_cm INT DEFAULT NULL,
    weight_kg INT DEFAULT NULL,
    account_create_date TIMESTAMP DEFAULT NULL,
    bike_serial VARCHAR(255) DEFAULT NULL,
    original_source VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS users_rides (
    ride_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (ride_id) REFERENCES rides (ride_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE IF NOT EXISTS rides (
    ride_id INT DEFAULT NULL,
    date VARCHAR(255) DEFAULT NULL,
    time VARCHAR(255) DEFAULT NULL,
    duration DECIMAL DEFAULT NULL,
    resistance INT DEFAULT NULL,
    heart_rate INT DEFAULT NULL,
    rpm INT DEFAULT NULL,
    power DECIMAL DEFAULT NULL,
    PRIMARY KEY (ride_id)
);