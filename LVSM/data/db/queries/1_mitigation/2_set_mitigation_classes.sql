-- Remove null values from SPVAT --

UPDATE SPVAT_cleansed_data
SET Mitigation = COALESCE(Mitigation, 'None provided')
WHERE Mitigation is NULL;

-- Set 'Maintenance' Class --

UPDATE SPVAT_cleansed_data
SET maintenance=1
WHERE apply_set_1==0 -- Only apply to train and validate sets
AND (Mitigation LIKE '%pm%' 
OR Mitigation LIKE '%thermography%' 
OR Mitigation LIKE '%rebuild%' 
OR Mitigation LIKE '%inspection%' 
OR Mitigation LIKE '%inspect%' 
OR Mitigation LIKE '%clean%' 
OR Mitigation LIKE '%maintain%' 
OR Mitigation LIKE '%replace%' 
OR Mitigation LIKE '%overhaul%' 
OR Mitigation LIKE '%calibrate%' 
OR Mitigation LIKE '%calibration%' 
OR Mitigation LIKE '%refurbish%' 
OR Mitigation LIKE '%test%' 
OR Mitigation LIKE '%check%'
OR Mitigation LIKE '%replacement%'
OR Mitigation LIKE '%preventative%'
OR Mitigation LIKE '%maintenance%');
-- OR Classification IS NOT NULL); -- If there is a Classification then it is maintenance, CANT do because mitigation won't see class in model

-- Set 'Operational' Class --

UPDATE SPVAT_cleansed_data
SET operational=1
WHERE apply_set_1==0
AND Mitigation NOT LIKE '%There are no activities that are performed%' 
AND (Mitigation LIKE '%Operator%' 
OR Mitigation LIKE '%operation%' 
OR Mitigation LIKE '%training%' 
OR Mitigation LIKE '%rounds%' 
OR Mitigation LIKE '%operations%' 
OR Mitigation LIKE '%procedure%' 
OR Mitigation LIKE '%operations/procedure%');

-- Set 'Design and Engineering' Class --

UPDATE SPVAT_cleansed_data
SET design_and_engineering=1
WHERE apply_set_1==0
AND (Mitigation LIKE '%Design%' 
OR Mitigation LIKE '%engineering%' 
OR Mitigation LIKE '%engineer%');

-- Set 'Physical Barriers' Class --

UPDATE SPVAT_cleansed_data
SET physical_barrier=1
WHERE apply_set_1==0 
AND Mitigation NOT LIKE '%Mtce Barriers: None%'
AND (Mitigation LIKE '%Mtce%' 
OR Mitigation LIKE '%barrier%' 
OR Mitigation LIKE '%wall%'
OR Mitigation LIKE '%railing%' 
OR Mitigation LIKE '%rail%');

-- Set 'Supply Chain' Class --

UPDATE SPVAT_cleansed_data
SET supply_chain=1
WHERE apply_set_1==0
AND Mitigation NOT LIKE '%Supply Barriers: No information found' -- avoid misclassifying
AND (Mitigation LIKE '%procurement%' 
OR Mitigation LIKE '%supply%' 
OR Mitigation LIKE '%chain%' 
OR Mitigation LIKE '%post manufacturing%' 
OR Mitigation LIKE '%manufacturing%');

-- Set 'Unknown' Class, this has to be done last --

UPDATE SPVAT_cleansed_data
SET unknown_mitigation=1
WHERE apply_set_1 == 0
AND maintenance == 0 AND operational == 0 AND design_and_engineering == 0 AND supply_chain == 0;

SELECT ROWID, Mitigation, Classification, maintenance, unknown_mitigation, train_set_1, validate_set_1, apply_set_1
FROM SPVAT_cleansed_data
WHERE apply_set_1 <> 1 AND Mitigation LIKE '%None%'
ORDER BY unknown_mitigation DESC;


