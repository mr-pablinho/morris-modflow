# -*- coding: utf-8 -*-
"""
Created on Mon May  3 19:58:51 2021
Edited on Mon May 17 11:08:53 2021
MORRIS method for sensitivity analysis -- 0) Model settings
@author: PMR
"""

# %% Import libraries and packages

import numpy as np


# %% Problem settings

numParameters = 16
numSP = 300
numRows = 260
numCols = 260
mySeed = 25

problem = {
    'num_vars': numParameters,
    'names': ['HK_SA', 'HK_SB', 'HK_SC',
              'SS_SA', 'SS_SB', 'SS_SC',
              'SY_SA', 'SY_SB', 'SY_SC',
              'RCH',
              'CON_CHA1', 'CON_CHA2', 
              'CON_RIV1', 'CON_RIV2', 'CON_RIV3',
              'STA'],
    'bounds': [[np.log10(1e-4), np.log10(1e-1)], [np.log10(1e-4), np.log10(1e-1)], [np.log10(1e-6), np.log10(1e-3)],
               [np.log10(1e-7), np.log10(1e-3)], [np.log10(1e-7), np.log10(1e-3)], [np.log10(1e-7), np.log10(1e-3)],
               [0.10, 0.40],[0.10, 0.40],[0.10, 0.40],
               [0, 2],
               [np.log10(1e-5), np.log10(9e-1)], [np.log10(1e-5), np.log10(9e-1)],
               [np.log10(1e-7), np.log10(9e-4)], [np.log10(1e-7), np.log10(9e-4)], [np.log10(1e-7), np.log10(9e-4)],
               [-0.145, 0.145]]
    }


# %% Morris sampling parameters

T = 10    # number of optimal trajectories to sample (between 2 and r) -- 10, 20, 30
p = 4     # p-level grid: number of grid levels (should be even) -- 4, 6, 8, 10
r = T+1   # r-trajectories: number of trajectories to generate

# define flag 
flag = '__morris__' + 'r' + str(r-1) + '_p' + str(p) 
print('Number of evaluations: ' + str((numParameters + 1) * T))