SELECT USER ();

USE `psdb` ;

CREATE USER login IDENTIFIED WITH caching_sha2_password BY '2Sasf@csAas3';
GRANT SELECT, INSERT, UPDATE ON admin TO 'login';
GRANT SELECT, INSERT, UPDATE ON banned_table TO 'login';
COMMIT;
