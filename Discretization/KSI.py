from Discretization.DiscretSpace import DiscretSpace
from ProjectExceptions.Exceptions import SymbolicStateError
from ProjectMath.Math import vec_mul_scalar, vec_add, vect_all_lte


class KSI(DiscretSpace):
    def __init__(self, x_min, x_max, Nx):
        super().__init__(x_min, x_max, Nx)
        self.x_min = self.vect_min
        self.x_max = self.vect_max
        self.Nx = self.Nv
        self.num_of_sym_states = self.num_of_discret_elmnts
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

    # method to transform position indices to partition index
    def indexToSymbolicState(self, r):
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
            self.check_vect_dimension(x)

            if not self.in_grid(x): return (0,) * self.dim_x

            # Calculating indices of position
            r = self.vectorToIndex(x)

            # Calculating ksi
            #ksi = self.indexToSymbolicState(r)

            return r#ksi
        except:
            raise

    # Method to resolve the index coordinate of a partition
    def symbolicStateToIdx(self, ksi: int):
        sym_states_space_idx = [0] * self.dim_x

        congruance = self.num_of_sym_states / self.Nx[len(self.Nx) - 1]

        for n in range(self.dim_x - 1, -1, -1):
            sym_states_space_idx[n] = int(ksi / congruance)
            ksi = ksi % congruance
            if n > 0:
                congruance /= self.Nx[n - 1]

        return sym_states_space_idx

    # Method to resolve the coordinate of the min and max for a partition X_ksi
    def getPartitionMinAndMax(self, ksi: int):
        if (vect_all_lte(ksi, (0,) * self.dim_x)) or (not vect_all_lte(ksi, self.Nx)):
            raise SymbolicStateError("the index of the symbolic state is out of range")

        #ksi -= 1
        #partition_coords = self.symbolicStateToIdx(ksi)

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

        return symb_states