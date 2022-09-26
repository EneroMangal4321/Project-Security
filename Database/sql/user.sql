SELECT USER ();

USE `psdb` ;

CREATE USER login IDENTIFIED WITH caching_sha2_password BY '2Sasf@csAas3';
GRANT SELECT ON admin TO 'login';
COMMIT;
