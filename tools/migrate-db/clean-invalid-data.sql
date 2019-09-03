BEGIN;

-- delete invalid users
DELETE FROM `user` where sex is NULL or account_active is NULL;

-- sqlite doesn't support delete left join

-- delete comments without existing user
DELETE FROM comment WHERE id in
(SELECT t1.id FROM comment t1
 LEFT JOIN complaint t2 ON t1.complaint_id = t2.id
WHERE t2.id IS NULL);

-- delete complaints without existing user
DELETE FROM complaint WHERE id in
(SELECT t1.id FROM complaint t1
 LEFT JOIN `user` t2 ON t1.user_id = t2.id
WHERE t2.id IS NULL);

COMMIT;
