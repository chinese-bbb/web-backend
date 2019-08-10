SET NAMES utf8mb4;

create TABLE `user` (
	`id` INTEGER NOT NULL,
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
	PRIMARY KEY (`id`)
);

create TABLE `post` (
	id INTEGER NOT NULL,
	body VARCHAR(140),
	timestamp DATETIME,
	user_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(user_id) REFERENCES user (id)
);

create TABLE `merchant_query_raw` (
	id INTEGER NOT NULL,
	keyword VARCHAR(140),
	storage VARCHAR(20000),
	PRIMARY KEY (id)
);

create TABLE `fuzzy_search_raw` (
	id INTEGER NOT NULL,
	keyword VARCHAR(140),
	storage VARCHAR(10000),
	pageIndex INTEGER,
	totalPage INTEGER,
	PRIMARY KEY (id)
);

create TABLE `complaint`
(
  id                        INTEGER NOT NULL
    PRIMARY KEY,
  complaint_body            VARCHAR(20000),
  expected_solution_body    VARCHAR(20000),
  complain_type             VARCHAR(140),
  complain_timestamp        DATETIME,
  user_id                   INTEGER
    REFERENCES user (id),
  if_negotiated_by_merchant BOOLEAN,
  negotiate_timestamp       DATETIME,
  allow_public              BOOLEAN,
  allow_contact_by_merchant BOOLEAN,
  allow_press               BOOLEAN,
  item_price                VARCHAR(200),
  item_model                VARCHAR(200),
  trade_info                VARCHAR(20000),
  relatedProducts           VARCHAR(2000),
  purchase_timestamp        DATETIME,
  invoice_files             VARCHAR(2000),
  evidence_files                  VARCHAR(2000),
  merchant_id               INTEGER,
  complaint_status          VARCHAR(140),
  CHECK (if_negotiated_by_merchant IN (0, 1)),
  CHECK (allow_public IN (0, 1)),
  CHECK (allow_contact_by_merchant IN (0, 1)),
  CHECK (allow_press IN (0, 1))
);

create TABLE `comment` (
	id INTEGER NOT NULL,
	user_id INTEGER,
	text VARCHAR(5000),
	timestamp DATETIME,
	complaint_id INTEGER,
	PRIMARY KEY (id),
	CONSTRAINT fk_comment_complaint_id_complaint FOREIGN KEY(complaint_id) REFERENCES complaint (id),
	FOREIGN KEY(user_id) REFERENCES user (id)
);
