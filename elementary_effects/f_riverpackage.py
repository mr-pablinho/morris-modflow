# -*- coding: utf-8 -*-
"""
TITLE: RIVER PACKAGE FILE FUNCTIONS
TYPE: FUNCTION
Project: FLOOD
@author: Pablo Merchan-Rivera
Date of last edition: 09/02/2021
"""


# %% Function to import vectors as integers, floats and strings


def importVector_integer(vectorFileName):
    with open(vectorFileName, 'r') as f: 
        vectorTemporal = f.readlines()
        vectorImported = [int(i) for i in vectorTemporal]
    return vectorImported
    

def importVector_float(vectorFileName):
    with open(vectorFileName, 'r') as f: 
        vectorTemporal = f.readlines()
        vectorImported = [float(i) for i in vectorTemporal]
    return vectorImported


def importVector_string(vectorFileName):
    with open(vectorFileName, 'r') as f: 
        vectorTemporal  = f.readlines()
    vectorImported = []
    for i in range(len(vectorTemporal)): 
        get_nl = vectorTemporal[i].rstrip()
        vectorImported.append(get_nl)
    return vectorImported


def createRiverPackage(rivFileName, numActiveCells, numSP, 
                       arrayStage, arrayLayer, arrayRow, arrayColumn, arrayCondText, arrayBedBot):
    # open file to edit
    text_file = open(rivFileName, "w")
    
    # write header line
    text_file.write("%10d" % numActiveCells)
    text_file.write("%10d" % 50)
    text_file.write("\r")
    
    # write values per cell per stress period
    for i in range(numSP):
        print("printing river package file at stress period: " + str(i+1) + "...")
        text_file.write("%10d\r" % numActiveCells)
        for j in range(numActiveCells):
            k = (numActiveCells*i)+j
            # print(k)
            text_file.write("%10d" % arrayLayer[j])
            text_file.write("%10d" % arrayRow[j])
            text_file.write("%10d" % arrayColumn[j])
            text_file.write("%10.4f" % arrayStage[k])
            text_file.write("%15s" % arrayCondText[j])
            text_file.write("%10.4f" % arrayBedBot[j])
            text_file.write("\r")
    
    # close file
    text_file.close()


