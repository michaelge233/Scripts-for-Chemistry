#include "ion.h"
#include<cstring>
using namespace std;

int Ioncmp(char* s1, char* s2) {
	for (int i = 0; i < 5; i++) {
		if (s1[i] > s2[2]) { return 1; }
		if (s1[i] < s2[2]) { return -1; }
		
	};

}

Ion::Ion() :l_num(0), l_max_num(0), l_p(NULL) {
	;
}
Ion::~Ion() {
	for (int i = 0; i < l_num; i++) {
		delete[] l_p[i].p;
	}
	if (l_p != NULL) {
		delete[] l_p;
	}
}
Ion::Ion(const Ion& n) {
	strcpy_s(name, n.name);
	l_num = n.l_num; l_max_num = n.l_max_num;
	l_p = new l_data[l_max_num];
	for (int i = 0; i < l_num; i++) {
		l_p[i].num = n.l_p[i].num;
		strcpy_s(l_p[i].name, n.l_p[i].name);
		l_p[i].p = new double[l_p[i].num];
		for (int k = 0; k < l_p[i].num; k++) {
			l_p[i].p[k] = n.l_p[i].p[k];
		}
	}
}
void Ion::set(char* s, int n) {
	strcpy_s(name, s);
	l_max_num = n;
	if (n == 0) { return; }
	l_p = new l_data[n];
}
void Ion::add_l(l_data& l) {
	if (l_num >= l_max_num) { return; }
	l_num++;
	strcpy_s(l_p[l_num].name, l.name);
	l_p[l_num].num = l.num;
	if (l.num == 0) { return; }
	l_p[l_num].p = new double[l.num];
	for (int i = 0; i < l.num; i++) {
		l_p[l_num].p[i] = l.p[i];
	}
}
double Ion::get_b(char* s, int n) {
	if (l_p == NULL) { return 0.0; }
	int k = -1;
	for (int i = 0; i < l_max_num; i++) {
		if (strcmp(l_p[i].name, s) == 0) {
			k = i;
			break;
		}
	}
	if (k == -1) { return 0.0; }
	if (l_p[k].num < n) { return 0.0; }
	return l_p[k].p[n - 1];
}
bool Ion::operator<(Ion& n) {
	if (strcmp(name, n.name) < 0) { return true; }
	else { return false; }
}
bool Ion::operator>(Ion& n) {
	if (strcmp(name, n.name) > 0) { return true; }
	else { return false; }
}
bool Ion::operator==(Ion& n) {
	if (strcmp(name, n.name) == 0) { return true; }
	else { return false; }
}

int Ion::get_b_num(char* s) {
	if (l_p == NULL) { return 0; }
	int k = -1;
	for (int i = 0; i < l_max_num; i++) {
		if (strcmp(l_p[i].name, s) == 0) {
			k = i;
			break;
		}
	}
	if (k == -1) { return 0; }
	return l_p[k].num;
}