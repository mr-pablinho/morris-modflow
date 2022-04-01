# -*- coding: utf-8 -*-
"""
TITLE: CREATE RIVER PACKAGE FILE 
TYPE: FUNCTION
Project: FLOOD
@author: Pablo Merchan-Rivera
Date of last edition: 21/01/2021
"""


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
