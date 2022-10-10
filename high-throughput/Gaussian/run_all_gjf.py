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
sys.stdout.flush()

os.chdir(real_dir[0])
for i in range(len(real_dir)):
    print("Starting task %s"%real_dir[i])
    sys.stdout.flush()
    os.chdir("../%s"%real_dir[i])
    gjf=[]
    for d in os.listdir("./"):
        if d.split(".")[-1]=="gjf":
            gjf.append(d)
    if len(gjf)!=1:
        print("Error: 0 or more gjf")
        continue
    task_name=gjf[0][:-4]
    
    os.system("g16 %s"%task_name)
    print("Finished")

print("All tasks finished.")