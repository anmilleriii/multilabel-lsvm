CREATE TABLE SPVAT_maintenance AS
SELECT * FROM import_mitigation_results_to_db
WHERE maintenance_p = 1 OR maintenance = 1; -- Grab records which are maintenance as a mitigation strategy, including from test set