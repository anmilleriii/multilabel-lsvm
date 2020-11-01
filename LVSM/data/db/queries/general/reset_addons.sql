-- Reset added SPVAT fields --

UPDATE SPVAT_cleansed_data
SET maintenance = 0, operational = 0, design_and_engineering = 0, supply_chain = 0, unknown_mitigation = 0, train_set_1 =0, validate_set_1=0, apply_set_1=0;