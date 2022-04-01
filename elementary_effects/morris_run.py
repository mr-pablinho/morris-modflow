# -*- coding: utf-8 -*-
'''
Created on Mon May  3 19:58:51 2021
Edited on Mon May 17 11:08:53 2021
MORRIS method for sensitivity analysis -- 1) Generate parameters and run MODFLOW
@author: PMR
'''

# %% Import libraries and packages

from SALib.sample.morris import sample
import numpy as np
import matplotlib.pyplot as plt
import f_runModflow as rm
from morris_init import numParameters, numSP, problem, r, p, T, mySeed, numRows, numCols, flag
import f_color as fc


# %% Run Morris using MODFLOW-2005


if __name__ == "__main__":

    # compute paramEters
    param_values = sample(problem, N=r, num_levels=p, optimal_trajectories=T, seed=mySeed)  
    numEvals = len(param_values)
    
    # correction to include logaritmic parameters
    log_parameters = [0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14]
    
    param_values_model = np.zeros((numEvals, numParameters))
    param_values_model[:,:] = param_values[:,:]
    
    for i in log_parameters:
        param_values_model[:,i] = 10 ** param_values[:,i]
        
    
    
    # %% Plot samples
    
    coord_evals = np.linspace(1, numEvals, numEvals)
    for i in range(numParameters):
        plt.figure(str(i))
        
        plt.subplot(1, 2, 1)
        plt.scatter(coord_evals, param_values[:,i], alpha=0.5, color=fc.redruby)
        plt.title('Sample per evaluation')
        plt.xlabel('number of evaluation')
        plt.ylabel('parameter value')
        plt.ylim(problem['bounds'][i][0], problem['bounds'][i][1])
        plt.xlim(0, numEvals)
        
        plt.subplot(1, 2, 2)
        plt.hist(param_values[:,i], p, color=fc.bluecorn)
        plt.title('Frequency')
        plt.xlabel('parameter value')
        plt.xlim(problem['bounds'][i][0], problem['bounds'][i][1])
        plt.ylim(0, 200)
    
        plt.suptitle(problem['names'][i])
        
    
    # %% Run function 
    
    # create storage array
    Y = np.zeros(numEvals)
    
    # run groundwater model
    Y = rm.runModflow(param_values_model, numEvals, numSP, numRows, numCols, flag)
    
    
    # %% Save model outcomes
    
    np.save('outputs_all/Y' + flag, Y)
    np.save('generated_parms/params' + flag, param_values)


