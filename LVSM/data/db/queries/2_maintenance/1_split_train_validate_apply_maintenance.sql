-- Maintenance --

-- Split train_set_2 --

UPDATE SPVAT_maintenance
SET train_set_2=1
WHERE ROWID  > 0 AND ROWID <= 72000 --maintenance only has already been taken care of in table
AND ROWID % 20 = 0;

-- Split validate_set_2 --

UPDATE SPVAT_maintenance
SET validate_set_2=1
WHERE ROWID  > 15 AND ROWID <= 72000 -- 15 is arbitrary
AND ROWID % 20 = 1;

-- Split apply_set_2 --
UPDATE SPVAT_maintenance
SET apply_set_2=1
WHERE train_set_2 == 0 AND validate_set_2 == 0;

SELECT * FROM SPVAT_maintenance;