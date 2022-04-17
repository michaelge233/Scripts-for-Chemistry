#include<fstream>
#include<iostream>
#include <windows.h>
#include<cmath>
#include "ion.h"
#include "aH.h"
#include "tree.h"
#define DLLEXPORT extern "C" __declspec(dllexport)
using namespace std;

//文件中读取的各种数据
int ion_num,aH_num;
Ion* ion_list = NULL;
H* aH_list = NULL;
Tree<Ion> ion_tree;
Tree<H> h_tree;

//滴定的详细计算信息
double lgaY,lgaM,lgK,lgaY_H,lgaY_M,lgaM_OH,lgaM_L;

//读入金属离子和各种配体的数据
void Ion_input() {
	fstream infile("ions.txt", ios::in);
	int l_num, l_max;
	char l_name[5], ion_name[10];
	infile >> ion_num;
	ion_list = new Ion[ion_num];
	for (int i = 0; i < ion_num; i++) {
		infile >> ion_name >> l_num;
		ion_list[i].set(ion_name, l_num);
		for (int k = 0; k < l_num; k++) {
			infile >> ion_list[i].l_p[k].name >> ion_list[i].l_p[k].num;
			ion_list[i].l_p[k].p = new double[ion_list[i].l_p[k].num];
			for (int j = 0; j < ion_list[i].l_p[k].num; j++) {
				infile >> ion_list[i].l_p[k].p[j];
			}
		}
	}
	infile.close();
}

//读入EDTA酸效应系数的数据
void H_input() {
	fstream infile("aH.txt", ios::in);
	double lgaH,pH;
	infile >> aH_num;
	aH_list = new H[aH_num];
	for (int i = 0; i < aH_num; i++) {
		infile >> pH >> lgaH;
		aH_list[i].set(pH, lgaH);
	}
	infile.close();
}

//计算EDTA的副反应系数
double get_lgaY(double pH,int i_num,char** s,double* c) {
	H temp1;
	Ion temp2;
	Ion* lgam_p;
	char temp3[5]="EDTA";
	temp1.set(pH, 0);
	double lgaH = h_tree.find(temp1, h_tree.root)->lgaH;
	double lgaM,aM,lgam=0.0;
	aM = 1.0;
	for (int i = 0; i < i_num; i++) {
		strcpy_s(temp2.name, s[i]);
		lgam_p = ion_tree.find(temp2, ion_tree.root);
		if (lgam_p == NULL) { lgam = 0.0; }
		else {
			lgam = lgam_p->get_b(temp3, 1);
		}
		aM = aM + c[i]*pow(10.0 ,lgam);
	}
	lgaY_H = lgaH;
	lgaY_M = log10(aM);
	lgaY = log10(pow(10.0, lgaH) + aM - 1);
	return lgaY;
}

//计算金属离子的副反应系数
double get_lgaM(double pH, char* x,int l_num, char** s, double* c) {
	Ion temp0;
	strcpy_s(temp0.name, x);
	Ion* aOH_p;
	char temp1[] = "OH-";
	double aOH=1.0,aL=1.0;
	aOH_p=ion_tree.find(temp0, ion_tree.root);
	if (aOH_p == NULL) { aOH = 1.0; }
	else {
		for (int i = 0; i < aOH_p->get_b_num(temp1); i++) {
			aOH = aOH + pow((pow(10.0, pH-14)), i+1) * pow(10.0, aOH_p->get_b(temp1, i+1));
		}
	}
	for (int i = 0; i < l_num; i++) {
		if (aOH_p == NULL) { ; }
		else {
			for (int k = 0;k< aOH_p->get_b_num(s[i]); k++) {
				aL = aL + pow(c[i], k+1) * pow(10.0,aOH_p->get_b(s[i], k+1));
			}
		}
	}
	lgaM_L = log10(aL);
	lgaM_OH = log10(aOH);
	lgaM = log10(aL + aOH - 1);
	return lgaM;
}

//以下是可被dll外部调用的函数

//开始计算
DLLEXPORT double __stdcall calc(char* m, double c, double pH,int l_num, char** l_name_p, double* l_c_p, int n_num, char** n_name_p, double* n_c_p) {
	Ion temp;
	char temp0[5] = "EDTA";
	Ion* K_p;
	strcpy_s(temp.name, m);
	get_lgaY(pH, n_num, n_name_p, n_c_p);
	get_lgaM(pH, m, l_num, l_name_p, l_c_p);
	K_p=ion_tree.find(temp, ion_tree.root);
	if (K_p == NULL) { lgK = 0.0; return lgK; }
	lgK=K_p->get_b(temp0, 1)-lgaM-lgaY;
	return log10(c * pow(10.0, lgK));
}

//初始化dll，读取数据并建立数据结构
DLLEXPORT void __stdcall begin() {
	Ion_input();
	H_input();
	tree_append(ion_tree, ion_tree.root, ion_list, ion_num);
	tree_append(h_tree, h_tree.root, aH_list, aH_num);
}

//返还相应的详细信息
DLLEXPORT double __stdcall get_lgK() { return lgK; }
DLLEXPORT double __stdcall get_lgaY_H() { return lgaY_H; }
DLLEXPORT double __stdcall get_lgaY_M() { return lgaY_M; }
DLLEXPORT double __stdcall get_lgaM_OH() { return lgaM_OH; }
DLLEXPORT double __stdcall get_lgaM_L() { return lgaM_L; }

//dll主函数
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
	return true;
}