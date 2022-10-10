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


if "POTCAR" in all_dir and "INCAR" in all_dir and "KPOINTS" in all_dir:
    print("POTCAT INCAR KPOINTS detected")
    sys.stdout.flush()
else:
    print("Error: Can't find input files!")
    sys.stdout.flush()
    sys.exit(1)
    

os.chdir(real_dir[0])
for i in range(len(real_dir)):
    print("Starting task %s"%real_dir[i])
    sys.stdout.flush()
    os.chdir("../")
    os.system("cp POTCAR INCAR KPOINTS ./%s"%real_dir[i])
    os.chdir(real_dir[i])
    os.system("mpirun -np 32 vasp_gam > nohup.out")
    
print("Finished all")
