import os
import sys

exe="mpirun -np 32 vasp_gam > nohup.out"

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

os.chdir(real_dir[0])
for i in range(len(real_dir)):
    print("Starting task %s"%real_dir[i])
    sys.stdout.flush()
    os.chdir("../")
    os.chdir(real_dir[i])
    os.system(exe)
    
print("Finished all")
