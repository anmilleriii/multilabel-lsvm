'''
Clean 'Component', 'Fleet', 'System', 'Mitigation' fields and output csv.
TODO: Refine.

# Author
@ Al Miller

# License
MIT License 2020
'''
# Import libraries and define functions
import re
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# Function to make all strings lowercase and replace spaces with underscores
def format_df (df):
    df = df.applymap(lambda s:s.lower() if type(s) == str else s)
    df.replace(' ', '_', regex=True, inplace = True)
    df = df.fillna('')
    return df

# Function to remove underscores and replace with spaces
def fix_text(df):
    df.replace('_',' ', inplace=True, regex=True)
    return df
    
# Plot parameters
plt.rcParams["figure.figsize"]=10,10
plt.rcParams['font.size'] =14
plt.rcParams['axes.labelsize']=14
plt.rcParams['figure.facecolor']='#ffffff'
plt.rcParams['grid.color'] = '#d3d3d3'
plt.rcParams['grid.linestyle'] = ':'

# Import the uncleansed CSV file
filename = './in/equipment_data_for_cleansing.csv'
df = pd.read_csv(filename, encoding = 'ISO-8859-1', dtype= str)

# Remove '_x00D_' endline characters and extra blank lines from free form fields
df['Basis'].replace('(?<=[a-z]|\))_x000D_',':',inplace=True, regex=True)
df['Basis'].replace('_x000D_|\?|!|_x000',' ',inplace=True, regex=True)
df['Basis'].replace('\n\s','',inplace=True, regex=True)

df['Mitigation'].replace('(?<=[a-z]|\))_x000D_',':',inplace=True, regex=True)
df['Mitigation'].replace('_x000D_|\?|!|_x000',' ',inplace=True, regex=True)
df['Mitigation'].replace('\n\s','',inplace=True, regex=True)

df['Elimination'].replace('(?<=[a-z]|\))_x000D_',':',inplace=True, regex=True)
df['Elimination'].replace('_x000D_|\?|!|_x000',' ',inplace=True, regex=True)
df['Elimination'].replace('\n\s','',inplace=True, regex=True)

df['NewComponent']=''
df['Method']=''
df['NewSystem']=''

'''
Fix 'Component' Name
'''

df2 = df
df2['ComponentDesc'].apply(str)
df2 = df2.fillna('')

#Create a smaller dataframe containing only the unspecified equipment entries and a new blank column

unspecified = df2[df2['Component']=='unspecified_equipment']

''' This block assigns component names to a column called New Component. If the component description column 
    contains the string it assigns the dictionary key. '''

comp_dict = {'fuse': ['fuse','fusible'],
             'fan':['fan'],
             'dampers_&_ducting':['damper'],
             'battery':['battery'],
             'condenser':['condenser'],
             'pipe':['pipe', 'flex_hose$','^flex_hose'],
             'rod_drive_mechanism':['crdm','control_rod_drive','control_element_drive'],
             'circuit_breaker':['breaker'],
             'transformers': ['transformer','xfmr'],
             'pump':['rcp'],
             'turbine_(steam)':['turbine', 'turb', 'lp', 'hp'],
             'pump':['pump', 'pmp'],
             'heat_exchanger':['cooler[s]*','_clr'],
             'motor':['motor','mtr_winding'],
             'tank':['tank'],
             'circuit_breaker':['cubicle','bkr','circuit_breaker'],
             'control_switch':['cntl_s','control_switch','ctrl_sw','sel_sw','isol_switch'],
             'contactor':['contactor','aux_cont_'],
             'valve':['valve','vlv'],
             'flow_switch':['flow_switch'],
             'relay':['relay','_rly','grnd_overcurrent','gnd_overcurrent'],
             'junction_box':['junction_box'],
             'expansion_joint':['expansion_joint','exp_joint','flex_joint'],
             'positioner':['^positioner','positioner$', 'posnr$'],
             'pressure_switch':['pressure_switch'],
             'vibration_monitor':['vibration_monitor'],
             'steam_jet_air_ejector':['steam_jet_air','steam_air_ejector','steam_jet_air_ejector']
        }
                         
comp_dict3 = {'transformers':['transformer'],
              'expansion_joint':['expansion_joint'],}

for i in comp_dict:
    list = comp_dict[i]
    pattern = '|'.join(list)
    unspecified.NewComponent.loc[unspecified.ComponentDesc.str.contains(pattern,case=False,na=False, regex=True)] = i
    
for i in comp_dict3:
    list3 = comp_dict3[i]
    pattern = '|'.join(list3)
    unspecified.NewComponent.loc[unspecified.Subcomponent.str.contains(pattern,case=False,na=False, regex = True)] = i
    
