"""
Extract CONTCAR and E after optimazation 
Result will be put into a .tar.gz file
"""

import os
import sys
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
all_dir=os.listdir("./")
real_dir=[]
for d in all_dir:
    if is_number(d):
        real_dir.append(d)
real_dir.sort(key=lambda x:float(x))
print("Detected %d tasks"%len(real_dir))


if not os.path.exists("./result"):
    os.mkdir("./result")

abnormal=[]
result=[]
for i in range(len(real_dir)):
    if os.path.exists("./%s/CONTCAR"%real_dir[i]) and os.path.exists("./%s/OSZICAR"%real_dir[i]):
        energies=[]
        with open("./%s/OSZICAR"%real_dir[i],"r") as fo:
            file_list=fo.readlines()
        for line in file_list:
            if "E0=" in line:
                cur_line=line.strip().split()
                energies.append(float(cur_line[cur_line.index("E0=")+1]))
        result.append("%s    %f \n"%(real_dir[i],min(energies)))
        os.system("cp ./%s/CONTCAR ./result/%s.CONTCAR"%(real_dir[i],real_dir[i]))
    else:
        abnormal.append(real_dir[i])
        result.append("%s    %f \n"%(real_dir[i],0.0))
        
with open("./result/E.txt","w") as fo:
    for line in result:
        fo.write(line)

print("Creating compressed file")
if os.path.exists("./result.tar.gz"):
    os.remove("./result.tar.gz")
os.system("tar -zcvf ./result.tar.gz ./result")

if len(abnormal)==0:
    print("ALL finished.")
else:
    print("Finished. Abnormal:")
    print(abnormal)