#include "aH.h"
using namespace std;
void H::set(double p, double a) {
	lgaH = a;
	pH = p;
}
bool H::operator>(H h) {
	if (pH > h.pH) { return true; }
	else { return false; }
}
bool H::operator<(H h) {
	if (pH < h.pH) { return true; }
	else { return false; }
}
bool H::operator==(H h) {
	if (pH == h.pH) { return true; }
	else { return false; }
}