CREATE TABLE SPVAT_maintenance AS
SELECT * FROM import_mitigation_results_to_db
WHERE maintenance_p = 1;