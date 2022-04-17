#========================加载模块======================================================
import ctypes 
import os
import numpy as np 
from matplotlib import pyplot as plt

#========================初始化dll=====================================================
lib=ctypes.CDLL("indicator.dll")
lib.strong_pH.restype=ctypes.c_double
lib.weak_pH.restype=ctypes.c_double
lib.wsb_pH.restype=ctypes.c_double
lib.wsa_pH.restype=ctypes.c_double

#========================输入==========================================================
i1=["甲基橙酸色","甲基橙碱色","酚酞酸色","酚酞碱色"]#各种终点的名字
i2=[3.1,4.4,8.2,10.0]            #各种终点的pH
i3=[20.0,20.0,20.0,20.0]         #储存每一个终点和滴定中各点pH的差值
i4=[0.0,0.0,0.0,0.0]             #储存每一个终点时的滴定程度
print("支持的滴定类型：A.强碱滴定强酸  B.强酸滴定强碱 C.强酸滴定弱碱 D.强碱滴定弱酸")
t=input("请输入滴定类型代码：")
while not t in ("A","B","C","D"):
    t=input("无效代码，请重新输入：")
ca0=float(input("输入酸的浓度："))#float是强制类型转换
cb0=float(input("输入碱的浓度："))
if t=="C":
    pkb=float(input("请输入弱碱的pkb："))
    pka=14.0-pkb
elif t=="D":
    pka=float(input("请输入弱酸的pka："))
    pkb=14.0-pka

#========================pH计算=========================================================
X=np.arange(0,2,0.0001)           #初始化x轴，x轴的范围是0-2，间隔是0.0001
pHs=[]                            #定义一个空的列表用于储存y的值
p=7
if t=="A":                        #A.强碱滴定强酸
    for i in X:                   #循环，遍历x轴每个点
        ca=ca0/(i*ca0/cb0+1)      #把ca结合滴定程度变换
        cb=ca0*i/(i*ca0/cb0+1)    #把cb结合滴定程度变换
        pH=lib.strong_pH(ctypes.c_double(ca),ctypes.c_double(cb))#计算ph（利用c++中的函数）
        for k in range(0,4):      #4个终点依次计算
            dpH=abs(pH-i2[k])     #计算dph的绝对值
            if dpH>=i3[k] and i4[k]==0.0:#如果dph开始增加而且x值没有被储存
                i4[k]=i           #储存i4用于计算终点误差
            i3[k]=dpH             #更新dph
        pHs.append(pH)            #把这一点的ph放置在y轴中
elif t=="B":                      #B.强酸滴定强碱
    for i in X:
        ca=cb0*i/(i*cb0/ca0+1)
        cb=cb0/(i*cb0/ca0+1)
        pH=lib.strong_pH(ctypes.c_double(ca),ctypes.c_double(cb))
        for k in range(0,4):
            dpH=abs(pH-i2[k])
            if dpH>=i3[k] and i4[k]==0.0:
                i4[k]=i
            i3[k]=dpH
        pHs.append(pH)

elif t=="C":                       #C.强酸滴定弱碱
    for i in X:
        if i<=1:                   #前半段
            ca=cb0*i/(i*cb0/ca0+1)
            cb=cb0*(1-i)/(i*cb0/ca0+1)
            pH=lib.weak_pH(ctypes.c_double(pka),ctypes.c_double(ca),ctypes.c_double(cb))
            pHs.append(pH)
            for k in range(0,4):
                dpH=abs(pH-i2[k])
                if dpH>=i3[k] and i4[k]==0.0:
                    i4[k]=i
                i3[k]=dpH
            if i==1:
                p=pH
        else:                      #后半段
            cw=cb0/(i*cb0/ca0+1)
            cs=cb0*(i-1)/(i*cb0/ca0+1)
            pH=lib.wsa_pH(ctypes.c_double(pka),ctypes.c_double(cw),ctypes.c_double(cs))
            pHs.append(pH)
            for k in range(0,4):
                dpH=abs(pH-i2[k])
                if dpH>=i3[k] and i4[k]==0.0:
                    i4[k]=i
                i3[k]=dpH
elif t=="D":                        #D.强碱滴定弱酸
    for i in X:
        if i<=1:
            ca=ca0*(1-i)/(i*ca0/cb0+1)
            cb=ca0*i/(i*ca0/cb0+1)
            pH=lib.weak_pH(ctypes.c_double(pka),ctypes.c_double(ca),ctypes.c_double(cb))
            pHs.append(pH)
            for k in range(0,4):
                dpH=abs(pH-i2[k])
                if dpH>=i3[k] and i4[k]==0.0:
                    i4[k]=i
                i3[k]=dpH
            if i==1:
                p=pH
        else:
            cw=ca0/(i*ca0/cb0+1)
            cs=ca0*(i-1)/(i*ca0/cb0+1)
            pH=lib.wsb_pH(ctypes.c_double(pkb),ctypes.c_double(cw),ctypes.c_double(cs))
            pHs.append(pH)
            for k in range(0,4):
                dpH=abs(pH-i2[k])
                if dpH>=i3[k] and i4[k]==0.0:
                    i4[k]=i
                i3[k]=dpH
Y=np.array(pHs)

#========================计算终点误差========================================================================
for i in range(0,4):
    e=abs(i4[i]-1)*100           
    print("滴定至%s的误差为%.2f%%"%(i1[i],e))

#========================绘图================================================================================
plt.plot(X,Y,color='black')      #画滴定曲线
plt.plot(np.array([0,2]),np.array([3.1,3.1]),color='red',label="methyl orange(acid)",linestyle='--')#四条横线
plt.plot(np.array([0,2]),np.array([4.4,4.4]),color='yellow',label="methyl orange(base)",linestyle='--')
plt.plot(np.array([0,2]),np.array([8.2,8.2]),color='silver',label="Phenolphthalein(acid)",linestyle='--')
plt.plot(np.array([0,2]),np.array([10.0,10.0]),color='magenta',label="Phenolphthalein(base)",linestyle='--')
plt.scatter(np.array([1]),np.array([p]),marker='^',label='end point')#画计量点（三角）
plt.axis([0,2,0,14])             #显示坐标的范围
plt.xlabel("V/V[ep]") 
plt.ylabel("pH") 
plt.legend()                     #添加图例
plt.show()                       #把图显示出来
