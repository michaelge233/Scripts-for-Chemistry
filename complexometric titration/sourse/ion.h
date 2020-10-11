//该文件定义了储存金属离子配体信息的类
#include<iostream>
//储存某种离子的某种个配体的信息
struct l_data {
	char name[10];           //配体名称
	int num;                 //最多配位数
	double* p;               //数组，每种配位数的配合物的稳定常数
};

//某种离子，其中包含其和各种配体形成配合物的信息
class Ion {
public:
	char name[5];                //金属离子名称
	int l_num, l_max_num;        //配体种类上限
	l_data* l_p;                 //l_data数组
	Ion();
	Ion(const Ion& n);
	~Ion();
	void set(char* s, int n);    //设置离子的名称和最大配体种类数
	void add_l(l_data& l);       //添加配体信息
	int get_b_num(char* s);
	double get_b(char* s, int n);//查询累积稳定常数
	//重载比较运算符，方便二叉树查找
	bool operator>(Ion& n);
	bool operator<(Ion& n);
	bool operator==(Ion& n);
};

