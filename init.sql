-- Creating the Table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL
);

---------------------------------------------------------
-- CREATE TABLE posts (
--    id BIGSERIAL PRIMARY KEY NOT NULL,
--    username VARCHAR(20) NOT NULL,
--    post_text VARCHAR(800) NOT NULL,
--    created_at TIMESTAMP DEFAULT NOW(),
--    FOREIGN KEY (username) REFERENCES users (username)
--);
---------------------------------------------------------