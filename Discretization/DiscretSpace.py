from ProjectExceptions.Exceptions import DimensionError
from ProjectMath.Math import PI

class DiscretSpace:
    def __init__(self, vect_min, vect_max, Nv):
        self.Nv = None
        self.vect_max = None
        self.vect_min = vect_min
        self.dim_v = self.getDimV()
        self.setV_max(vect_max)
        self.setNv(Nv)
        self.num_of_discret_elmnts = PI(self.Nv)

    # getters
    def getDimV(self):
        return len(self.vect_min)

    def getV_min(self):
        return self.vect_min

    def getV_max(self):
        return self.vect_max

    def getNv(self):
        return self.Nv

    # setters
    def setDimV(self, dim_v):
        if dim_v == self.dim_v:
            return

        if dim_v < self.dim_v:
            del self.vect_min[dim_v:]
            del self.vect_max[dim_v:]
            del self.Nv[dim_v:]
        else:
            self.vect_min.extend([0] * (self.dim_v - dim_v))
            self.vect_max.extend([0] * (self.dim_v - dim_v))
            self.Nv.extend([0] * (self.dim_v - dim_v))

        self.dim_v = dim_v

    def setV_min(self, vect_min):
        try:
            self.check_vect_dimension(vect_min)
            self.vect_min = vect_min
        except:
            raise

    def setV_max(self, vect_max):
        try:
            self.check_vect_dimension(vect_max)
            self.vect_max = vect_max
        except:
            raise

    def setNv(self, Nv):
        try:
            self.check_vect_dimension(Nv)
            self.Nv = Nv
        except:
            raise

        # Check dimension

    def check_vect_dimension(self, v):
        if len(v) != self.dim_v:
            raise DimensionError("Dimension of the vector does not match the space dimension.")