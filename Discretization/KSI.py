from operator import index

from Exceptions.Exceptions import DimensionError
from Math.Math import PI, vec_mul_scalar, vec_add


class KSI:
    def __init__(self, x_min, x_max, Nx):
        self.x_min = x_min
        self.dim_x = self.getDimX()
        self.setX_max(x_max)
        self.setNx(Nx)
        self.num_of_sym_states = PI(self.Nx)

    # getters
    def getDimX(self):
        return len(self.x_min)

    def getX_min(self):
        return self.x_min

    def getX_max(self):
        return self.x_max

    def getNx(self):
        return self.Nx

    #setters
    def setDimX(self, dim_x):
        if dim_x == self.dim_x:
            return
        elif dim_x < self.dim_x:
            del self.x_min[dim_x:]
            del self.x_max[dim_x:]
            del self.Nx[dim_x:]
        elif dim_x > self.dim_x:
            self.x_min.extend([0] * (self.dim_x - dim_x))
            self.x_max.extend([0] * (self.dim_x - dim_x))
            self.Nx.extend([0] * (self.dim_x - dim_x))

        self.dim_x = dim_x

    def setX_min(self, x_min):
        if len(x_min) != self.dim_x:
            raise DimensionError("Err1")

        self.x_min = x_min

    def setX_max(self, x_max):
        if len(x_max) != self.dim_x:
            raise DimensionError("Err1")

        self.x_max = x_max

    def setNx(self, Nx):
        if len(Nx) != self.dim_x:
            raise DimensionError("Err1")

        self.Nx = Nx

    # Check dimension
    def check_dimension(self, x):
        if len(x) != self.dim_x:
            raise DimensionError("Err2")

    # method to check if x belong to X0
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
            r.append(ri)

        # Multiplying by the division number and casting
        for i in range(len(x)):
            r[i] = int(self.Nx[i] * r[i])

        return r

    # method to transform position indices to partition index
    def indexToPartition(self, r):
        ksi = 1  # To shift the indexation by 1
        multiplyer = 1
        for i in range(self.dim_x):
            ksi += multiplyer * r[i]
            multiplyer *= self.Nx[i]

        return ksi

    # abstraction interface
    def q(self, x):
        try:
            # Check the dimension
            self.check_dimension(x)

            if not self.in_grid(x): return 0

            # Calculating indices of position
            r = self.vectorToIndex(x)

            # Calculating ksi
            ksi = self.indexToPartition(r)

            return ksi
        except:
            raise

    # Method to resolve the index coordinate of a partition
    def partitionToIdx(self, ksi: int):
        sym_states_space_idx = [0] * self.dim_x

        congruance = self.num_of_sym_states / self.Nx[len(self.Nx) - 1]

        for n in range(self.dim_x - 1, -1, -1):
            sym_states_space_idx[n] = int(ksi / congruance)
            ksi = ksi % congruance
            if n > 0:
                congruance /= self.Nx[n - 1]

        return sym_states_space_idx

    # Method to resolve the coordinate of the min and max for a partition
    def getPartitionMinAndMax(self, ksi: int):
        if ksi <= 0 or ksi > self.num_of_sym_states:
            raise ValueError("the index of the state is out of range")

        ksi -= 1
        partition_coords = self.partitionToIdx(ksi)

        state_x_min = []
        state_x_max = []

        # Calculating the min and max position of the state in its coordinates
        for n in range(self.dim_x):
            partition_width = (self.x_max[n] - self.x_min[n]) / self.Nx[n]
            local_x_min = self.x_min[n] + partition_width * partition_coords[n]
            state_x_min.append(local_x_min)
            state_x_max.append(local_x_min + partition_width)

        return state_x_min, state_x_max

    # Method to get the center point of a partition
    def getPartitionCenter(self, ksi):
        try:
            state_x_min, state_x_max = self.getPartitionMinAndMax(ksi)

            x_center = vec_mul_scalar(vec_add(state_x_max, state_x_min), 0.5)
            return x_center
        except:
            raise

    # Method to return a set containing all states
    def getAllStates(self):
        states = set()
        for ksi_plus in range(0, self.num_of_sym_states + 1):
            states.add(ksi_plus)

        return states