-- 1. إعداد قاعدة البيانات
CREATE DATABASE IF NOT EXISTS `smartzone_db`;
USE `smartzone_db`;

SET FOREIGN_KEY_CHECKS = 0;

-- 2. تنظيف الجداول القديمة
DROP TABLE IF EXISTS `specs`;
DROP TABLE IF EXISTS `phones`;
DROP TABLE IF EXISTS `brands`;

-- 3. إنشاء الجداول
CREATE TABLE `brands` (
  `brand_id` INT AUTO_INCREMENT PRIMARY KEY,
  `brand_name` VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `phones` (
  `phone_id` INT AUTO_INCREMENT PRIMARY KEY,
  `model_name` VARCHAR(150) NOT NULL,
  `brand_id` INT,
  `release_date` DATE DEFAULT '1970-01-01',
  `image_url` VARCHAR(255) DEFAULT NULL,
  `price` DECIMAL(10, 2) DEFAULT 0.00,
  CONSTRAINT `fk_brand` FOREIGN KEY (`brand_id`) REFERENCES `brands` (`brand_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `specs` (
  `spec_id` INT AUTO_INCREMENT PRIMARY KEY,
  `phone_id` INT,
  `spec_category` VARCHAR(50) DEFAULT 'General',
  `spec_name` VARCHAR(100),
  `spec_value` TEXT,
  CONSTRAINT `fk_phone` FOREIGN KEY (`phone_id`) REFERENCES `phones` (`phone_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. إدخال الشركات (القائمة الموسعة)
INSERT INTO `brands` (`brand_name`) VALUES 
('Samsung'), ('Apple'), ('Xiaomi'), ('Oppo'), 
('Vivo'), ('Realme'), ('Huawei'), ('Honor'), 
('Infinix'), ('Tecno'), ('Itel'), ('Motorola'), 
('Google'), ('OnePlus'), ('Sony'), ('Asus'), ('Nubia');

-- 5. مثال لبيانات هاتف (اختياري للتجربة)
INSERT INTO `phones` (`model_name`, `brand_id`, `price`, `image_url`) 
VALUES ('Galaxy S24 Ultra', 1, 47000, 'https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-ultra-5g-sm-s928.jpg');

SET @id = LAST_INSERT_ID();
INSERT INTO `specs` (`phone_id`, `spec_category`, `spec_name`, `spec_value`) VALUES
(@id, 'Performance', 'RAM', '12 GB'), 
(@id, 'Display', 'Screen Size', '6.8 inches'),
(@id, 'Battery', 'Capacity', '5000 mAh'), 
(@id, 'Camera', 'Main Camera', '200 MP'),
(@id, 'Platform', 'Chipset', 'Snapdragon 8 Gen 3');

SET FOREIGN_KEY_CHECKS = 1;