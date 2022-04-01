# -*- coding: utf-8 -*-
"""
EDIT MODFLOW PACKAGE FILES
TYPE: Function
@author: Pablo Merchan-Rivera
Date of last edition: 02/06/2020
"""

# %% Libraries
import fileinput as fi
import numpy as np


# %% Function to change text to new parameter values


def rewrite_mask(modflowEditable, textToReplace, valueParameter):
    
    with fi.FileInput(modflowEditable, inplace=True, backup='') as file:
        for line in file:
            print(line.replace(textToReplace, valueParameter), end='')
            

# %% Function to extract data at specific points


def extract_at(data_matrix, location_points, numSP, numRows):
    
    heads_at_point = np.zeros((numSP))
    
    for i in range(numSP):
        jump_sp = i*numRows
        heads_at_point[i] = data_matrix[jump_sp + location_points[0], location_points[1]]
    
    return heads_at_point
            
          
            
# %% Remove lines/headers from results file


def remove_lines(fileToEdit, keyToFind): 
    
    with open(fileToEdit,"r+") as f:
        new_f = f.readlines()
        f.seek(0)
        for line in new_f:
            if keyToFind not in line:
                f.write(line)
        f.truncate()


# %% Store heads at specific stress periods from all the simulations
        

def store_heads_sp(storeHeads, spToExtract, numRows, numCols):
    
    store = storeHeads[(spToExtract*numRows):(spToExtract*numRows)+numRows,0:numCols]
    return store


# %% Create recharge package


def createRechargePackage(rechargeMatrix, rchFileName, numSP, numRows, numCols):
    
    header_line =  "         1        50         0"
    flag = 0
    format_header = "        18         1(260G14.0)                   -1  Recharge"
    
    # open file to edit
    text_file = open(rchFileName, "w")
    
    # write header line
    text_file.write(header_line)
    text_file.write("\n")
    
    # write subheaders (stress period) line
    for i in range(numSP):
        numSP_i = i+1
        print("... Generating recharge file: " + str(numSP_i))
        text_file.write("%10d" % numSP_i)
        text_file.write("%10d" % flag)
        text_file.write("\n")
        text_file.write(format_header)
        text_file.write("\n")
        
        # print recharge matrix
        for row in range(numRows):
            for col in range(numCols):
                text_file.write("%14E" % rechargeMatrix[i,row,col])
            text_file.write("\n")
        
    # close file
    text_file.close()

    
