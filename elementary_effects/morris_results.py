# -*- coding: utf-8 -*-
"""
Created on Mon May  3 19:58:51 2021
Edited on Mon May 17 11:08:53 2021
MORRIS method for sensitivity analysis -- 2) Morris analysis
@author: PMR
"""

# %% Import libraries and packages

import numpy as np
import matplotlib.pyplot as plt

from SALib.analyze import morris
from morris_init import numParameters, numSP, problem, flag, p
from f_names_flood import params_names_all, namPoints, params_names_short
from SALib.plotting.morris import horizontal_bar_plot
from f_color import *


# %% Extract and evaluate results


if __name__ == "__main__":

    # load samples and results
    
    Y = np.load('outputs_all/Y' + flag + '.npy')
    
    # compute paramters
    param_values = np.load('generated_parms/params' + flag + '.npy')
    
    
    # evaluate at every observation point and every stress period
    numObsPoints = int(21)
    Si_all_mu = np.zeros((numObsPoints, numSP, numParameters))
    Si_all_mu_star = np.zeros((numObsPoints, numSP, numParameters))
    Si_all_mu_star_conf = np.zeros((numObsPoints, numSP, numParameters))
    Si_all_sigma = np.zeros((numObsPoints, numSP, numParameters))
    
    
    for obs in range(numObsPoints):
        print('Morris analysis for observation point ' + str(obs+1) + '/' + str(numObsPoints))
        soo_mu = []
        soo_mu_star = []
        soo_mu_star_conf = []
        soo_sigma = []
        for sp in range(300):
            Yi = Y[obs][sp][:]
            Si = morris.analyze(problem, param_values, Yi, 
                                conf_level=0.95,
                                print_to_console=False,
                                num_levels=p, 
                                num_resamples=1000)
            soo_mu.append(Si['mu'][:]) 
            soo_mu_star.append(Si['mu_star'][:])
            soo_mu_star_conf.append(Si['mu_star_conf'][:])
            soo_sigma.append(Si['sigma'][:])
        Si_all_mu[obs] = np.array(soo_mu)
        Si_all_mu_star[obs] = np.array(soo_mu_star)
        Si_all_mu_star_conf[obs] = np.array(soo_mu_star_conf)
        Si_all_sigma[obs] = np.array(soo_sigma)
    
    # evaluate at specific period and specific observation point

    check_sp = 128  # 128: peak-flow
    check_obs = 10  # 10: house fw_AW_26, 1: well ALZPITZ
    
    Si = morris.analyze(problem, param_values, Y[check_obs][check_sp][:], 
                        conf_level=0.95, 
                        print_to_console=False, 
                        num_levels=p, 
                        num_resamples=1000)  
    
    np.save('./outputs_all/Si_all_mu' + flag, Si_all_mu)
    np.save('./outputs_all/Si_all_mu_star' + flag, Si_all_mu_star)
    np.save('./outputs_all/Si_all_mu_star_conf' + flag, Si_all_mu_star_conf)
    np.save('./outputs_all/Si_all_sigma' + flag, Si_all_sigma)
    
    
    # %% Print and plot results
      
    # (0) plot at specific phases of the event
    
    phase = {'before':     80,
             'peak':      128,
             'recession': 160,
             'after':     290}
    
    x_coord = np.arange(0, numParameters, 1)
    w = 0.20
    
    for obs in range(numObsPoints): 
        
        fig0, ax0 = plt.subplots(1, 1)
        ax0.set_title(namPoints[obs])
        
        ax0.bar(x_coord - .30, Si_all_mu_star[obs, phase['before'],:], width=w, label='before')
        ax0.bar(x_coord - .10, Si_all_mu_star[obs, phase['peak'],:], width=w, label='peak')
        ax0.bar(x_coord + .10, Si_all_mu_star[obs, phase['recession'],:], width=w, label='recession')
        ax0.bar(x_coord + .30, Si_all_mu_star[obs, phase['after'],:], width=w, label='after')
        
        ax0.set_xticks(x_coord)
        ax0.set_xticklabels(params_names_all, rotation=90, ha='center')
        ax0.set_ylim(0,5)
        ax0.legend(edgecolor='black', fancybox=False,
                   borderpad=0.8, handletextpad=0.95, labelspacing=0.65)
        
        fig0.set_size_inches(8, 3.5)
        fig0.savefig('./figures/bar_plot_' + str(obs+1) + '__' + flag, dpi=300, bbox_inches='tight')
        
        
    # (1) plot ranking using SALib library (at specific space and time)
    
    fig1, ax1 = plt.subplots(1, 1)
    horizontal_bar_plot(ax1, Si, {}, sortby='mu_star', unit=r"")
    fig1.savefig('./figures/horizontal_plot' + flag, dpi=300, bbox_inches='tight')
    
    # (2) plot linearity using SALib library (at specific space and time)
    
    markers = ['o', 'o', 'o', 
               'P', 'P', 'P',
               '+', '+', '+', 
               'X', 
               's', 's', 
               'D', 'D', 'D',
               'v']
    
    fig2, ax2 = plt.subplots(1, 1)   
    for ip in range(len(params_names_all)):
        ax2.scatter(Si['mu_star'][ip], Si['sigma'][ip], s=50, alpha=0.5, marker=markers[ip], label=params_names_all[ip])
    ax2.set_xlabel(r'$\mu^\star$')
    ax2.set_ylabel(r'$\sigma$')
    ax2.set_xlim(0,)
    ax2.set_ylim(0,)
    
    x_axis_bounds = np.array(ax2.get_xlim())
    ax2.plot(x_axis_bounds, x_axis_bounds, 
             linestyle='-', color='black', alpha=0.5,
             label=r'$\sigma / \mu^{\star} = 1.0$')
    ax2.plot(x_axis_bounds, 0.5 * x_axis_bounds, 
             linestyle='--', color='black', alpha=0.5,
             label=r'$\sigma / \mu^{\star} = 0.5$')
    ax2.plot(x_axis_bounds, 0.1 * x_axis_bounds, 
             linestyle='-.', color='black', alpha=0.5, 
             label=r'$\sigma / \mu^{\star} = 0.1$')

    ax2.legend(bbox_to_anchor=(1.01, 1),
               edgecolor='black', fancybox=False, fontsize=8.5,
               borderpad=0.8, handletextpad=0.9, labelspacing=0.65)
    
    fig2.savefig('./figures/covariance_plot' + flag, dpi=300, bbox_inches='tight')
    
    # (3) plot along time
    
    lines = ['-', '-', '-', '-',
             '--', '--','--','--','--','--','--','--','--','--',
             ':', ':', ':', ':', ':', ':', ':']
    
    for i in range(numParameters):
        check_param = i
        fig3, ax3 = plt.subplots(1, 1)
        ax3.set_title('Sensitivity along time - ' + params_names_all[i])
        [ax3.plot(Si_all_sigma[oo][:,check_param], 
                  label=namPoints[oo], linestyle=lines[oo], alpha=0.75, linewidth=1.2) for oo in range(numObsPoints)]
        ax3.legend(title=None, fontsize=7, loc='upper right', 
                   bbox_to_anchor=(1.2, 0.95),
                   edgecolor='black', fancybox=False,
                   borderpad=0.8, handletextpad=0.95, labelspacing=0.65)
        ax3.set_xlim(0,300)
        fig3.savefig('./figures/time_plot_' + str(i+1) + '__' + flag, dpi=300, bbox_inches='tight')


