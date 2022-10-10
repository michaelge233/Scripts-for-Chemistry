import os
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def read_gauss_E(path):
    with open(path,"r") as fo:
        file_list=fo.readlines()
    if not "Normal termination" in file_list[-1]:
        return 0
    
    E_list=[]
    for i in range(len(file_list)):
        if "E(" in file_list[i] and "=" in file_list[i]:
            line_list=file_list[i].strip().split()
            E_list.append(float(line_list[line_list.index("=")+1]))
            
    return min(E_list)

all_dir=os.listdir("./")
real_dir=[]
for d in all_dir:
    if is_number(d):
        real_dir.append(d)
real_dir.sort(key=lambda x:float(x))

E_list=[]
abnormal=[]
for i in range(len(real_dir)):
    out=[]
    for d in os.listdir("./%s"%real_dir[i]):
        if d.split(".")[-1]=="log":
            out.append(d)
    if len(out)!=1:
        abnormal.append(real_dir[i])
        E_list.append(0)
        continue
        
    file_path="./%s/%s"%(real_dir[i],out[0])
    E_list.append(read_gauss_E(file_path))
    
with open("energies.txt","w") as fo:
    for i in range(len(E_list)):
        fo.write(str(E_list[i])+"\n")
    
print("Finished.")
if len(abnormal)!=0:
    print("Abnormal:")
    print(abnormal)
