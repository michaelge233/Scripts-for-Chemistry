from tkinter import *
import tkinter.font as tf
import ctypes

#初始化dll
lib=ctypes.CDLL("tree.dll")      #加载dll，必须安装好visual c++，否则报错
lib.calc.restype=ctypes.c_double #声明相关函数返还的数据类型
lib.get_lgK.restype=ctypes.c_double
lib.get_lgaY_H.restype=ctypes.c_double
lib.get_lgaY_M.restype=ctypes.c_double
lib.get_lgaM_OH.restype=ctypes.c_double
lib.get_lgaM_L.restype=ctypes.c_double
lib.begin()                      #dll内部初始化（读取数据文件，建立数据结构），begin是dll内部的函数

#初始化标签和输入输出框
win=Tk()
win.title("络合滴定计算器")      #窗口标题
label_1=Label(win,text="*要滴定的金属离子：")
entry_1=Entry(win)
label_2=Label(win,text="*终点时的pH：")
entry_2=Entry(win)
label_3=Label(win,text="终点时其他配体（若多个以空格连接）：")
entry_3=Entry(win)
label_4=Label(win,text="其他配体浓度（顺序请和上面一项对应）：")
entry_4=Entry(win)
label_5=Label(win,text="终点时其他金属离子（若多个以空格连接）：")
entry_5=Entry(win)
label_6=Label(win,text="其他金属离子浓度（顺序请和上面一项对应）：")
entry_6=Entry(win)
label_7=Label(win,text="*滴定剂浓度：")
entry_7=Entry(win)
text_1=Text(win,state=DISABLED)  #输出框
#添加文字格式
text_1.tag_add("tag1","1.0","1.1")
text_1.tag_add("tag2","1.0","1.1")
text_1.tag_add("tag3","1.0","1.1")
#定义字体
font1=tf.Font(size=28)
font2=tf.Font(size=28)
font3=tf.Font(size=28)
#设置文字格式
text_1.tag_config("tag1",font=font1)                   #黑色
text_1.tag_config("tag2",font=font2,foreground="green")#绿色
text_1.tag_config("tag3",font=font3,foreground="red")  #红色
#从文件中读入图片
photo1 = PhotoImage(file='T.png')#对勾图片
photo2 = PhotoImage(file='F.png')#叉子图片

#点击详细信息按钮调用的函数
def f0():
    text_1.config(state=NORMAL)#设置输出框为可变化
    text_1.delete(2.7,2.8)     #删除按钮，以免重复点击
    #输出详细信息
    text_1.insert(INSERT,"lgαH=%.2f\n"%lib.get_lgaY_H(),"tag1")
    text_1.insert(INSERT,"lgαYM\'=%.2f\n"%lib.get_lgaY_M(),"tag1")
    text_1.insert(INSERT,"lgαMOH=%.2f\n"%lib.get_lgaM_OH(),"tag1")
    text_1.insert(INSERT,"lgαML=%.2f\n"%lib.get_lgaM_L(),"tag1")
    text_1.config(state=DISABLED)#锁住输出框