# Assign 'NewComponent' categories to unspecified equipment
unspecified.NewComponent = unspecified.NewComponent.apply(lambda x: 'unspecified_equipment' if x =='' else x ) 
unspecified.Component = unspecified.NewComponent
df2[df2['Component'] == 'unspecified_equipment'] = unspecified


# Assign Grouped Component Names to match IRIS

df2.Component.loc[(df2.Component == 'accumulator')|(df2.Component == 'tank')] = 'accumulators,_tanks,_air_receivers'
df2.Component.loc[(df2.Component == 'air_dryer')] = 'air_dryers,_dehumidifiers'
df2.Component.loc[(df2.Component == 'annunciator_module')|(df2.Component == 'alarm')] = 'annunciator_modules,_alarms'
df2.Component.loc[(df2.Component == 'battery')|(df2.Component == 'battery_-_charger')] = 'batteries,_battery_chargers'
df2.Component.loc[(df2.Component == 'bistable')|(df2.Component == 'switch')|(df2.Component == 'i&c_-_temperature_switch')|(df2.Component == 'control_switch')|(df2.Component == 'pressure_switch')|(df2.Component == 'i&c_-_pressure_switch')|(df2.Component == 'flow_switch')] = 'bistable,_switch_(mechanical,_electronic)'
df2.Component.loc[(df2.Component == 'compressor')|(df2.Component == 'cooling_tower')|(df2.Component == 'air_handling_equipment')|(df2.Component == 'fan')|(df2.Component == 'cooling_unit')|(df2.Component == 'vacuum_pump')] = 'blowers,_compressors,_fans,_vacuum_pumps,_cooling_units'
df2.Component.loc[(df2.Component == 'heating_vessel')] = 'boilers,_heating_vessels,_excluding_reactor_vessels'
df2.Component.loc[(df2.Component == 'circuit_breaker')|(df2.Component == 'switchgear')|(df2.Component == 'switchgear_-_motor_control_centers')|(df2.Component == 'circuit_breaker_-_substation')|(df2.Component == 'contactor')|(df2.Component=='motor_controller')|(df2.Component=='manual_switch')|(df2.Component == 'fuse')|(df2.Component == 'circuit_card')] = 'circuit_breakers,_contactors,_motor_controllers,_manual_switches'
df2.Component.loc[(df2.Component == 'control_panel')] = 'control_board/panel'
df2.Component.loc[(df2.Component == 'control_rod')|(df2.Component == 'control_element_assembly')] = 'control_rods,_control_element_assemblies'
df2.Component.loc[(df2.Component == 'crane')] = 'crane,_hoist,_or_lifting_device'       
df2.Component.loc[(df2.Component == 'demineralizer')|(df2.Component == 'ion_exchanger')] = 'demineralizers,_ion_exchangers'
df2.Component.loc[(df2.Component == 'feedwater_heater')] = 'electric_heaters'
df2.Component.loc[(df2.Component == 'bus')|(df2.Component == 'cable')|(df2.Component == 'junction_box')|(df2.Component == 'electrical_conductor')] = 'electrical_conductors,_bus,_cable,_wire'
df2.Component.loc[(df2.Component == 'i&c_-_capacitor_-_electrolytic')|(df2.Component == 'i&c_-_dc_power_supply')] = 'electronic_power_supply'
df2.Component.loc[(df2.Component == 'diesel_engine')] = 'engines_(gas,_diesel)'
df2.Component.loc[(df2.Component == 'filter')|(df2.Component == 'strainer')|(df2.Component == 'water_intake_screen')] = 'filters,_strainers,_screens'
# floor (none)
# roof (none)
df2.Component.loc[(df2.Component == 'generator')|(df2.Component == 'inverter')|(df2.Component == 'motor_generator')|(df2.Component == 'main_generator_-_exciter')]='generators,_inverters,_motor_generators'
df2.Component.loc[(df2.Component == 'governor')|(df2.Component == 'fluid_drive')|(df2.Component == 'coupling')|(df2.Component == 'gearbox')|(df2.Component=='gearbox_with_cooler')]='governors,_couplings,_gear_boxes'
df2.Component.loc[(df2.Component == 'heat_exchanger')|(df2.Component == 'condenser')|(df2.Component == 'steam_jet_air_ejector')|(df2.Component == 'steam_generator')] = 'heat_exchanger,_condenser,_steam_generator'
#Illumination Source (None)
df2.Component.loc[(df2.Component == 'indicator')|(df2.Component == 'recorder')|(df2.Component == 'gauge')] = 'indicators,_recorders,_gauges'
df2.Component.loc[(df2.Component == 'positioner')|(df2.Component == 'i&c_-_analog_electronic_controller')|(df2.Component == 'i&c_-_positioner')|(df2.Component == 'i&c_-_booster')|(df2.Component == 'i&c_-_pneumatic_controller')|(df.Component == 'i&c_-_pressure_regulator')|(df.Component == 'i&c_-_signal_conditioner')] = 'instrument_controllers'
# integrator/computation module OK
# isolation devices ok
# landscaping (none)
# Manual tools (none)
df2.Component.loc[(df2.Component == 'motor')|(df2.Component == 'motor_(electric)')|(df2.Component == 'motor_(hydraulic)')|(df2.Component == 'motors_(electric)')|(df2.Component == 'motors_(hydraulic)')] = 'motors_(electric,_hydraulic,_pneumatic)'
df2.Component.loc[(df2.Component == 'penetration')] = 'penetrations,_air_locks,_hatches'
df2.Component.loc[(df2.Component == 'pipe')|(df2.Component == 'fitting')|(df2.Component == 'expansion_joint')|(df2.Component == 'rupture_disc')] = 'pipes,_fittings,_rupture_discs'
# Power Tools (None)
df2.Component.loc[(df2.Component == 'pressure_vessel')|(df2.Component == 'pressurizer')|(df2.Component == 'reactor_vessel')] = 'pressure_vessel,_reactor_vessel,_pressurizer'
# Process Fluid (None)
df2.Component.loc[(df2.Component == 'pump')|(df2.Component == 'pump_-_vertical')|(df2.Component == 'lube_oil_pump')] = 'pumps,_eductors'
# Recombiners (None)
df2.Component.loc[(df2.Component.str.contains('relay', case=False))] = 'relays'
df2.Component.loc[(df2.Component == 'rod_drive_mechanism')] = 'rod_drive_mechanism,_hydraulic_control_unit'
# Room (None)
# Software (None)
df2.Component.loc[(df2.Component == 'support')] = 'supports,_hangers,_snubbers'
df2.Component.loc[(df2.Component == 'transformers')|(df2.Component == 'voltage_regulator')|(df2.Component == 'shunt_reactor')] = 'transformers,_shunt_reactors'
#Transient Combustible (None)
df2.Component.loc[(df2.Component == 'transmitter')|(df2.Component == 'i&c_-_i/p_and_e/p_transducer')|(df2.Component == 'i&c_-_pressure_sensor_and_transmitter')|(df2.Component == 'radiation_monitor')|(df2.Component == 'vibration_monitor')|(df2.Component == 'detector')] = 'transmitters,_detectors,_elements'
df2.Component.loc[(df2.Component == 'turbine_(steam)')|(df2.Component == 'main_turbine')|(df2.Component == 'main_turbine_-_ehc_hydraulics')|(df2.Component == 'main_turbine_-_mhc_controls')|(df2.Component == 'main_turbine_-_trip_system')]= 'turbines_(steam,_gas)'
df2.Component.loc[(df2.Component == 'valve_actuator')] = 'valve_operators'
df2.Component.loc[(df2.Component == 'valve')|(df2.Component=='valve_-_air_operated')|(df2.Component == 'valve_-_air_operated_-_aov_-_piston')|(df2.Component=='valve_-_ball')|(df2.Component == 'valve_-_check')|(df2.Component=='valve_-_gate')|(df2.Component == 'valve_-_globe')|(df2.Component=='valve_-_motor_operated')|(df2.Component == 'valve_-_power_operated_relief')|(df2.Component=='valve_-_pressure_relief')|(df2.Component == 'valve_-_solenoid_operated')|(df2.Component=='valve_-_steam_turbine')|(df2.Component == 'dampers_&_ducting')]= 'valves,_dampers'
# Vehicle (None)
# Wall (None)
# Waste Bin (None)
# Working Fluid (None)

