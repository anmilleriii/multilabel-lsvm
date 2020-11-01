UPDATE SPVAT_maintenance
SET train_set_2 = 0, validate_set_2 = 0, apply_set_2 = 0, monitor_and_maintain =0, test_or_calibrate =0, overhaul_or_replace = 0, interval_based_maintenance =0, no_action_required = 0, unknown_maintenance = 0;


-- SELECT train_set_2, validate_set_2, apply_set_2 FROM SPVAT_maintenance ORDER BY train_set_2 DESC, validate_set_2 DESC;