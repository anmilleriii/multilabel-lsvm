-- Mitigation --

-- Split train_set_1 --

UPDATE SPVAT_cleansed_data
SET train_set_1=1
WHERE ROWID  > 0 AND ROWID <= 72000
AND ROWID % 20 = 0;

-- Split validate_set_1 --

UPDATE SPVAT_cleansed_data
SET validate_set_1=1
WHERE ROWID  > 15 AND ROWID <= 72000
AND ROWID % 20 = 1;

-- Split apply_set_1 --
UPDATE SPVAT_cleansed_data
SET apply_set_1=1
WHERE train_set_1 == 0 AND validate_set_1 == 0;

-- Maintenance --

-- -- Split train_set_2 --

-- UPDATE SPVAT
-- SET train_set_2=1
-- WHERE ROWID  > 0 AND ROWID <= 72000
-- AND ROWID % 20 = 0;

-- -- Split validate_set_1 --

-- UPDATE SPVAT
-- SET validate_set_2=1
-- WHERE ROWID  > 15 AND ROWID <= 72000
-- AND ROWID % 20 = 1;

-- -- Split apply_set_2 --

-- UPDATE SPVAT
-- SET apply_set_1=2
-- WHERE train_set_2 == 0 AND validate_set_2 == 0;