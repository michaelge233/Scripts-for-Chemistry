//酸效应系数类
class H {
public:
	double lgaH, pH;
	void set(double p, double a);
	//重载比较运算符，方便二叉树查找
	bool operator>(H h);
	bool operator<(H h);
	bool operator==(H h);
};

