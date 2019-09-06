SET NAMES utf8mb4;

-- this is a reference schema from sqlite to mysql
-- however, we are actually using table generated from sqlalchemy models

CREATE TABLE IF NOT EXISTS `user`
(
  `id` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(64),
  `email` VARCHAR(120),
  `password_hash` VARCHAR(128),
  `account_active` BOOLEAN,
  `if_verified` BOOLEAN,
  `minority` VARCHAR(120),
  `real_name` VARCHAR(120),
  `registered_date` VARCHAR(120),
  `sex` VARCHAR(120),
  `first_name` VARCHAR(120),
  `last_name` VARCHAR(120),
  `is_founder` tinyint(1) DEFAULT NULL,
  `urole` VARCHAR(120)
);

CREATE TABLE IF NOT EXISTS `merchant_query_raw`
(
  `id` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `keyword` VARCHAR(140),
  `storage` JSON COMMENT '企查查查询结果json序列化'
);

CREATE TABLE IF NOT EXISTS `fuzzy_search_raw`
(
  `id` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `keyword` VARCHAR(140),
  `storage` JSON COMMENT '企查查查询结果json序列化',
  `pageIndex` INTEGER,
  `totalPage` INTEGER
);

CREATE TABLE IF NOT EXISTS `complaint`
(
  `id` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `complaint_body` TEXT,
  `expected_solution_body` TEXT,
  `complain_type` VARCHAR(140),
  `complain_timestamp` DATETIME,
  `user_id` INTEGER,
  `if_negotiated_by_merchant` BOOLEAN,
  `negotiate_timestamp` DATETIME,
  `allow_public` BOOLEAN,
  `allow_contact_by_merchant` BOOLEAN,
  `allow_press` BOOLEAN,
  `item_price` VARCHAR(200),
  `item_model` VARCHAR(200),
  `trade_info` VARCHAR(1000),
  `relatedProducts` VARCHAR(1000),
  `purchase_timestamp` DATETIME,
  `invoice_files` VARCHAR(2000),
  `evidence_files` VARCHAR(2000),
  `merchant_id` INTEGER,
  `complaint_status` VARCHAR(140),
  `audit_status` VARCHAR(140)
);

CREATE TABLE IF NOT EXISTS `comment`
(
  `id` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `user_id` INTEGER,
  `text` VARCHAR(5000),
  `timestamp` DATETIME,
  `complaint_id` INTEGER
);

ALTER TABLE `comment` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `comment` ADD FOREIGN KEY (`complaint_id`) REFERENCES `complaint` (`id`);

ALTER TABLE `complaint` ADD FOREIGN KEY (`merchant_id`) REFERENCES `merchant_query_raw` (`id`);
