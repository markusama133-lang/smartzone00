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

-- 4. إدخال الشركات
INSERT INTO `brands` (`brand_name`) VALUES 
('Samsung'), ('Apple'), ('Xiaomi'), ('Realme'), 
('Honor'), ('Oppo'), ('Vivo'), ('OnePlus'), 
('Google'), ('Infinix'), ('Nothing');

-- 5. إدخال 15 موبايل ببيانات كاملة

-- 1. Samsung Galaxy S24 Ultra
INSERT INTO `phones` (`model_name`, `brand_id`, `price`, `image_url`) 
VALUES ('Galaxy S24 Ultra', 1, 47000, 'https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-ultra-5g-sm-s928.jpg');
SET @id = LAST_INSERT_ID();
INSERT INTO `specs` (`phone_id`, `spec_category`, `spec_name`, `spec_value`) VALUES
(@id, 'Performance', 'RAM', '12 GB'), (@id, 'Storage', 'Internal', '256 GB'),
(@id, 'Battery', 'Capacity', '5000 mAh'), (@id, 'Camera', 'Main Camera', '200 MP'),
(@id, 'Platform', 'Chipset', 'Snapdragon 8 Gen 3');

-- 2. iPhone 15 Pro Max
INSERT INTO `phones` (`model_name`, `brand_id`, `price`, `image_url`) 
VALUES ('iPhone 15 Pro Max', 2, 61000, 'https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-15-pro-max.jpg');
SET @id = LAST_INSERT_ID();
INSERT INTO `specs` (`phone_id`, `spec_category`, `spec_name`, `spec_value`) VALUES
(@id, 'Performance', 'RAM', '8 GB'), (@id, 'Storage', 'Internal', '256 GB'),
(@id, 'Battery', 'Capacity', '4441 mAh'), (@id, 'Camera', 'Main Camera', '48 MP'),
(@id, 'Platform', 'Chipset', 'Apple A17 Pro');

-- 3. Xiaomi 14 Ultra
INSERT INTO `phones` (`model_name`, `brand_id`, `price`, `image_url`) 
VALUES ('Xiaomi 14 Ultra', 3, 44000, 'https://fdn2.gsmarena.com/vv/bigpic/xiaomi-14-ultra-new.jpg');
SET @id = LAST_INSERT_ID();
INSERT INTO `specs` (`phone_id`, `spec_category`, `spec_name`, `spec_value`) VALUES
(@id, 'Performance', 'RAM', '16 GB'), (@id, 'Storage', 'Internal', '512 GB'),
(@id, 'Battery', 'Capacity', '5000 mAh'), (@id, 'Camera', 'Main Camera', '50 MP'),
(@id, 'Platform', 'Chipset', 'Snapdragon 8 Gen 3');

-- 4. Samsung Galaxy A55
INSERT INTO `phones` (`model_name`, `brand_id`, `price`, `image_url`) 
VALUES ('Galaxy A55', 1, 19500, 'https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-a55.jpg');
SET @id = LAST_INSERT_ID();
INSERT INTO `specs` (`phone_id`, `spec_category`, `spec_name`, `spec_value`) VALUES
(@id, 'Performance', 'RAM', '8 GB'), (@id, 'Storage', 'Internal', '128 GB'),
(@id, 'Battery', 'Capacity', '5000 mAh'), (@id, 'Camera', 'Main Camera', '50 MP'),
(@id, 'Platform', 'Chipset', 'Exynos 1480');

-- 5. Realme 12 Pro Plus
INSERT INTO `phones` (`model_name`, `brand_id`, `price`, `image_url`) 
VALUES ('12 Pro Plus', 4, 16500, 'https://fdn2.gsmarena.com/vv/bigpic/realme-12-pro-plus.jpg');
SET @id = LAST_INSERT_ID();
INSERT INTO `specs` (`phone_id`, `spec_category`, `spec_name`, `spec_value`) VALUES
(@id, 'Performance', 'RAM', '12 GB'), (@id, 'Storage', 'Internal', '256 GB'),
(@id, 'Battery', 'Capacity', '5000 mAh'), (@id, 'Camera', 'Main Camera', '50 MP'),
(@id, 'Platform', 'Chipset', 'Snapdragon 7s Gen 2');

