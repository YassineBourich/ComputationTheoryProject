from Discretization.DiscretSpace import DiscretSpace
from ProjectExceptions.Exceptions import SymbolicStateError
from UtilityFunctions.Math import vec_mul_scalar, vec_add, vect_all_lte


class KSI(DiscretSpace):
    def __init__(self, x_min, x_max, Nx):
        super().__init__(x_min, x_max, Nx)
        self.x_min = self.vect_min
        self.x_max = self.vect_max
        self.Nx = self.Nv
        self.dim_x = self.dim_v

    # method to check if x belong to X0 or not
    def in_grid(self, x: list):
        for i in range(len(x)):
            if x[i] < self.x_min[i] or x[i] > self.x_max[i]:
                return False
        return True

    # method to transform a vector to index of position
    def vectorToIndex(self, x):
        # Calculating the interpolation ratio vector
        r = []
        for i in range(len(x)):
            ri = (x[i] - self.x_min[i]) / (self.x_max[i] - self.x_min[i])
            r.append(int(self.Nx[i] * ri) + 1)

        return tuple(r)

    # abstraction interface
    def q(self, x):
        try:
            # Check the dimension
            self.check_vect_dimension(x)

            if not self.in_grid(x): return (0,) * self.dim_x

            return self.vectorToIndex(x)
        except:
            raise

    # Method to resolve the coordinate of the min and max for a partition X_ksi
    def getPartitionMinAndMax(self, ksi: int):
        if (vect_all_lte(ksi, (0,) * self.dim_x)) or (not vect_all_lte(ksi, self.Nx)):
            raise SymbolicStateError("the index of the symbolic state is out of range")

        state_x_min = []
        state_x_max = []

        # Calculating the min and max position of the state in its coordinates
        for n in range(self.dim_x):
            partition_width = (self.x_max[n] - self.x_min[n]) / self.Nx[n]
            local_x_min = self.x_min[n] + partition_width * (ksi[n] - 1)
            state_x_min.append(local_x_min)
            state_x_max.append(local_x_min + partition_width)

        return tuple(state_x_min), tuple(state_x_max)

    # Method to get the center point of a partition X_ksi
    def getPartitionCenter(self, ksi):
        try:
            state_x_min, state_x_max = self.getPartitionMinAndMax(ksi)
            x_center = vec_mul_scalar(vec_add(state_x_max, state_x_min), 0.5)
            return x_center
        except:
            raise

    def isNullState(self, ksi):
        return ksi == (0,) * self.dim_x

    # Method to return a set containing all states
    def getAllStates(self):
        symb_states = set()
        ksi = [1] * self.dim_x
        while vect_all_lte(ksi, tuple(self.Nx)):
            symb_states.add(tuple(ksi.copy()))
            ksi[0] += 1
            for i in range(self.dim_x - 1):
                if ksi[i] > self.Nx[i]:
                    ksi[i] = 1
                    ksi[i + 1] += 1

        symb_states.add((0,) * self.dim_x)

        return symb_states