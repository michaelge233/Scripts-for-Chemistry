"""
This script is to show the residual forces during the geometry optimization.
The residual forces are often treated as convergence criteria, but neither stdout nor OSZICAR containing them.
This script extracts the residual forces from OUTCAR and outputs to stdout. It was designed to monitor the geometry optimization.
It can be directly executed on Linux. Just copy the script to the path that VASP are running, and run this script.
"""

with open("OUTCAR","r") as fo:
    out=fo.readlines()

import numpy as np
MAX_J=500
i=0
force_list=[]
while i<len(out):
    if "TOTAL-FORCE" in out[i]:
        start = -1
        end = -1
        for j in range(1,MAX_J):
            if start == -1 and "------" in out[i+j]:
                start = i+j+1
            elif start != -1 and "------" in out[i+j]:
                end = i+j
                break
        if start == -1 or end == -1:
            print("error at "+ str(i))
            i=i+1
            continue
        
        max_force=0
        for k in range(start,end):
            c=out[k].split()[3:]
            for n in range(3):
                c[n]=float(c[n])
            c=np.array(c)
            force=np.sqrt(np.square(c).sum())
            if force>max_force:
                max_force=force

        force_list.append(max_force)
        i=end
        
    i=i+1

print(force_list)
input("Finished, press ENTER to exit...")