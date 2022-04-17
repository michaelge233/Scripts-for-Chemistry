//该文件用来定义二叉树
#include<iostream>
using namespace std;

//节点类
template<typename T>
class Node {
public:
	T data;
	Node* left, * right;
};

//二叉树
template<typename T>
class Tree {
public:
	Node<T>* root;                                  //根节点
	Tree();
	void set_data(Node<T>* p, T& s);                //修改指定节点的数据
	Node<T>* add_left(Node<T>* p);                  //添加左
	Node<T>* add_right(Node<T>* p);                 //添加右
	T* find(T& s, Node<T>* p);                      //查找
};

template<typename T>
Tree<T>::Tree() {
	root = new Node<T>;
	root->left = NULL; root->right = NULL;
}
template<typename T>
void Tree<T>::set_data(Node<T>* p, T& s) {
	p->data = s;
}
template<typename T>
Node<T>* Tree<T>::add_left(Node<T>* p) {
	p->left = new Node<T>;
	p->left->left = NULL; p->left->right = NULL;
	return p->left;
}
template<typename T>
Node<T>* Tree<T>::add_right(Node<T>* p) {
	p->right = new Node<T>;
	p->right->left = NULL; p->right->right = NULL;
	return p->right;
}
template<typename T>
T* Tree<T>::find(T& s, Node<T>* p) {
	if (p->data == s) { return &(p->data); }
	if (p->data < s) {
		if (p->right == NULL) { return NULL; }
		else { return find(s, p->right); }
	}
	if (p->data > s) {
		if (p->left == NULL) { return NULL; }
		else { return find(s, p->left); }
	}
}

//一个单独的函数模板
//实现插入一个有序（从小到大）的数组，按二叉排序树规则，尽可能产生完全二叉树
template<typename T>
void tree_append(Tree<T> &t,Node<T> *p, T* s, int n) {
	if(n==1) { t.set_data(p, *s); return; }
	if (n == 2) {
		t.set_data(p, s[1]);
		Node<T>* L;
		L = t.add_left(p);
		tree_append(t, L, s, 1);
		return;
	}
	Node<T> *L, *R;
	L = t.add_left(p); R = t.add_right(p);
	//插入中间元素到指定的节点
	t.set_data(p, s[n / 2]);
	//左边入左边，右边入右边
	tree_append(t,L ,s,n/2 );
	tree_append(t,R, s + n / 2 + 1, (n - 1) / 2);
}