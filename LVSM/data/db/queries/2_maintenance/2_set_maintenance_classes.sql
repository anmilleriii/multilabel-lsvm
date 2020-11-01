-- Set 'Monitor and Maintain' Class --

UPDATE SPVAT_maintenance
SET monitor_and_maintain=1
WHERE apply_set_2==0
AND (Mitigation LIKE '%cleaning%' 
OR Mitigation LIKE '%lubrication%'
OR Mitigation LIKE '%lubricate%'
OR Mitigation LIKE '%inspect%' 
OR Mitigation LIKE '%inspection%' 
OR Mitigation LIKE '%surveillance%'
OR Mitigation LIKE '%vibration analysis%' 
OR Mitigation LIKE '%rail%');

-- Set 'Overhaul or Replace' Class --

UPDATE SPVAT_maintenance
SET overhaul_or_replace=1
WHERE apply_set_2==0
AND (Mitigation LIKE '%rebuild%' 
OR Mitigation LIKE '%assemble%' 
OR Mitigation LIKE '%reassemble%' 
OR Mitigation LIKE '%disassembly%' 
OR Mitigation LIKE '%disassemble%'
OR Mitigation LIKE '%replace%' 
OR Mitigation LIKE '%replacement%' 
OR Mitigation LIKE '%refurbish%');

-- Set 'Test or Calibrate' Class --

UPDATE SPVAT_maintenance
SET test_or_calibrate=1
WHERE apply_set_2 == 0
AND (Mitigation LIKE '%calibration%' 
OR Mitigation LIKE '%recalibration%' 
OR Mitigation LIKE '%test%' 
OR Mitigation LIKE '%testing%' 
OR Mitigation LIKE '%thermography%' 
OR Mitigation LIKE '%current tracing%'
OR Mitigation LIKE '%time testing%');

-- Set 'Interval Based Maintenance' Class --

UPDATE SPVAT_maintenance
SET interval_based_maintenance=1
WHERE apply_set_2 == 0
AND(Mitigation LIKE '%periodic cycling%' -- add "cycle"?
OR Mitigation LIKE '%periodic%'
OR Mitigation LIKE '%year%'
OR Mitigation LIKE '%0Y%' -- SQL has wildcards [0-9], but SQLite does not
OR Mitigation LIKE '%1Y%' 
OR Mitigation LIKE '%2Y%' 
OR Mitigation LIKE '%3Y%' 
OR Mitigation LIKE '%4Y%' 
OR Mitigation LIKE '%5Y%' 
OR Mitigation LIKE '%6Y%' 
OR Mitigation LIKE '%7Y%' 
OR Mitigation LIKE '%8Y%' 
OR Mitigation LIKE '%9Y%' 
OR Mitigation LIKE '%0M%' -- SQL has wildcards [0-9], but SQLite does not
OR Mitigation LIKE '%1M%' 
OR Mitigation LIKE '%2M%' 
OR Mitigation LIKE '%3M%' 
OR Mitigation LIKE '%4M%' 
OR Mitigation LIKE '%5M%' 
OR Mitigation LIKE '%6M%' 
OR Mitigation LIKE '%7M%' 
OR Mitigation LIKE '%8M%' 
OR Mitigation LIKE '%9M%' 
OR Mitigation LIKE '%0R%' -- SQL has wildcards [0-9], but SQLite does not
OR Mitigation LIKE '%1R%' 
OR Mitigation LIKE '%2R%' 
OR Mitigation LIKE '%3R%' 
OR Mitigation LIKE '%4R%' 
OR Mitigation LIKE '%5R%' 
OR Mitigation LIKE '%6R%' 
OR Mitigation LIKE '%7R%' 
OR Mitigation LIKE '%8R%' 
OR Mitigation LIKE '%9R%'
OR Mitigation LIKE '%every __ cycles%');

-- Set 'No Action Required' Class --

UPDATE SPVAT_maintenance
SET no_action_required=1
WHERE apply_set_2==0 
AND (Mitigation LIKE '%Not required%'
OR Mitigation LIKE '%None required%');

-- Set 'Unknown' Class, this has to be done last --

UPDATE SPVAT_maintenance
SET unknown_maintenance=1
WHERE apply_set_2==0 
AND monitor_and_maintain == 0 
AND overhaul_or_replace == 0 
AND test_or_calibrate == 0 
AND interval_based_maintenance == 0 
AND no_action_required == 0;

-- AND (Mitigation LIKE '%None%' 
-- OR Mitigation LIKE '%Not provided%' 
-- OR Mitigation LIKE '%None provided%'
-- OR Mitigation LIKE '%N/A%'
-- OR Mitigation LIKE '%#VALUE%'
-- OR Mitigation LIKE '');

-- Show Table --

SELECT ROWID, Mitigation, Classification, monitor_and_maintain, overhaul_or_replace, test_or_calibrate, interval_based_maintenance, no_action_required, 
unknown_maintenance, train_set_2, validate_set_2, apply_set_2
FROM SPVAT_maintenance
ORDER BY train_set_2 DESC, validate_set_2 DESC;

-- SELECT COUNT(no_action_required) FROM SPVAT_maintenance WHERE no_action_required = 1;

