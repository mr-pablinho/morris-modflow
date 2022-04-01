# -*- coding: utf-8 -*-
"""
Created on Mon May 31 06:55:21 2021
Names of monitoring wells, monitored houses and evaluation points
@author: PMR
"""

namPoints = [# observation location
             'ALZPITZ', 'B1', 'B3', 'B4',
             # flood points
             'FP-JS-3', 'FP-PS-3', 'FP-GS-10', 'FP-FS-6', 'FP-WW-9', 'FP-EW-16', 'FP-AW-26', 'FP-BW-26', 'FP-NW-17', 'FP-NW-15',
             # evaluation points 
             'EP-1', 'EP-2', 'EP-3', 'EP-4', 'EP-5', 'EP-6', 'EP-7'
             ]

params_data = ['Hyd. conductivity - SA [m/s] (log scale)',
               'Hyd. conductivity - SB [m/s] (log scale)',
               'Specific yield - SA [-]', 
               'Specific yield - SB [-]', 
               'Recharge multiplier [-]', 
               'Canal bed conductance - S1 [m$^2$/s] (log scale)', 
               'Canal bed conductance - S2 [m$^2$/s] (log scale)', 
               'River bed conductance - S1 [m$^2$/s] (log scale)', 
               'River bed conductance - S2 [m$^2$/s] (log scale)', 
               'River bed conductance - S3 [m$^2$/s] (log scale)', 
               'River stage variation [m]'
               ]

params_data_all = ['Hyd. conductivity - SA [m/s] (log scale)',
               'Hyd. conductivity - SB [m/s] (log scale)',
               'Hyd. conductivity - SC [m/s] (log scale)',
               'Specific storage - SA [-]', 
               'Specific storage - SB [-]', 
               'Specific storage - SC [-]',
               'Specific yield - SA [-]', 
               'Specific yield - SB [-]', 
               'Specific yield - SC [-]',
               'Recharge multiplier [-]', 
               'Canal bed conductance - S1 [m$^2$/s] (log scale)', 
               'Canal bed conductance - S2 [m$^2$/s] (log scale)', 
               'River bed conductance - S1 [m$^2$/s] (log scale)', 
               'River bed conductance - S2 [m$^2$/s] (log scale)', 
               'River bed conductance - S3 [m$^2$/s] (log scale)', 
               'River stage variation [m]'
               ]

params_names_all = ['Hyd. conductivity - SA',
                    'Hyd. conductivity - SB',
                    'Hyd. conductivity - SC',
                    'Specific storage - SA', 
                    'Specific storage - SB', 
                    'Specific storage - SC',
                    'Specific yield - SA', 
                    'Specific yield - SB', 
                    'Specific yield - SC',
                    'Recharge multiplier', 
                    'Canal bed conductance - S1', 
                    'Canal bed conductance - S2', 
                    'River bed conductance - S1', 
                    'River bed conductance - S2', 
                    'River bed conductance - S3', 
                    'River stage variation'
                    ]
                    
params_names_short = ['HK_SA', 'HK_SB', 'HK_SC',
                      'SS_SA', 'SS_SB', 'SS_SC', 
                      'SY_SA', 'SY_SB', 'SY_SC', 
                      'RCH', 
                      'CON_CHA1', 'CON_CHA2', 
                      'CON_RIV1', 'CON_RIV2', 'CON_RIV3', 
                      'STA']