from Discretization.Discretizator import Discretizator
from Reachability.ReachabilityMethods import ReachabilityMethods
from ProjectMath.Math import vect_all_lte
import pickle
from tqdm import tqdm
from math import pi
import numpy as np

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

        self.symb_states = self.discretizator.KSI.getAllStates()
        self.symb_commands = self.discretizator.SIGMA.getAllCommands()

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
        """all_states = self.discretizator.KSI.getAllStates()
        for sigma in range(1, self.num_of_commands + 1):
            model[(0, sigma)] = all_states"""

        # Calculating the symbolic model for each symbolic state and command
        bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
        for ksi in tqdm(self.symb_states, bar_format=bar_format, ncols=80):
            x_min, x_max = self.discretizator.getPartitionMinAndMax(ksi)
            for sigma in self.symb_commands:
                u = self.discretizator.p(sigma)
                f_min, f_max = r_m(x_min, x_max, u, self.continuous_model.getW()[0], self.continuous_model.getW()[1])

                # resolving the states qmin and qmax from f_min and f_max
                if self.continuous_model.get_dim_x() == 3:
                    if f_min[2] < -pi:
                        f_min[2] += 2 * pi
                    if f_max[2] < -pi:
                        f_max[2] += 2 * pi
                    if f_min[2] > pi:
                        f_min[2] -= 2 * pi
                    if f_max[2] > pi:
                        f_max[2] -= 2 * pi

                self.correct_reach_f(f_min, f_max)

                if not vect_all_lte(f_min, f_max):
                    print(f"Fatal: fmin={f_min}, fmax={f_max}")

                include_x0 = 0
                if (not vect_all_lte(f_min, self.continuous_model.getX()[1])) or (not vect_all_lte(self.continuous_model.getX()[0], f_max)):
                    include_x0 = 2

                if include_x0 != 2:
                    if (not vect_all_lte(f_max, self.continuous_model.getX()[1])) or (not vect_all_lte(self.continuous_model.getX()[0], f_min)):
                        f_min, f_max = self.crop_reachable_area(f_min, f_max)
                        include_x0 = 1

                q_min = self.discretizator.q(f_min)
                q_max = self.discretizator.q(f_max)
                # Constructing the model for every pair (ksi, sigma) by stocking the delimiter states
                model[(ksi, sigma)] = (q_min, q_max)#self.getSetOfSuccessors(f_min, f_max, ksi, sigma)

        print("Symbolic model constructed: DONE")
        return model

    # Method that return the set of successor states, which are partitions that intersect
    # with the region f_min, f_max
    def getSetOfSuccessors(self, f_min, f_max, ksi, sigma):
        print("Resolving successors of (" + str(ksi) + ", " + str(sigma) + ")...")
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
        for i in range(self.continuous_model.get_dim_x()):
            quarter_partition_width = ((self.continuous_model.getX()[1][i] - self.continuous_model.getX()[0][i]) / self.Nx[i]) * 1/4
            if f_max[i] >= self.continuous_model.getX()[1][i]:
                f_max[i] = self.continuous_model.getX()[1][i] - quarter_partition_width
            if f_min[i] <= self.continuous_model.getX()[0][i]:
                f_min[i] = self.continuous_model.getX()[0][i]
        return f_min, f_max

    # Correcting the positions f_min and f_max delimiting the hyper rectangle
    def correct_reach_f(self, f_min, f_max):
        for i in range(self.continuous_model.get_dim_x()):
            if f_min[i] > f_max[i]:
                f_min[i], f_max[i] = f_max[i], f_min[i]

    # method to get predecessors of a set of states
    def Pre(self, R: set):
        R_grid = self.construct_R_grid(R)

        predecessors = set()
        bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
        for ksi in tqdm(self.symb_states, bar_format=bar_format, ncols=80):
            if self.exists_sigma_st_ksi_is_pre(ksi, R_grid):
                predecessors.add(ksi)

        return predecessors

    # method to check if there is a command such that g(ksi, sigma) is in R (such that ksi
    # is a predecessor)
    def exists_sigma_st_ksi_is_pre(self, ksi: int, R_grid):
        for sigma in self.symb_commands:
            if (ksi, sigma) in self.g:
                q_min, q_max = self.g[(ksi, sigma)]
                if self.rectangle_in_R(q_min, q_max, R_grid):
                    return True
        return False

    # method to return the all commands such that g(ksi, sigma) is in R
    def sigma_st_g_ksi_sigma_is_in_R(self, ksi: int, R_grid):
        sigma_set = set()
        for sigma in self.symb_commands:
            if (ksi, sigma) in self.g:
                q_min, q_max = self.g[(ksi, sigma)]
                if self.rectangle_in_R(q_min, q_max, R_grid):
                    sigma_set.add(sigma)
        return sigma_set

    def construct_R_grid(self, R: set):
        R_grid = np.zeros([self.Nx[i] + 1 for i in range(self.continuous_model.get_dim_x())], dtype=bool)
        for v in R:
            R_grid[v] = True

        return R_grid

    def rectangle_in_R(self, q_min, q_max, R_grid):
        # Build slice for each dimension
        slices = tuple(slice(a, b + 1) for a, b in zip(q_min, q_max))
        # Check if all states in rectangle are in R
        return R_grid[slices].all()

    def getAllStates(self):
        return self.symb_states

    def getAllCommands(self):
        return self.symb_commands

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