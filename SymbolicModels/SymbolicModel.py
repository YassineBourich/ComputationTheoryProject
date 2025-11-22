from Discretization.Discretizator import Discretizator
from Reachability.ReachabilityMethods import ReachabilityMethods
from ProjectMath.Math import vect_all_lte
import pickle

class SymbolicModel:
    def __init__(self, continuous_model, reachability, reachability_method: ReachabilityMethods, Nx, Nu):
        self.Nx = Nx
        self.Nu = Nu
        self.continuous_model = continuous_model
        self.discretizator = Discretizator(
            self.continuous_model.getX()[0], self.continuous_model.getX()[1],
            self.continuous_model.getU()[0], self.continuous_model.getU()[1],
            self.Nx, self.Nu
        )

        self.num_of_sym_states = self.discretizator.KSI.num_of_sym_states
        self.num_of_commands = self.discretizator.SIGMA.num_of_commands

        self.reachability = reachability
        self.reachability_method = reachability_method

        self.g = self.construct_model()

    def construct_model(self):
        print("Constructing the symbolic model...")
        model = {}

        # Choose the reachability methods
        r_m = self.reachability.reachable_interval_Monotone
        if not self.reachability_method.value:
            r_m = self.reachability.reachable_interval_Bounds

        # Calculating the symbolic for ksi = 0
        all_states = self.discretizator.KSI.getAllStates()
        for sigma in range(1, self.num_of_commands + 1):
            model[(0, sigma)] = all_states

        # Calculating the symbolic model for each symbolic state and command
        for ksi in range(1, self.num_of_sym_states + 1):
            x_min, x_max = self.discretizator.getPartitionMinAndMax(ksi)
            for sigma in range(1, self.num_of_commands + 1):
                u = self.discretizator.p(sigma)
                f_min, f_max = r_m(x_min, x_max, u, self.continuous_model.getW()[0], self.continuous_model.getW()[1])

                # Constructing the model for every pair (ksi, sigma) by returning the set
                # of successor states
                model[(ksi, sigma)] = self.getSetOfSuccessors(f_min, f_max, ksi, sigma)

        print("Symbolic model constructed.")
        return model

    # Method that return the set of successor states, which are partitions that intersect
    # with the region f_min, f_max
    def getSetOfSuccessors(self, f_min, f_max, ksi, sigma):
        include_x0 = 0
        # If the reachable region is totally out of grid
        if (not vect_all_lte(f_min, self.discretizator.KSI.getV_max())) or (not vect_all_lte(self.discretizator.KSI.getV_min(), f_max)):
            include_x0 = 2

        successors = []

        if include_x0 != 2:
            # If the reachable region is partially out of grid
            if (not vect_all_lte(f_max, self.discretizator.KSI.getV_max())) or (not vect_all_lte(self.discretizator.KSI.getV_min(), f_min)):
                f_min, f_max = self.crop_reachable_area(f_min, f_max)
                include_x0 = 1

            min_index = self.discretizator.KSI.vectorToIndex(f_min)
            max_index = self.discretizator.KSI.vectorToIndex(f_max)

            successor = min_index.copy()

            while vect_all_lte(successor, max_index):
                successors.append(successor.copy())
                successor[0] += 1
                for i in range(len(successor) - 1):
                    if successor[i] > max_index[i]:
                        successor[i] = min_index[i]
                        successor[i + 1] += 1

            for i in range(len(successors)):
                successors[i] = self.discretizator.KSI.indexToSymbolicState(successors[i])

        if include_x0:
            successors.append(0)

        return set(successors)

    # method to crop the reachable area
    def crop_reachable_area(self, f_min, f_max):
        for i in range(self.discretizator.KSI.getDimV()):
            quarter_partition_width = ((self.discretizator.KSI.getV_max()[i] - self.discretizator.KSI.getV_min()[i]) / self.discretizator.KSI.getNv()[i]) * 1/4
            if f_max[i] >= self.discretizator.KSI.getV_max()[i]:
                f_max[i] = self.discretizator.KSI.getV_max()[i] - quarter_partition_width
            if f_min[i] <= self.discretizator.KSI.getV_min()[i]:
                f_min[i] = self.discretizator.KSI.getV_min()[i]
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

    # method to return the all commands such that g(ksi, sigma) is in R
    def sigma_st_g_ksi_sigma_is_in_R(self, ksi: int, R: set):
        sigma_set = set()
        for sigma in range(1, self.num_of_commands + 1):
            if self.g[(ksi, sigma)] and self.g[(ksi, sigma)].issubset(R):
                sigma_set.add(sigma)
        return sigma_set

    def getAllStates(self):
        return self.discretizator.KSI.getAllStates()

    def save_model(self, filename):
        try:
            print("Saving symbolic model...")
            with open(filename, "wb") as f:
                pickle.dump(self, f)
                print("Symbolic model saved.")
        except:
            raise

    @classmethod
    def load_model(self, filename):
        try:
            print("Loading symbolic model...")
            with open(filename, "rb") as f:
                model = pickle.load(f)
                print("Symbolic model loaded.")
                return model
        except:
            raise