import os
import sys

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

real_dir=[]
for d in os.listdir("./"):
    if is_number(d):
        real_dir.append(d)
real_dir.sort(key=lambda x:float(x))
print("Detected %d tasks"%len(real_dir))
sys.stdout.flush()

os.chdir(real_dir[0])
for i in range(len(real_dir)):
    print("Starting task %s"%real_dir[i])
    sys.stdout.flush()
    os.chdir("../%s"%real_dir[i])
    inp=[]
    for d in os.listdir("./"):
        if d.split(".")[-1]=="inp":
            inp.append(d)
    if len(inp)!=1:
        print("Error: 0 or more inp")
        continue
    task_name=inp[0][:-4]
    
    os.system("/home/cccpccc/orca_5_0_3_linux_x86-64_shared_openmpi411/orca %s.inp > %s.out"%(task_name,task_name))

print("All tasks finished.")