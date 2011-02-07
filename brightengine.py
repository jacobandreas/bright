from math import *
from numpy import *

class World(object):

    def __init__(self, dimensions, c):
        self.dimensions = dimensions
        self.c = c

    def AddVelocities(self, v1, v2):

        if not v2.any():
            return v1

        par = dot(v1, v2) / dot(v2, v2) * v2
        perp = v1 - par

        fin = (v2 + par + sqrt(1 - dot(v2, v2)) * perp) / (1 + dot(v1, v2))

        return fin

class FrameOfReference(object):

    def __init__(self, world):
        self.world = world

    def GetLabX(self):
        raise NotImplementedError()

    def GetLabV(self):
        raise NotImplementedError()

    def GetLabBeta(self):
        v = self.GetLabV()
        return dot(v, v)

    def GetLabGamma(self):
        return 1 / sqrt(1 - self.GetLabBeta())

    def GetGamma(self, ref):

        v = self.GetLabV()
        rv = ref.GetLabV()

        dv = self.world.AddVelocities(rv, -v)

        b = dot(dv, dv)

        return 1 / sqrt(1 - b)

        return self.GetLabGamma()

    def GetApparentX(self, ref, time):

        x = self.GetLabX()
        v = self.GetLabV()
        rx = ref.GetLabX()
        rv = ref.GetLabV()

        rvpar = dot(rv, v) / dot(v, v) * v
        rvperp = rv - rvpar

        if v.any():
            rvg = rvpar * self.GetLabGamma() + rvperp
            vg = v * self.GetLabGamma()
        else:
            rvg = rv
            vg = v

        ltime = time

        labDist = (rx + rvg * ltime * self.world.c) - (x + vg * time * self.world.c)

        if not v.any():
            return labDist

        par = dot(labDist, v) / dot(v, v) * v
        perp = labDist - par

        return par / self.GetLabGamma() + perp

        return array([xp, yp]) + dx

        #v = self.GetLabV()
        #x0 = self.GetLabX()
        #c = self.world.c

        #if not self.GetLabV().any():
        #    return time * ref.GetLabV() + ref.GetLabX()

        #labTime = time / (self.GetLabGamma() * (1 - dot(v,v) + dot(v, x0) / c))

        #labX = ref.GetLabV() * labTime * c + ref.GetLabX()

        #refX = -self.GetLabGamma() * c * v * labTime + labX + (self.GetLabGamma() - 1) * \
        #    dot(outer(c * v, c * v) / dot(c * v, c * v), labX)

        #return refX


    def GetApparentV(ref):
        raise NotImplementedError()


class StationaryFrameOfReference(FrameOfReference):

    def __init__(self, world, x):
        FrameOfReference.__init__(self, world)
        self.__labX = x
        self.__labV = zeros(self.world.dimensions)

    def GetLabX(self):
        return self.__labX

    def GetLabV(self):
        return self.__labV


class LinearFrameOfReference(FrameOfReference):

    def __init__(self, world, x, v):
        FrameOfReference.__init__(self, world)
        self.__labX = x
        self.__labV = v

    def GetLabX(self):
        return self.__labX

    def GetLabV(self):
        return self.__labV

    def ChangeVelocity(self, nv, time):

        v = self.GetLabV()

        #print self.GetLabV(), nv

        dv = self.world.AddVelocities(-self.GetLabV(), nv)
        #nx = time * self.world.c * dv + self.GetLabX()

        cLabGamma = self.GetLabGamma()
        nLabGamma = 1 / sqrt(1 - dot(nv, nv))
        dGamma = 1 / sqrt(1 - dot(dv,dv))

        #print sqrt(1 - dot(v,v)), sqrt(1 - dot(nv,nv)) 
        
        vsq = dot(dv,dv)
        dt = time * cLabGamma / nLabGamma

        ct = time# * cLabGamma
        nt = dt

        #print sqrt(1 - dot(v,v)) / sqrt(1 - dot(nv,nv)), nt

        #print

        nx = ct * self.world.c * self.GetLabV() * self.GetLabGamma() - nt * \
            self.world.c * nv * nLabGamma + self.GetLabX()
        return LinearFrameOfReference(self.world, nx, nv), nt

