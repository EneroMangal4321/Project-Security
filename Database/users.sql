-- Create user for sign up

-- SELECT CURRENT_USER();

SELECT USER();

USE `psdb`;

-- Create user for login
CREATE USER login IDENTIFIED WITH caching_sha2_password BY '*2Sasf@csAas3';
GRANT SELECT ON admin TO 'login';

COMMIT;