# Assign new component names to original dataframe
df.NewComponent = df2['Component']

# # Output Final Cleansed csv File

df3 = df
df3 = df3.replace('_',' ',regex= True)
df3.NewComponent = df.NewComponent.str.title()
df3.NewSystem=df3.NewSystem.str.title()

df3.to_csv('cleansed_equipment_data.csv')




















# # Search for a system using this: 
# #df.loc[df.NewSystem.str.contains('main_generator_system',regex=True)].groupby(['NewSystem','NewComponent','Method']).size()

# #Outputs only results used in Table.  Percentages were calculated in excel.  see Table 3_2 and Table 3_3.xlsx
# dictionary = {'feedwater_system':['valves,_dampers','valve_operators','pumps,_eductors','instrument_controllers'], 
#         'mainreheat_steam_system':['valves,_dampers','valve_operators','pipes,_fittings,_rupture_discs','instrument_controllers'],
#               'main_generator_output_power_system':['transformers,_shunt_reactors','relays','electrical_conductors,_bus,_cable,_wire','generators,_inverters,_motor_generators','circuit_breakers,_contactors,_motor_controllers,_manual_switches'],
#               'medium_voltage_power_sys':['generators,_inverters,_motor_generators','circuit_breakers,_contactors,_motor_controllers,_manual_switches','relays','transformers,_shunt_reactors'],
#               'main_generator_system':['relays','generators,_inverters,_motor_generators','instrument_controllers','transformers,_shunt_reactors'],
#               'main_turbine_system':['turbines_(steam,_gas)','instrument_controllers','valve_operators','valves,_dampers'],
#               'reactor_coolant_system':['motors_(electric,_hydraulic,_pneumatic)','circuit_breakers,_contactors,_motor_controllers,_manual_switches','valves,_dampers','pumps,_eductors'],
#               'condensate_system':['heat_exchanger,_condenser,_steam_generator','motors_(electric,_hydraulic,_pneumatic)','pumps,_eductors']  }

