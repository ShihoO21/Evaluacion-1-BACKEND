   CREATE DATABASE IF NOT EXISTS transporte_db
     CHARACTER SET utf8mb4
     COLLATE utf8mb4_unicode_ci;

   CREATE USER IF NOT EXISTS 'transporte_user'@'%' IDENTIFIED BY 'Transporte2026!';
   CREATE USER IF NOT EXISTS 'transporte_user'@'localhost' IDENTIFIED BY 'Transporte2026!';

   GRANT ALL PRIVILEGES ON transporte_db.* TO 'transporte_user'@'%';
   GRANT ALL PRIVILEGES ON transporte_db.* TO 'transporte_user'@'localhost';

   FLUSH PRIVILEGES;