#计算按钮触发的函数
def f1():
    text_1.config(state=NORMAL)
    text_1.delete(0.0, END) #清空输出框
    #从输入框中读取信息，类型为Python字符串对象
    m=entry_1.get()         #滴定的金属离子名称
    ph=entry_2.get()        #pH
    m_c=entry_7.get()       #浓度
    if len(m)==0 or len(ph)==0 or len(m_c)==0:
        text_1.insert(INSERT,"计算失败，输入内容不全。","tag1")
        text_1.config(state=DISABLED)
        return
    l_name=entry_3.get().split(" ") #其他配体名称，分解为列表
    l_c=entry_4.get().split(" ")    #其他配体浓度，分解为列表
    if len(l_name)!=len(l_c):
        text_1.insert(INSERT,"计算失败，其他配体名称个数和浓度不一致。","tag1")
        text_1.config(state=DISABLED)
        return
    n_name=entry_5.get().split(" ") #其他金属离子名称，分解为列表
    n_c=entry_6.get().split(" ")    #其他金属离子浓度，分解为列表
    if len(n_name)!=len(n_c):
        text_1.insert(INSERT,"计算失败，其他金属离子名称个数和浓度不一致。","tag1")
        text_1.config(state=DISABLED)
        return
    
    #数据类型转换，从Python数据类型变为C++的数据类型
    m_c=float(m_c)/2.0
    m=ctypes.c_char_p(bytes(m,"utf-8"))    #将字符串对象转化为char指针
    ph=ctypes.c_double(float(ph))

    l_num=len(l_name)
    if l_name[0]=="":                      #空的字符串split后长度不为0，需单独处理
        l_num=0
    l_name_p=(ctypes.c_char_p*l_num)()     #将字符串列表转化为二维字符数组
    l_c_p=(ctypes.c_double*l_num)()        #将浮点数列表转化为double数组
    for i in range(0,l_num):
        l_name[i]=ctypes.c_char_p(bytes(l_name[i],"utf-8"))
        l_name_p[i]=l_name[i]
        l_c_p[i]=ctypes.c_double(float(l_c[i]))

    n_num=len(n_name)
    if n_name[0]=="":
        n_num=0
    n_name_p=(ctypes.c_char_p*n_num)()     #将字符串列表转化为二维字符数组
    n_c_p=(ctypes.c_double*n_num)()        #将浮点数列表转化为double数组
    for i in range(0,n_num):
        n_name[i]=ctypes.c_char_p(bytes(n_name[i],"utf-8"))
        n_name_p[i]=n_name[i]
        n_c_p[i]=ctypes.c_double(float(n_c[i]))
    m_c=ctypes.c_double(m_c)

    #调用dll的计算函数
    KC=lib.calc(m,m_c,ph,l_num,l_name_p,l_c_p,n_num,n_name_p,n_c_p)

    #输出lg(KC)
    text_1.insert(INSERT,"lg(K\'C)=%.2f\n"%KC,"tag1")
    if KC>=6:     #可以准确滴定
        text_1.image_create(END,image=photo1)      #对勾图片
        text_1.insert(INSERT,"可以准确滴定","tag2")#提示文字
    else:
        text_1.image_create(END,image=photo2)      #叉子图片
        text_1.insert(INSERT,"无法准确滴定","tag3")#提示文字
    b1 = Button(text_1,text="详细信息",command=f0) #初始化显示详细信息的按钮
    b1["state"]="normal"
    text_1.window_create(END,window=b1)            #显示按钮
    text_1.insert(INSERT,"\n")
    text_1.config(state=DISABLED)

#点击清空按钮触发的函数
def f2():
    #清空所有
    text_1.config(state=NORMAL)
    text_1.delete(0.0, END)
    text_1.config(state=DISABLED)
    entry_1.delete(0, END)
    entry_2.delete(0, END)
    entry_3.delete(0, END)
    entry_4.delete(0, END)
    entry_5.delete(0, END)
    entry_6.delete(0, END)
    entry_7.delete(0, END)

#初始化计算和清空按钮    
button_1=Button(win,text="计算",command=f1)
button_2=Button(win,text="清空",command=f2)

#所有提示、输入输出框和按钮的排版
label_1.grid(row=0,column=0,sticky=E)
entry_1.grid(row=0,column=1)
label_2.grid(row=1,column=0,sticky=E)
entry_2.grid(row=1,column=1)
label_3.grid(row=3,column=0,sticky=E)
entry_3.grid(row=3,column=1)
label_4.grid(row=4,column=0,sticky=E)
entry_4.grid(row=4,column=1)
label_5.grid(row=5,column=0,sticky=E)
entry_5.grid(row=5,column=1)
label_6.grid(row=6,column=0,sticky=E)
entry_6.grid(row=6,column=1)
label_7.grid(row=2,column=0,sticky=E)
entry_7.grid(row=2,column=1)
text_1.grid(row=7,column=0,columnspan=2)
button_1.grid(row=8,column=0)
button_2.grid(row=8,column=1)

#开启窗口主循环
mainloop()