# for i in dictionary:
#     print('\n',i,'\n')
#     for j in dictionary[i]:
#         print(df.loc[(df.NewSystem.str.contains(i) & df.NewComponent.str.contains(j))].groupby(['NewSystem','NewComponent','Method']).size())
 
# # Print the remaining systems where component will not display
# print('\n','main_turbine_system','\n',df.loc[df.NewSystem.str.contains('main_turbine_system',regex=True)].groupby(['NewSystem','NewComponent','Method']).size())
# print('\n','reactor_coolant_system','\n',df.loc[df.NewSystem.str.contains('reactor_coolant_system',regex=True)].groupby(['NewSystem','NewComponent','Method']).size())
# print('\n','condensate_system','\n',df.loc[df.NewSystem.str.contains('condensate_system',regex=True)].groupby(['NewSystem','NewComponent','Method']).size())

'''
SPV Mitigation strategy heatmap
'''

# # # Table 3-2: SPV Mitigation Strategy Category Heatmap

# 


# # Search for a system using this: 
# #df.loc[df.NewSystem.str.contains('main_generator_system',regex=True)].groupby(['NewSystem','NewComponent','Method']).size()

# #Outputs only results used in Table.  Percentages were calculated in excel.  see Table 3_2 and Table 3_3.xlsx
# dictionary = {'feedwater_system':['valves,_dampers','valve_operators','pumps,_eductors','instrument_controllers'], 
#         'mainreheat_steam_system':['valves,_dampers','valve_operators','pipes,_fittings,_rupture_discs','instrument_controllers'],
#               'main_generator_output_power_system':['transformers,_shunt_reactors','relays','electrical_conductors,_bus,_cable,_wire','generators,_inverters,_motor_generators','circuit_breakers,_contactors,_motor_controllers,_manual_switches'],
#               'medium_voltage_power_sys':['generators,_inverters,_motor_generators','circuit_breakers,_contactors,_motor_controllers,_manual_switches','relays','transformers,_shunt_reactors'],
#               'main_generator_system':['relays','generators,_inverters,_motor_generators','instrument_controllers','transformers,_shunt_reactors'],
#               'main_turbine_system':['turbines_(steam,_gas)','instrument_controllers','valve_operators','valves,_dampers'],
#               'reactor_coolant_system':['motors_(electric,_hydraulic,_pneumatic)','circuit_breakers,_contactors,_motor_controllers,_manual_switches','valves,_dampers','pumps,_eductors'],
#               'condensate_system':['heat_exchanger,_condenser,_steam_generator','motors_(electric,_hydraulic,_pneumatic)','pumps,_eductors']  }

# for i in dictionary:
#     print('\n',i,'\n')
#     for j in dictionary[i]:
#         print(df.loc[(df.NewSystem.str.contains(i) & df.NewComponent.str.contains(j))].groupby(['NewSystem','NewComponent','Method']).size())
 
# # Print the remaining systems where component will not display
# print('\n','main_turbine_system','\n',df.loc[df.NewSystem.str.contains('main_turbine_system',regex=True)].groupby(['NewSystem','NewComponent','Method']).size())
# print('\n','reactor_coolant_system','\n',df.loc[df.NewSystem.str.contains('reactor_coolant_system',regex=True)].groupby(['NewSystem','NewComponent','Method']).size())
# print('\n','condensate_system','\n',df.loc[df.NewSystem.str.contains('condensate_system',regex=True)].groupby(['NewSystem','NewComponent','Method']).size())


'''
Mitigation Strategy by Fleet
'''

# # # Table 3-3 Mitigation Strategy Categories by Fleet



# fleetlist=df.Fleet.unique()

# for i in fleetlist:
#     number = df.loc[df.Fleet==i].Method.value_counts()/sum(df.loc[df.Fleet==i].Method.value_counts()) * 100
#     print(i,'\n',number)
# fleet_plot.ScramScaled

