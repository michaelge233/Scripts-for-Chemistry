import sys
import os
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def r(x, y, z):
    return np.sqrt(x**2+y**2+z**2)


def s(x, y, z):
    return 1


def pz(x, y, z):
    return z / r(x, y, z)


def px(x, y, z):
    return x / r(x, y, z)


def py(x, y, z):
    return y / r(x, y, z)


def dz2(x, y, z):
    return (2*z**2-x**2-y**2)/r(x, y, z)**2


def dxz(x, y, z):
    return x*z/r(x, y, z)**2


def dyz(x, y, z):
    return y*z/r(x, y, z)**2


def dx2y2(x, y, z):
    return (x**2-y**2)/r(x, y, z)**2


def dxy(x, y, z):
    return x*y/r(x, y, z)**2


def fz3(x, y, z):
    return z*(5*z**2-3*r(x, y, z)**2)/r(x, y, z)**3


def fxz2(x, y, z):
    return x*(5*z**2-r(x, y, z)**2)/r(x, y, z)**3


def fyz2(x, y, z):
    return y*(5*z**2-r(x, y, z)**2)/r(x, y, z)**3


def fy3x2y2(x, y, z):
    return y*(3*x**2-y**2)/r(x, y, z)**3


def fxx23y2(x, y, z):
    return x*(x**2-3*y**2)/r(x, y, z)**3


def fxyz(x, y, z):
    return x*y*z/r(x, y, z)**3


def fzx2y2(x, y, z):
    return z*(x**2-y**2)/r(x, y, z)**3


def gz4(x, y, z):
    return (35*z**4-30*z**2*r(x, y, z)**2+3*r(x, y, z)**4)/r(x, y, z)**4


def gz3x(x, y, z):
    return x*z*(4*z**2-3*x**2-3*y**2)/r(x, y, z)**4


def gz3y(x, y, z):
    return x*z*(4*z**2-3*x**2-3*y**2)/r(x, y, z)**4


def gz2xy(x, y, z):
    return x*y*(6*z**2-x**2-y**2)/r(x, y, z)**4


def gz2x2y2(x, y, z):
    return (x**2-y**2)*(6*z**2-x**2-y**2)/r(x, y, z)**4


def gzx3(x, y, z):
    return x*z*(x**2-3*y**2)/r(x, y, z)**4


def gzy3(x, y, z):
    return y*z*(3*x**2-y**2)/r(x, y, z)**4


def gxyx2y2(x, y, z):
    return x*y*(x**2-y**2)/r(x, y, z)**4


def gx4y4(x, y, z):
    return (x**4+y**4-6*x**2*y**2)/r(x, y, z)**2


def R1s(x, y, z):
    return np.exp(-r(x, y, z))


def R2s(x, y, z):
    return (2-r(x, y, z))*np.exp(-r(x, y, z)/2)


def R2p(x, y, z):
    return r(x, y, z)*np.exp(-r(x, y, z)/2)


def R3s(x, y, z):
    return (6-4*r(x, y, z)+4/9*r(x, y, z)**2)*np.exp(-r(x, y, z)/3)


def R3p(x, y ,z):
    return 2/3*r(x, y, z)*(4-2/3*r(x, y, z))*np.exp(-r(x, y, z)/3)


def R3d(x, y, z):
    return 4/9*r(x, y, z)**2*np.exp(-r(x, y, z)/3)


def R4s(x, y, z):
    return (24-18*r(x, y, z)+3*r(x, y, z)**2-r(x, y, z)**3/8)*np.exp(-r(x, y, z)/4)


def R4p(x, y, z):
    return r(x, y, z)/2*(20-5*r(x, y, z)+r(x, y, z)**2/4)*np.exp(-r(x, y, z)/4)


def R4d(x, y, z):
    return (6-r(x, y, z)/2)*r(x, y, z)**2/4*np.exp(-r(x, y, z)/4)


def R4f(x, y, z):
    return r(x, y, z)**3/8*np.exp(-r(x, y, z)/4)


def R5s(x, y, z):
    return (120-96*r(x, y, z)+19.2*r(x, y, z)**2-1.28*r(x, y, z)**3+0.0256*r(x, y, z)**4)*np.exp(-r(x, y, z)/5)


