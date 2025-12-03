from Discretization.Discretizator import Discretizator
from Reachability.ReachabilityMethods import ReachabilityMethods
from UtilityFunctions.Math import vect_all_lte
import pickle
from tqdm import tqdm
from math import pi
from UtilityFunctions.NumpyGrid import *

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
        for sigma in self.symb_commands:
            model[((0,) * self.continuous_model.get_dim_x(), sigma)] = ((1,) * self.continuous_model.get_dim_x(), tuple(self.Nx), True)

        # Calculating the symbolic model for each symbolic state and command
        bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
        for ksi in tqdm(self.symb_states, bar_format=bar_format, ncols=80):
            if not self.discretizator.KSI.isNullState(ksi):
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

                    # Correcting the order of f_min and f_max
                    self.correct_reach_f(f_min, f_max)

                    # Constructing the model for every pair (ksi, sigma) by stocking the delimiter states
                    if (not vect_all_lte(f_min, self.continuous_model.getX()[1])) or (not vect_all_lte(self.continuous_model.getX()[0], f_max)):
                        model[(ksi, sigma)] = (None, None, True)

                    else:
                        include_0 = False
                        if (not vect_all_lte(f_max, self.continuous_model.getX()[1])) or (not vect_all_lte(self.continuous_model.getX()[0], f_min)):
                            f_min, f_max = self.crop_reachable_area(f_min, f_max)
                            include_0 = True

                        q_min = self.discretizator.q(f_min)
                        q_max = self.discretizator.q(f_max)
                        model[(ksi, sigma)] = (q_min, q_max, include_0)

        print("Symbolic model constructed: DONE")
        return model

    """
    Method that return the set of successor states, which are states between q_min
    and q_max in all terms, if they are not None
    (Abandoned)
    """
    def getSetOfSuccessors(self, q_min, q_max, includes_0):
        successors = []
        if q_min is not None and q_max is not None:
            successor = list(q_min)

            while vect_all_lte(successor, q_max):
                successors.append(tuple(successor.copy()))
                successor[0] += 1
                for i in range(len(successor) - 1):
                    if successor[i] > q_max[i]:
                        successor[i] = q_max[i]
                        successor[i + 1] += 1

        if includes_0:
            successors.append((0,) * self.continuous_model.get_dim_x())

        return successors

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
        # Using numpy grid (bit masking) for faster computation
        R_grid = construct_R_grid(self.Nx, R)

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
                q_min, q_max, includes_0 = self.g[(ksi, sigma)]
                # if the reachable region includes 0 (totaly or partially out of the grid)
                # It cannot be a predecessor of R
                if includes_0:
                    continue        # if includes 0, it is not the right sigma
                # Next, we check if the hyper rectangle delimited by q_min and q_max is in R
                if rectangle_in_R(q_min, q_max, R_grid):
                    return True
        return False

    # method to return the all commands such that g(ksi, sigma) is in R
    def sigma_st_g_ksi_sigma_is_in_R(self, ksi: int, R_grid):
        sigma_set = set()
        for sigma in self.symb_commands:
            if (ksi, sigma) in self.g:
                q_min, q_max, includes_0 = self.g[(ksi, sigma)]
                if includes_0:
                    continue  # if includes 0, it is not the right sigma
                if rectangle_in_R(q_min, q_max, R_grid):
                    sigma_set.add(sigma)
        return sigma_set

    # Getters
    def getAllStates(self):
        return self.symb_states

    def getAllCommands(self):
        return self.symb_commands

    """
    Methods to save the model in a file using pickle so it is not necessary
    to compute it as it takes a long time especially for large models
    """
    def save_model(self, filename):
        try:
            print("Saving symbolic model...")
            with open(filename + ".mdl", "wb") as f:
                pickle.dump(self, f)
                print("Symbolic model saved.")
        except:
            raise

    @classmethod
    def load_model(self, filename):
        try:
            print("Loading symbolic model...")
            with open(filename + ".mdl", "rb") as f:
                model = pickle.load(f)
                print("Symbolic model loaded.")
                return model
        except:
            raise