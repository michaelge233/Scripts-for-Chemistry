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
for i in range(len(real_dir)):
    cur_dir=os.listdir(real_dir[i])
    cur_out=[]
    for cur_file in cur_dir:
        if ".log" in cur_file:
            cur_out.append(cur_file)
    if len(cur_out)!=1:
        abnormal.append(real_dir[i])
        continue
        
    cur_out=cur_out[0]
    os.system("cp ./%s/%s ./result/%s.log"%(real_dir[i],cur_out,real_dir[i]))
    
print("Creating compressed file")
if os.path.exists("./result.tar.gz"):
    os.remove("./result.tar.gz")
os.system("tar -zcvf ./result.tar.gz ./result")


if len(abnormal)==0:
    print("ALL finished.")
else:
    print("Finished. Abnormal:")
    print(abnormal)