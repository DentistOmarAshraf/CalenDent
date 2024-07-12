-- Creating User and Grant Privilage

CREATE DATABASE IF NOT EXISTS calen_dev_db;

CREATE USER IF NOT EXISTS
'calen_dev'@'localhost' IDENTIFIED WITH mysql_native_password BY 'calen_dev_pwd';

FLUSH PRIVILEGES;
GRANT ALL ON calen_dev_db.* TO 'calen_dev'@'localhost';

FLUSH PRIVILEGES;
GRANT SELECT ON performance_schema.* TO 'calen_dev'@'localhost';

FLUSH PRIVILEGES;
