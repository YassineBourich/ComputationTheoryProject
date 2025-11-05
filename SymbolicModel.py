from Discretization.Discretizator import Discretizator
from Reachability.ReachabilityMethods import ReachabilityMethods
from Math.Math import vect_all_lte

class SymbolicModel:
    def __init__(self, reachability, reachability_method: ReachabilityMethods, X, U, W, Nx, Nu):
        self.Nx = Nx
        self.Nu = Nu
        self.w_min = W[0]
        self.w_max = W[1]
        self.discretisator = Discretizator(X[0], X[1], U[0], U[1], self.Nx, self.Nu)
        self.num_of_sym_states = self.discretisator.KSI.num_of_sym_states
        self.num_of_commands = self.discretisator.SIGMA.num_of_commands
        self.g = self.construct_model(reachability, reachability_method)

    def construct_model(self, reachability, reachability_method: ReachabilityMethods):
        model = {}

        # Choose the reachability methods
        r_m = reachability.reachable_interval_Monotone
        if not reachability_method.value:
            r_m = reachability.reachable_interval_Bounds

        # Calculating the symbolic for ksi = 0
        all_states = self.discretisator.KSI.getAllStates()
        for sigma in range(1, self.num_of_commands + 1):
            model[(0, sigma)] = all_states


        # Calculating the symbolic model for each symbolic state and command
        for ksi in range(1, self.num_of_sym_states + 1):
            x_min, x_max = self.discretisator.getPartitionMinAndMax(ksi)
            for sigma in range(1, self.num_of_commands + 1):
                u = self.discretisator.p(sigma)
                f_min, f_max = r_m(x_min, x_max, u, self.w_min, self.w_max)

                # Constructing the model for every pair (ksi, sigma) by returning the set
                # of successor states
                model[(ksi, sigma)] = self.getSetOfSuccessors(f_min, f_max)

        return model

    # Method that return the set of successor states, which are partitions that intersect
    # with the region f_min, f_max
    def getSetOfSuccessors(self, f_min, f_max):
        include_x0 = 0
        # If the reachable region is totally out of grid
        if (not vect_all_lte(f_min, self.discretisator.KSI.x_max)) or (not vect_all_lte(self.discretisator.KSI.x_min, f_max)):
            include_x0 = 2

        successors = []

        if include_x0 != 2:
            # If the reachable region is partially out of grid
            if (not vect_all_lte(f_max, self.discretisator.KSI.x_max)) or (not vect_all_lte(self.discretisator.KSI.x_min, f_min)):
                f_min, f_max = self.crop_reachable_area(f_min, f_max)
                include_x0 = 1

            min_index = self.discretisator.KSI.vectorToIndex(f_min)
            max_index = self.discretisator.KSI.vectorToIndex(f_max)

            print(min_index)
            print(max_index)

            successor = min_index.copy()

            while vect_all_lte(successor, max_index):
                successors.append(successor.copy())
                print("successor :" + str(successor))
                successor[0] += 1
                for i in range(len(successor) - 1):
                    if successor[i] > max_index[i]:
                        successor[i] = min_index[i]
                        successor[i + 1] += 1

            for i in range(len(successors)):
                successors[i] = self.discretisator.KSI.indexToPartition(successors[i])

        successors = set(successors)
        if include_x0:
            successors.add(0)

        return successors

    # method to crop the reachable area
    def crop_reachable_area(self, f_min, f_max):
        for i in range(self.discretisator.KSI.dim_x):
            quarter_partition_width = ((self.discretisator.KSI.x_max[i] - self.discretisator.KSI.x_min[i]) / self.discretisator.KSI.Nx[i]) * 1/4
            if f_max[i] >= self.discretisator.KSI.x_max[i]:
                f_max[i] = self.discretisator.KSI.x_max[i] - quarter_partition_width
            if f_min[i] <= self.discretisator.KSI.x_min[i]:
                f_max[i] = self.discretisator.KSI.x_min[i]
        return f_min, f_max

    # method to get predecessors of a set of states
    def Pre(self, R: set):
        predecessors = set()
        for ksi in range(0, self.num_of_sym_states + 1):
            if self.exists_sigma_st_ksi_is_pre(ksi, R):
                predecessors.add(ksi)

        return predecessors

    # method to check if there is a command such that g(ksi, sigma) is in R (such that ksi
    # is a predecessor)
    def exists_sigma_st_ksi_is_pre(self, ksi: int, R: set):
        for sigma in range(1, self.num_of_commands + 1):
            if self.g[(ksi, sigma)] and self.g[(ksi, sigma)].issubset(R):
                return True
        return False