-- 6. Redmi Note 13 Pro+
INSERT INTO `phones` (`model_name`, `brand_id`, `price`, `image_url`) 
VALUES ('Redmi Note 13 Pro+', 3, 18000, 'https://fdn2.gsmarena.com/vv/bigpic/xiaomi-redmi-note-13-pro-plus-5g.jpg');
SET @id = LAST_INSERT_ID();
INSERT INTO `specs` (`phone_id`, `spec_category`, `spec_name`, `spec_value`) VALUES
(@id, 'Performance', 'RAM', '12 GB'), (@id, 'Storage', 'Internal', '512 GB'),
(@id, 'Battery', 'Capacity', '5000 mAh'), (@id, 'Camera', 'Main Camera', '200 MP'),
(@id, 'Platform', 'Chipset', 'Dimensity 7200 Ultra');

-- 7. Honor X9b
INSERT INTO `phones` (`model_name`, `brand_id`, `price`, `image_url`) 
VALUES ('X9b', 5, 15000, 'https://fdn2.gsmarena.com/vv/bigpic/honor-x9b.jpg');
SET @id = LAST_INSERT_ID();
INSERT INTO `specs` (`phone_id`, `spec_category`, `spec_name`, `spec_value`) VALUES
(@id, 'Performance', 'RAM', '12 GB'), (@id, 'Storage', 'Internal', '256 GB'),
(@id, 'Battery', 'Capacity', '5800 mAh'), (@id, 'Camera', 'Main Camera', '108 MP'),
(@id, 'Platform', 'Chipset', 'Snapdragon 6 Gen 1');

-- 8. Oppo Reno 11 F
INSERT INTO `phones` (`model_name`, `brand_id`, `price`, `image_url`) 
VALUES ('Reno 11 F', 6, 14500, 'https://fdn2.gsmarena.com/vv/bigpic/oppo-reno11-f.jpg');
SET @id = LAST_INSERT_ID();
INSERT INTO `specs` (`phone_id`, `spec_category`, `spec_name`, `spec_value`) VALUES
(@id, 'Performance', 'RAM', '8 GB'), (@id, 'Storage', 'Internal', '256 GB'),
(@id, 'Battery', 'Capacity', '5000 mAh'), (@id, 'Camera', 'Main Camera', '64 MP'),
(@id, 'Platform', 'Chipset', 'Dimensity 7050');

-- 9. Poco X6 Pro
INSERT INTO `phones` (`model_name`, `brand_id`, `price`, `image_url`) 
VALUES ('Poco X6 Pro', 3, 17500, 'https://fdn2.gsmarena.com/vv/bigpic/xiaomi-poco-x6-pro.jpg');
SET @id = LAST_INSERT_ID();
INSERT INTO `specs` (`phone_id`, `spec_category`, `spec_name`, `spec_value`) VALUES
(@id, 'Performance', 'RAM', '12 GB'), (@id, 'Storage', 'Internal', '512 GB'),
(@id, 'Battery', 'Capacity', '5000 mAh'), (@id, 'Camera', 'Main Camera', '64 MP'),
(@id, 'Platform', 'Chipset', 'Dimensity 8300 Ultra');

-- 10. Vivo V30
INSERT INTO `phones` (`model_name`, `brand_id`, `price`, `image_url`) 
VALUES ('V30', 7, 21000, 'https://fdn2.gsmarena.com/vv/bigpic/vivo-v30.jpg');
SET @id = LAST_INSERT_ID();
INSERT INTO `specs` (`phone_id`, `spec_category`, `spec_name`, `spec_value`) VALUES
(@id, 'Performance', 'RAM', '12 GB'), (@id, 'Storage', 'Internal', '256 GB'),
(@id, 'Battery', 'Capacity', '5000 mAh'), (@id, 'Camera', 'Main Camera', '50 MP'),
(@id, 'Platform', 'Chipset', 'Snapdragon 7 Gen 3');

