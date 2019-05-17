import plotly.figure_factory as FF

import numpy as np
from scipy.spatial import Delaunay

class СharacteristicQuadrilateral:
    def __init__(self, a):
        self.x0 = (a[0] - a[2])*1j
        self.y0 = a[0] + a[2]
        self.z0 = -a[1]*1j
        self.x1 = (a[0]-a[2]-a[3])*1j
        self.y1 = a[0]+a[2]+a[3]
        self.z1 = -a[1]*1j
        self.x2 = (a[0] - a[2] - 2*a[3])*1j
        self.y2 = a[0] + a[2] + 2*a[3]
        self.z2 = (a[3] - a[1])*1j
        self.x3 = (a[0] - a[2] - 2*a[3])*1j
        self.y3 = a[0] + a[2] + 4*a[3]
        self.z3 = (3*a[3] - a[1])*1j

    def create_trisurf_with_parameters(self, u, v, x, y, z, name):
        points2D = np.vstack([u, v]).T
        tri = Delaunay(points2D)
        simplices = tri.simplices
        return FF.create_trisurf(x=x, y=y, z=z,
                                colormap=['rgb(50, 0, 75)', 'rgb(200, 0, 200)', '#c8dcc8'],
                                show_colorbar=True,
                                simplices=simplices,
                                title=name)

    def get_uv(self, min, max):
        u=np.linspace(min, max, 60)
        v=np.linspace(min, max, 60)
        u,v=np.meshgrid(u,v)
        u=u.flatten()
        v=v.flatten()
        return u, v
    def conformal_replacement(self, u, v, r0, r1, r2, r3):
        return (r0*(1-u-v*1j)**3+3*(r1*(1-u-v*1j)**2)*(u+v*1j)+3*(r2*(1-u-v*1j))*(v*1j+u)**2+r3*(u+v*1j)**3).real
    def quasiconformal_replacement(self, u, v, k, r0, r1, r2, r3):
        return r0.real*(1 - 3*u + 3*u**2 - 3*v**2*k**2 - u**3 + 3*u*v**2*k**2) - r0.imag*(-3*v*k+6*u*v*k - 3*u**2*v*k + v**3*k**3) - \
                    (-3*r1.real*(1 - 2*u + u**2 - v**2*k**2) + 3*r1.imag*(-2*v*k + 2*u*v*k))*u + (-3*r1.imag*(1 - 2*u+ u**2 - v**2*k**2) - \
                        3*r1.real*(-2*v*k+2*u*v*k))*v*k - (-3*r2.real*(1 - u) - 3*r2.imag*v*k)*(u**2 - v**2*k**2) + 2*(-3*r2.imag*(1 - u) + \
                            3*r2.real*v*k)*u*v*k + r3.real*(u**3 - 3*u*v**2*k**2) - r3.imag*(3*u**2*v*k - v**3*k**3)
    def create_minimal_surface_conformal_replacement(self, name):
        u,v = self.get_uv(0,1)
        x = self.conformal_replacement(u, v, self.x0,self.x1,self.x2,self.x3)
        y = self.conformal_replacement(u, v, self.y0,self.y1,self.y2,self.y3)
        z = self.conformal_replacement(u, v, self.z0,self.z1,self.z2,self.z3)
        return self.create_trisurf_with_parameters(u, v, x, y, z, name)
    def create_minimal_surface_quasiconformal_replacement(self, name, k):
        u,v = self.get_uv(0,1)
        x = self.quasiconformal_replacement(u, v, k, self.x0,self.x1,self.x2,self.x3)
        y = self.quasiconformal_replacement(u, v, k, self.y0,self.y1,self.y2,self.y3)
        z = self.quasiconformal_replacement(u, v, k, self.z0,self.z1,self.z2,self.z3)
        return self.create_trisurf_with_parameters(u, v, x, y, z, name)
    