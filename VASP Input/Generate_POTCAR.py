"""
This script is a tool to generate the POTCAR. 
Firstly, you should edit this script to replace the value of POTPATH with the path you store your pseudopotentials. 
Then, put this script and the POSCAR file in the same path and run this script.
"""
import os
import re

#Please input your own path for POTCAR.
POTPATH="D:\\chem_project\\calculation\\POT\\PAW_PBE"

POTDIR=os.listdir(POTPATH)
print("using POT in "+POTPATH)

fo=open("POSCAR","r")
POSCAR=fo.readlines()
fo.close()
fo=open("POTCAR","w")

elements=POSCAR[5].strip()
elements=elements.split()

ENMAX_MAX=0
for element in elements:
    possible_list=[]
    for pot in POTDIR:
        if element in pot:
            possible_list.append(pot)
    print("Choose POTCAR for element "+element)
    print("Possible Choice:",possible_list)
    p=True
    while p:
        in_POT=input("ENTER POTCAR name: ")
        if in_POT in POTDIR:
            p=False
        else:
            print("Can't Find This POTCAR")
    
    f=open(POTPATH+"\\"+in_POT+"\\POTCAR")
    POTCAR=f.read()
    f.close()
    
    es=POTCAR.find("ENMAX")
    ee=POTCAR.find("\n",es)
    ENMAX=float(re.search("\d+(\.\d+)?", POTCAR[es:ee]).group())
    if ENMAX>ENMAX_MAX:
        ENMAX_MAX=ENMAX
        
    fo.write(POTCAR)
    print(in_POT+" Writen Successfully.")

fo.close()
print("ALL ELEMENT FINISHED!")
print("MAX(ENMAX) = "+str(ENMAX_MAX))
input("PRESS ENTER TO EXICT...")