-- 11. Samsung Galaxy S23 FE
INSERT INTO `phones` (`model_name`, `brand_id`, `price`, `image_url`) 
VALUES ('Galaxy S23 FE', 1, 26000, 'https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s23-fe.jpg');
SET @id = LAST_INSERT_ID();
INSERT INTO `specs` (`phone_id`, `spec_category`, `spec_name`, `spec_value`) VALUES
(@id, 'Performance', 'RAM', '8 GB'), (@id, 'Storage', 'Internal', '256 GB'),
(@id, 'Battery', 'Capacity', '4500 mAh'), (@id, 'Camera', 'Main Camera', '50 MP'),
(@id, 'Platform', 'Chipset', 'Exynos 2200');

-- 12. OnePlus 12
INSERT INTO `phones` (`model_name`, `brand_id`, `price`, `image_url`) 
VALUES ('12', 8, 39000, 'https://fdn2.gsmarena.com/vv/bigpic/oneplus-12.jpg');
SET @id = LAST_INSERT_ID();
INSERT INTO `specs` (`phone_id`, `spec_category`, `spec_name`, `spec_value`) VALUES
(@id, 'Performance', 'RAM', '16 GB'), (@id, 'Storage', 'Internal', '512 GB'),
(@id, 'Battery', 'Capacity', '5400 mAh'), (@id, 'Camera', 'Main Camera', '50 MP'),
(@id, 'Platform', 'Chipset', 'Snapdragon 8 Gen 3');

-- 13. Infinix Note 40 Pro
INSERT INTO `phones` (`model_name`, `brand_id`, `price`, `image_url`) 
VALUES ('Note 40 Pro', 10, 12000, 'https://fdn2.gsmarena.com/vv/bigpic/infinix-note-40-pro.jpg');
SET @id = LAST_INSERT_ID();
INSERT INTO `specs` (`phone_id`, `spec_category`, `spec_name`, `spec_value`) VALUES
(@id, 'Performance', 'RAM', '8 GB'), (@id, 'Storage', 'Internal', '256 GB'),
(@id, 'Battery', 'Capacity', '5000 mAh'), (@id, 'Camera', 'Main Camera', '108 MP'),
(@id, 'Platform', 'Chipset', 'Helio G99 Ultimate');

-- 14. Realme C67
INSERT INTO `phones` (`model_name`, `brand_id`, `price`, `image_url`) 
VALUES ('C67', 4, 9000, 'https://fdn2.gsmarena.com/vv/bigpic/realme-c67-4g.jpg');
SET @id = LAST_INSERT_ID();
INSERT INTO `specs` (`phone_id`, `spec_category`, `spec_name`, `spec_value`) VALUES
(@id, 'Performance', 'RAM', '8 GB'), (@id, 'Storage', 'Internal', '256 GB'),
(@id, 'Battery', 'Capacity', '5000 mAh'), (@id, 'Camera', 'Main Camera', '108 MP'),
(@id, 'Platform', 'Chipset', 'Snapdragon 685');

-- 15. Nothing Phone (2a)
INSERT INTO `phones` (`model_name`, `brand_id`, `price`, `image_url`) 
VALUES ('Phone (2a)', 11, 19000, 'https://fdn2.gsmarena.com/vv/bigpic/nothing-phone-2a.jpg');
SET @id = LAST_INSERT_ID();
INSERT INTO `specs` (`phone_id`, `spec_category`, `spec_name`, `spec_value`) VALUES
(@id, 'Performance', 'RAM', '12 GB'), (@id, 'Storage', 'Internal', '256 GB'),
(@id, 'Battery', 'Capacity', '5000 mAh'), (@id, 'Camera', 'Main Camera', '50 MP'),
(@id, 'Platform', 'Chipset', 'Dimensity 7200 Pro');

SET FOREIGN_KEY_CHECKS = 1;