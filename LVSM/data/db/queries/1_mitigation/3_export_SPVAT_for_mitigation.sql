SELECT * FROM SPVAT_cleansed_data
ORDER BY train_set_1 DESC, validate_set_1 DESC;
-- select ifnull(Mitigation, 'N/A') from SPVAT_cleansed_data;

-- SELECT Mitigation FROM SPVAT_cleansed_data WHERE Fleet = 'Xcel Energy'
-- ORDER BY train_set_1 DESC, validate_set_1 DESC;

-- SELECT ISNULL(Mitigation, 'None provided') FROM SPVAT_cleansed_data;
-- CASE WHEN fieldname IS NULL THEN 0 ELSE fieldname END

-- SELECT COALESCE(Mitigation, 'None provided') FROM SPVAT_cleansed_data;