def R5p(x, y, z):
    return 2/5*r(x, y, z)*(120-36*r(x, y, z)+2.88*r(x, y, z)**2-0.064*r(x, y, z)**3)*np.exp(-r(x, y, z)/5)


def R5d(x, y, z):
    return 0.16*r(x, y, z)*(42-5.6*r(x, y, z)+0.16*r(x, y, z)**2)*np.exp(-r(x, y, z)/5)


def R5f(x, y, z):
    return 0.064*r(x, y, z)**3*(8-0.4*r(x, y, z))*np.exp(-r(x, y, z)/5)


def R5g(x, y, z):
    return 0.0256*r(x, y, z)**4*np.exp(-r(x, y, z)/5)


def chooser(n=1, l=0, m=0, x=0, y=0, z=0):
    if n == 1:
        if l == 0:
            return R1s(x, y, z)*s(x, y, z), '1s'
    elif n == 2:
        if l == 0:
            return R2s(x, y, z)*s(x, y, z), '2s'
        else:
            if m == 0:
                return R2p(x, y, z)*pz(x, y, z), '$2p_z$'
            elif m == 1:
                return R2p(x, y, z)*px(x, y, z), '$2p_x$'
            else:
                return R2p(x, y, z)*py(x, y, z), '$2p_y$'
    elif n == 3:
        if l == 0:
            return R3s(x, y, z)*s(x, y, z), '3s'
        elif l == 1:
            if m == 0:
                return R3p(x, y, z)*pz(x, y, z), '$3p_z$'
            elif m == 1:
                return R3p(x, y, z)*px(x, y, z), '$3p_x$'
            else:
                return R3p(x, y, z)*py(x, y, z), '$3p_y$'
        elif l == 2:
            if m == 0:
                return R3d(x, y, z)*dz2(x, y, z), '$3d_{z^2}$'
            elif m == 1:
                return R3d(x, y, z)*dxz(x, y, z), '$3d_{xz}$'
            elif m == -1:
                return R3d(x, y, z)*dyz(x, y, z), '$3d_{yz}$'
            elif m == 2:
                return R3d(x, y, z)*dx2y2(x, y, z), '$3d_{x^2-y^2}$'
            else:
                return R3d(x, y, z)*dxy(x, y, z), '$3d_{xy}$'
    elif n == 4:
        if l == 0:
            return R4s(x, y, z)*s(x, y, z), '4s'
        elif l == 1:
            if m == 0:
                return R4p(x, y, z)*pz(x, y, z), '$4p_z$'
            elif m == 1:
                return R4p(x, y, z)*px(x, y, z), '$4p_x$'
            else:
                return R4p(x, y, z)*py(x, y, z), '$4p_y$'
        elif l == 2:
            if m == 0:
                return R4d(x, y, z)*dz2(x, y, z), '$4d_{z^2}$'
            elif m == 1:
                return R4d(x, y, z)*dxz(x, y, z), '$4d_{xz}$'
            elif m == -1:
                return R4d(x, y, z)*dyz(x, y, z), '$4d_{yz}$'
            elif m == 2:
                return R4d(x, y, z)*dx2y2(x, y, z), '$4d_{x^2-y^2}$'
            else:
                return R4d(x, y, z)*dxy(x, y, z), '$4d_{xy}$'
        elif l == 3:
            if m == 0:
                return R4f(x, y, z)*fz3(x, y, z), '$4f_{z^3}$'
            elif m == 1:
                return R4f(x, y, z)*fxz2(x, y, z), '$4f_{xz^2}$'
            elif m == -1:
                return R4f(x, y, z)*fyz2(x, y, z), '$4f_{yz^2}$'
            elif m == 3:
                return R4f(x, y, z)*fy3x2y2(x, y, z), '$4f_{y(3x^2-y^2)}$'
            elif m == -3:
                return R4f(x, y, z)*fxx23y2(x, y, z), '$4f_{x(x^2-3y^2)}$'
            elif m == 2:
                return R4f(x, y, z)*fxyz(x, y, z), '$4f_{xyz}$'
            else:
                return R4f(x, y, z)*fzx2y2(x, y, z), '$4f_{z(x^2-y^2)}$'
    elif n == 5:
        if l == 0:
            return R5s(x, y, z)*s(x, y, z), '5s'
        elif l == 1:
            if m == 0:
                return R5p(x, y, z)*pz(x, y, z), '$5p_z$'
            elif m == 1:
                return R5p(x, y, z)*px(x, y, z), '$5p_x$'
            else:
                return R5p(x, y, z)*py(x, y, z), '$5p_y$'
        elif l == 2:
            if m == 0:
                return R5d(x, y, z)*dz2(x, y, z), '$5d_{z^2}$'
            elif m == 1:
                return R5d(x, y, z)*dxz(x, y, z), '$5d_{xz}$'
            elif m == -1:
                return R5d(x, y, z)*dyz(x, y, z), '$5d_{yz}$'
            elif m == 2:
                return R5d(x, y, z)*dx2y2(x, y, z), '$5d_{x^2-y^2}$'
            else:
                return R5d(x, y, z)*dxy(x, y, z), '$5d_{xy}$'
        elif l == 3:
            if m == 0:
                return R5f(x, y, z)*fz3(x, y, z), '$5f_{z^3}$'
            elif m == 1:
                return R5f(x, y, z)*fxz2(x, y, z), '$5f_{xz^2}$'
            elif m == -1:
                return R5f(x, y, z)*fyz2(x, y, z), '$5f_{yz^2}$'
            elif m == 3:
                return R5f(x, y, z)*fy3x2y2(x, y, z), '$5f_{y(3x^2-y^2)}$'
            elif m == -3:
                return R5f(x, y, z)*fxx23y2(x, y, z), '$5f_{x(x^2-3y^2)}$'
            elif m == 2:
                return R5f(x, y, z)*fxyz(x, y, z), '$5f_{xyz}$'
            else:
                return R5f(x, y, z)*fzx2y2(x, y, z), '$5f_{z(x^2-y^2)}$'
        elif l == 4:
            if m == 0:
                return R5g(x, y, z)*gz4(x, y, z), '$5g_{z^4}$'
            elif m == 1:
                return R5g(x, y, z)*gz3x(x, y, z), '$5g_{z^3x}$'
            elif m == -1:
                return R5g(x, y, z)*gz3y(x, y, z), '$5g_{z^3y}$'
            elif m == 2:
                return R5g(x, y, z)*gz2xy(x, y, z), '$5g_{z^2xy}$'
            elif m == -2:
                return R5g(x, y, z)*gz2x2y2(x, y, z), '$5g_{z^2(x^2-y^2)}$'
            elif m == 3:
                return R5g(x, y, z)*gzx3(x, y, z), '$5g_{zx^3}$'
            elif m == -3:
                return R5g(x, y, z)*gzy3(x, y, z), '$5g_{zy^3}$'
            elif m == 4:
                return R5g(x, y, z)*gxyx2y2(x, y, z), '$5g_{xy(x^2-y^2)}$'
            else:
                return R5g(x, y, z)*gx4y4(x, y, z), '$5g_{x^4+y^4}$'

X=15
Y=15
Z=15
n=3
l=2
m=0

fig = plt.figure()
axes = fig.add_subplot(111, projection='3d')
fig.suptitle('{}'.format(chooser(n, l, m)[1]))
Axes3D.mouse_init(axes)
x = np.linspace(-X, X, 100)
y = np.linspace(-Y, Y, 100)
z = np.linspace(-Z, Z, 100)
ans_x, ans_y, ans_z, ans_x2, ans_y2, ans_z2 = [], [], [], [], [], []
for i in x:
    for j in y:
        for k in z:
            if 0.7 < chooser(n, l, m, i, j, k)[0] :
                ans_x.append(i)
                ans_y.append(j)
                ans_z.append(k)
            if chooser(n, l, m, i, j, k)[0] < -0.7:
                ans_x2.append(i)
                ans_y2.append(j)
                ans_z2.append(k)
axes.scatter(ans_x2, ans_y2, ans_z2, s=1,c='r', alpha=0.01)
axes.scatter(ans_x, ans_y, ans_z, s=1,c='b', alpha=0.01)

axes.grid(True)
axes.set_xlim(-X,X)
axes.set_ylim(-Y,Y)
axes.set_zlim(-Z,Z)
plt.show()
