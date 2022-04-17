import numpy as np
import math

def rotate(pr,k,theta,p0=np.zeros(3)):
    # rotate a group of points along specific axis counterclockwise
    # pr np.array(shape=(N,3)) points to be rotated
    # k np.array(shape=3) rotation axis
    # theta float or int rotation rad
    # p0 np.array(shape=3) grid origin
    # return np.array(shape=(N,3)) points after rotation
    if type(pr)!=np.ndarray:
        pr=np.array(pr)
    if type(k)!=np.ndarray:
        k=np.array(k)
    if type(p0)!=np.ndarray:
        p0=np.array(p0)
    k=k/np.sqrt((k*k).sum())
    p_opt=(pr-p0).T
    cos=math.cos(theta)
    sin=math.sin(theta)
    m=np.zeros((3,3))
    m[0,0]=cos+k[0]*k[0]*(1-cos)
    m[0,1]=-sin*k[2]+(1-cos)*k[0]*k[1]
    m[0,2]=sin*k[1]+(1-cos)*k[0]*k[2]
    m[1,0]=sin*k[2]+(1-cos)*k[0]*k[1]
    m[1,1]=cos+k[1]*k[1]*(1-cos)
    m[1,2]=-sin*k[0]+(1-cos)*k[1]*k[2]
    m[2,0]=-sin*k[1]+(1-cos)*k[0]*k[2]
    m[2,1]=sin*k[0]+(1-cos)*k[1]*k[2]
    m[2,2]=cos+k[2]*k[2]*(1-cos)
    return np.dot(m,p_opt).T+p0

def surface_vector(p1,p2,p3):
    # get surface normal vector from 3 points on the surface
    # p1,p2,p3 np.array(shape=3), points on the surface 
    # return np.array(shape=3)
    r=np.cross(p2-p1,p3-p1)
    r=r/np.linalg.norm(r)
    return r

def hkl_vector(hkl,cell):
    # get the normal vector of a crystal surface
    # hkl  list or np.array
    # cell  np.array(shape=(3,3))
    # return np.array(shape=3)
    points=np.zeros((3,3))
    zero_i=[False,False,False]
    none_zero_i=0
    for i in range(3):
        if hkl[i]!=0:
            points[i,:]=cell[i]/hkl[i]
            none_zero_i=i
        else:
            zero_i[i]=True
    for i in range(3):
        if zero_i[i]:
            points[i]=points[none_zero_i]+cell[i]
    return surface_vector(points[0],points[1],points[2])
    
def move_near(p0,p1,cell):
    """
    Eliminate the positions error after relaxation caused by peroidic condition. 
    In details, moving an atom near the edge of cell slightly may cause the atom to appear at the other end of the cell,
    which is common in geometry relaxation. 
    However, this phenomenon can cause serious problems when modeling for neb calculation.
    This function returns positions that are equivalent to p1 in which all atom positions fit p0.
    """
    # p0,p1 np.array((n,3)) positions in a cell
    # cell np.array((3,3)) cell vectors
    # return np.array(n,3) positions of p1 after moving
    
    def period(p,a,b,c):
        return p+a*cell[0]+b*cell[1]+c*cell[2]
    
    r=np.empty((p0.shape[0],3))
    tmp_d=np.empty((p0.shape[0],27))

    n_ijk=np.empty((27,3))
    n=0
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            for k in [-1,0,1]:
                tmp_d[:,n]=np.sqrt(np.square(period(p1,i,j,k)-p0).sum(1))
                n_ijk[n]=np.array([i,j,k])
                n=n+1
    best=tmp_d.argmin(1)
    for i in range(p0.shape[0]):
        n=best[i]
        r[i,:]=period(p1[i],n_ijk[n,0],n_ijk[n,1],n_ijk[n,2])
        
    return r
    
def neb_rotate(V1,V2,base,ro,n_img=4):
    """
    A tool to model for neb calculation of ion migration in perocskite.
    V1 is a perovskite with a halogen vacancy. If an adjacent halogen migrates to fill it, another vacancy V2 will form. 
    This function is written to model for this process, and is also helpful to other similar cases. 
    """
    # V1,V2 ase.Atoms, Initial and final state
    # base int, index of atom of rotation center
    # ro int, index of atom to be rotated
    # n_img int, number of images in neb
    # return a list containing the ase.Atoms objects representing the images for neb calculation
    img_list=[]
    for i in range(n_img):
        img_list.append(V1.copy())
        img_list[i].positions=V1.positions+(i+1)/(n_img+1)*(V2.positions-V1.positions)
        
    d1=np.sqrt(np.square(V1[ro].position-V1[base].position).sum())
    d2=np.sqrt(np.square(V2[ro].position-V2[base].position).sum())
    
    for i in range(n_img):
        vec=img_list[i][ro].position-img_list[i][base].position
        vec=vec/np.linalg.norm(vec)*(d1*(i+1)/(n_img+1)+d2*(n_img-i)/(n_img+1))
        img_list[i][ro].position=img_list[i][base].position+vec
    return img_list