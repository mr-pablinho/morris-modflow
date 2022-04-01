# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 21:49:35 2021
FUNCTION FOR MODFLOW
@author: PMR
"""

# %% Libraries

import f_editor as fed
import f_riverpackage as friv
import flopy as fp
import numpy as np
import os
import sys
from shutil import copyfile


# %% Observation points and data

# observation location
obsPoint_alzpitz = [157, 158]
obsPoint_b1 =      [218,  98]
obsPoint_b3 =      [127, 159]
obsPoint_b4 =      [ 39, 123]

# flood points
fp_JS_3  = [6, 88]
fp_PS_3  = [40, 96]
fp_GS_10 = [54, 118]
fp_FS_6  = [80, 76]
fp_WW_9  = [106, 98]
fp_EW_16 = [140, 82]
fp_AW_26 = [150, 132]
fp_BW_26 = [170, 108]
fp_NW_17 = [252, 174]
fp_NW_15 = [252, 162]

# evaluation points 
ep_1 = [113, 179]
ep_2 = [145, 163]
ep_3 = [171, 157]
ep_4 = [185, 165]
ep_5 = [204, 167]
ep_6 = [157, 176]
ep_7 = [157, 200]


# %% Define mask texts 

# multiple file (lpf_mult.dat)
modflowMultFile_editable = "pmr_ip_lpf_editable_sa.dat"
modflowMultFile_processed = "pmr_ip_lpf_sa.dat"
textToReplace_hk_1 = "**hk_01**"
textToReplace_hk_2 = "**hk_02**"
textToReplace_hk_3 = "**hk_03**"
textToReplace_ss_1 = "**ss_01**"
textToReplace_ss_2 = "**ss_02**"
textToReplace_ss_3 = "**ss_03**"
textToReplace_sy_1 = "**sy_01**"
textToReplace_sy_2 = "**sy_02**"
textToReplace_sy_3 = "**sy_03**"

# river package values (riv6.dat)
modflowRiverFile_editable = "pmr_bc_riv_editable_sa.dat"
modflowRiverFile_processed = "pmr_bc_riv_sa.dat"

# vectors and for river file
numActiveCells = 3849
vectorLayer = friv.importVector_integer('inputs/array_layer_1sp.txt')
vectorRow = friv.importVector_integer('inputs/array_row_1sp.txt')
vectorColumn = friv.importVector_integer('inputs/array_col_1sp.txt')
vectorCondText = friv.importVector_string('inputs/array_cond_2sections_1sp.txt')
vectorBedBottom = friv.importVector_float('inputs/array_bedBot_1sp.txt')
vectorStageBase = friv.importVector_float('inputs/array_stages_300sp.txt')

# recharge package values (rch6.dat)
modflowRechargeFile_processed = "pmr_bc_rch_sa.dat"
base_rch_array = np.load("inputs/rch_array.npy")


# create log file
log_file = open("./logs/log" + "flag" + ".txt", "w+")
log_file.truncate(0)
log_file.close()






# %% Function to calculate the vectors


def runModflow(Mat, numSamples, numSP, numRows, numCols, flag):
    
    # Create container matrices
    fMat_al =    np.zeros((numSP, numSamples))
    fMat_b1 =    np.zeros((numSP, numSamples))
    fMat_b3 =    np.zeros((numSP, numSamples))
    fMat_b4 =    np.zeros((numSP, numSamples))
    
    fMat_JS_3  = np.zeros((numSP, numSamples))
    fMat_PS_3  = np.zeros((numSP, numSamples))
    fMat_GS_10 = np.zeros((numSP, numSamples))
    fMat_FS_6  = np.zeros((numSP, numSamples))
    fMat_WW_9  = np.zeros((numSP, numSamples))
    fMat_EW_16 = np.zeros((numSP, numSamples))
    fMat_AW_26 = np.zeros((numSP, numSamples))
    fMat_BW_26 = np.zeros((numSP, numSamples))
    fMat_NW_17 = np.zeros((numSP, numSamples))
    fMat_NW_15 = np.zeros((numSP, numSamples))
    
    fMat_ep_1 = np.zeros((numSP, numSamples))
    fMat_ep_2 = np.zeros((numSP, numSamples))
    fMat_ep_3 = np.zeros((numSP, numSamples))
    fMat_ep_4 = np.zeros((numSP, numSamples))
    fMat_ep_5 = np.zeros((numSP, numSamples))
    fMat_ep_6 = np.zeros((numSP, numSamples))
    fMat_ep_7 = np.zeros((numSP, numSamples))
    
    log_file = open("./logs/log" + flag + ".txt", "w+")
    log_file.truncate(0)

    
    for i in range(numSamples):
                         
        # give format for printing in file hydraulic parameters
        value_hk_1 = "{:1.7E}".format(Mat[i,0])
        value_hk_2 = "{:1.7E}".format(Mat[i,1])
        value_hk_3 = "{:1.7E}".format(Mat[i,2])    
        value_ss_1 = "{:1.7E}".format(Mat[i,3])
        value_ss_2 = "{:1.7E}".format(Mat[i,4])
        value_ss_3 = "{:1.7E}".format(Mat[i,5])
        value_sy_1 = "{:1.7E}".format(Mat[i,6])  
        value_sy_2 = "{:1.7E}".format(Mat[i,7])  
        value_sy_3 = "{:1.7E}".format(Mat[i,8])  
        
        # boundary conditions
        rch_multiplier = Mat[i,9]
        rch_array_run = base_rch_array * rch_multiplier
        
        valueConductance_cha_1 = "{:1.7e}".format(Mat[i,10])
        valueConductance_cha_2 = "{:1.7e}".format(Mat[i,11])
        valueConductance_riv_1 = "{:1.7e}".format(Mat[i,12])
        valueConductance_riv_2 = "{:1.7e}".format(Mat[i,13])
        valueConductance_riv_3 = "{:1.7e}".format(Mat[i,14])
        
        coeffStage = Mat[i,15]
        vectorStage = vectorStageBase + coeffStage
        
        friv.createRiverPackage(modflowRiverFile_editable, numActiveCells, numSP, 
                                vectorStage, 
                                vectorLayer, vectorRow, vectorColumn, 
                                vectorCondText, vectorBedBottom)
         
        # copy and rename to protect mask files
        copyfile(modflowMultFile_editable, modflowMultFile_processed)
        copyfile(modflowRiverFile_editable, modflowRiverFile_processed)
        
        # find and replace text to edit parameters
        fed.rewrite_mask(modflowMultFile_processed, textToReplace_hk_1, value_hk_1)
        fed.rewrite_mask(modflowMultFile_processed, textToReplace_hk_2, value_hk_2)
        fed.rewrite_mask(modflowMultFile_processed, textToReplace_hk_3, value_hk_3)
        
        fed.rewrite_mask(modflowMultFile_processed, textToReplace_ss_1, value_ss_1)
        fed.rewrite_mask(modflowMultFile_processed, textToReplace_ss_2, value_ss_2)
        fed.rewrite_mask(modflowMultFile_processed, textToReplace_ss_3, value_ss_3)
        
        fed.rewrite_mask(modflowMultFile_processed, textToReplace_sy_1, value_sy_1)
        fed.rewrite_mask(modflowMultFile_processed, textToReplace_sy_2, value_sy_2)
        fed.rewrite_mask(modflowMultFile_processed, textToReplace_sy_3, value_sy_3)
        
        # create recharge package file        
        fed.createRechargePackage(rch_array_run, modflowRechargeFile_processed, numSP, numRows, numCols)
        
        # create river package file    
        fed.rewrite_mask(modflowRiverFile_processed, '**cha_01**', valueConductance_cha_1)
        fed.rewrite_mask(modflowRiverFile_processed, '**cha_02**', valueConductance_cha_2)          
        fed.rewrite_mask(modflowRiverFile_processed, '**riv_01**', valueConductance_riv_1)
        fed.rewrite_mask(modflowRiverFile_processed, '**riv_02**', valueConductance_riv_2)
        fed.rewrite_mask(modflowRiverFile_processed, '**riv_03**', valueConductance_riv_3)

        # run MODFLOW model
        success = fp.run_model("MODFLOW_mod_sa.BAT", "mod_sa.nam") 
        
        if success[0] == True:
            check_success = 'Finished ' + str(i+1) + ' of ' + str(numSamples)
        else:
            check_success = 'Error at ' + str(i+1) + ' of ' + str(numSamples)
            
        log_file = open("./logs/log" + flag + ".txt", "a")
        log_file.write(check_success + '\n')
        log_file.close()
        
        
    # save all the results of all the simulations
        storeHeads = np.loadtxt("pmr_op_heads_sa.dat") 
        
        # extract results at observation points
        fMat_al[:,i] = fed.extract_at(storeHeads, obsPoint_alzpitz, numSP, numRows)
        fMat_b1[:,i] = fed.extract_at(storeHeads, obsPoint_b1, numSP, numRows)
        fMat_b3[:,i] = fed.extract_at(storeHeads, obsPoint_b3, numSP, numRows)
        fMat_b4[:,i] = fed.extract_at(storeHeads, obsPoint_b4, numSP, numRows)
        
        fMat_JS_3[:,i]  = fed.extract_at(storeHeads, fp_JS_3 , numSP, numRows)
        fMat_PS_3[:,i]  = fed.extract_at(storeHeads, fp_PS_3 , numSP, numRows)
        fMat_GS_10[:,i] = fed.extract_at(storeHeads, fp_GS_10, numSP, numRows)
        fMat_FS_6[:,i]  = fed.extract_at(storeHeads, fp_FS_6 , numSP, numRows)
        fMat_WW_9[:,i]  = fed.extract_at(storeHeads, fp_WW_9 , numSP, numRows)
        fMat_EW_16[:,i] = fed.extract_at(storeHeads, fp_EW_16, numSP, numRows)
        fMat_AW_26[:,i] = fed.extract_at(storeHeads, fp_AW_26, numSP, numRows)
        fMat_BW_26[:,i] = fed.extract_at(storeHeads, fp_BW_26, numSP, numRows)
        fMat_NW_17[:,i] = fed.extract_at(storeHeads, fp_NW_17, numSP, numRows)
        fMat_NW_15[:,i] = fed.extract_at(storeHeads, fp_NW_15, numSP, numRows)
        
        fMat_ep_1[:,i] = fed.extract_at(storeHeads, ep_1, numSP, numRows)
        fMat_ep_2[:,i] = fed.extract_at(storeHeads, ep_2, numSP, numRows)
        fMat_ep_3[:,i] = fed.extract_at(storeHeads, ep_3, numSP, numRows)
        fMat_ep_4[:,i] = fed.extract_at(storeHeads, ep_4, numSP, numRows)
        fMat_ep_5[:,i] = fed.extract_at(storeHeads, ep_5, numSP, numRows)
        fMat_ep_6[:,i] = fed.extract_at(storeHeads, ep_6, numSP, numRows)
        fMat_ep_7[:,i] = fed.extract_at(storeHeads, ep_7, numSP, numRows) 
    
    log_file.close()

    return fMat_al, fMat_b1, fMat_b3, fMat_b4, fMat_JS_3, fMat_PS_3, fMat_GS_10, fMat_FS_6, fMat_WW_9, fMat_EW_16, fMat_AW_26, fMat_BW_26, fMat_NW_17, fMat_NW_15, fMat_ep_1, fMat_ep_2, fMat_ep_3, fMat_ep_4 ,fMat_ep_5, fMat_ep_6, fMat_ep_7
