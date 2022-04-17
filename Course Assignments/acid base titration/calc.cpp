#include<math.h>
#include <windows.h>
#define DLLEXPORT extern "C" __declspec(dllexport)

DLLEXPORT double __stdcall strong_pH(double ca, double cb) {
	if (ca == cb) {
		return 7.0;
	}
	if (ca > cb) {
		double pH = -log10(ca - cb);
		return pH;
	}
	else {
		double pH = 14 + log10(cb - ca);
		return pH;
	}
}
DLLEXPORT double __stdcall f3(double a, double b, double c, double d) {
	double x = 1.0e-14, y = 1.0, z, r;
	r = d;
	if (r < 0) {
		x = 0.0;
		y = 1.0;
	}
	else {
		x = 1.0;
		y = 0.0;
	}
	z = (x + y) / 2;
	r = (a * z * z * z) + (b * z * z) + (c * z) + d;
	while (fabs(r) > 1.0e-19) {
		if (r > 0) {
			y = z;
		}
		else {
			x = z;
		}
		z = (x + y) / 2;
		r = (a * z * z * z) + (b * z * z) + (c * z) + d;
	}
	if (z < 1.0e-4) {
		while (fabs(r) > 1.0e-19) {
			if (r > 0) {
				y = z;
			}
			else {
				x = z;
			}
			z = (x + y) / 2;
			r = (a * z * z * z) + (b * z * z) + (c * z) + d;
		}
	}
	if (z < 1.0e-7) {
		while (fabs(r) > 1.0e-19) {
			if (r > 0) {
				y = z;
			}
			else {
				x = z;
			}
			z = (x + y) / 2;
			r = (a * z * z * z) + (b * z * z) + (c * z) + d;
		}
	}
	return z;
}

DLLEXPORT double __stdcall weak_pH(double pka, double ca, double cb) {
	double ka = pow(10, -pka);
	double a = 1.0, b = cb + ka, c = -(ka * ca + 1.0e-14), d = -1.0e-14*ka;
	double pH = -log10(f3(a, b, c, d));
	return pH;
}

DLLEXPORT double __stdcall wsa_pH(double pka, double cw, double cs) {
	double ka = pow(10.0, -pka);
	double a = 1.0, b = ka - cs, c = -(ka * cw + ka * cs + 1.0e-14), d = -1.0e-14 * ka;
	double pH = -log10(f3(a, b, c, d));
	return pH;
}

DLLEXPORT double __stdcall wsb_pH(double pkb, double cw, double cs) {
	double kb = pow(10.0, -pkb);
	double a = 1.0, b = kb - cs, c = -(kb * cw + kb * cs + 1.0e-14), d = -1.0e-14 * kb;
	double pH = 14.0 + log10(f3(a, b, c, d));
	return pH;
}
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)

{
	return true;
}