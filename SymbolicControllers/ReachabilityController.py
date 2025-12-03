from SymbolicControllers.SymbolicController import SymbolicController
import random
from UtilityFunctions.NumpyGrid import construct_R_grid, construct_R_dictionary, construct_compatibility_grids
from tqdm import tqdm

from SymbolicModels.MutatedSymbolicModel import MutatedSymbolicModel


class ReachabilityController(SymbolicController):
    def __init__(self, symb_model, Qa: set):
        print("Constructing the reachability controller...")
        self.symb_model = symb_model
        self.Qa = Qa
        self.R_list = self.getReachabilityDomain()
        self.R_star = self.R_list[-1]
        self.h = self.construct_controller()
        print("Constructing the reachability controller: DONE")

    """
    Method to calculate the safety domain (R*) using the fixed point algorithm for reachability.
    In this case we store all the Rk's in the R_list
    """
    def getReachabilityDomain(self):
        print("Constructing the reachability domain...")
        k = 0
        R_list = [self.Qa.copy()]
        print(f"iter {k}: {len(R_list[-1])}")
        Rkp1 = R_list[0].union(self.symb_model.Pre(R_list[-1]))
        R_list.append(Rkp1)
        while R_list[-1] != R_list[-2]:
            k += 1
            print(f"iter {k}: {len(R_list[-1])}")
            Rkp1 = R_list[0].union(self.symb_model.Pre(R_list[-1]))
            R_list.append(Rkp1)

        return R_list

    """
    Constructing the controller function by choosing a random sigma that satisfies
    staying in the safe domain. We use R_star_grip (a numpy grid) for fast computation
    """
    def construct_controller(self):
        print("Constructing the controller function...")
        h = {}
        compat_grids = None
        # Choose a deterministic default command that is always valid
        default_sigma = next(iter(self.symb_model.getAllCommands()))
        bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
        for k in range(len(self.R_list) - 1, 1, -1):
            print(f"iter {k}")
            if isinstance(self.symb_model, MutatedSymbolicModel):
                R_prime = construct_R_dictionary(self.R_list[k - 1])
                R_grid_k = construct_R_grid(self.symb_model.symb_model.Nx, set(R_prime.keys()))
                compat_grids = construct_compatibility_grids(self.symb_model.symb_model.Nx, self.symb_model.Automaton.Q, self.symb_model.h1, R_prime)
            else:
                R_grid_k = construct_R_grid(self.symb_model.Nx, self.R_list[k - 1])

            for ksi in tqdm(self.R_list[k], bar_format=bar_format, ncols=80):
                if isinstance(self.symb_model, MutatedSymbolicModel):
                    sigmas = self.symb_model.sigma_st_g_ksi_sigma_is_in_R(ksi, compat_grids, R_grid_k)
                else:
                    sigmas = self.symb_model.sigma_st_g_ksi_sigma_is_in_R(ksi, R_grid_k)
                if sigmas:
                    h[ksi] = random.choice(list(sigmas))

        for ksi in self.symb_model.getAllStates():
            if ksi not in h:
                h[ksi] = default_sigma

        return h

    def isInReachableSet(self, x):
        ksi = self.symb_model.discretizator.q(x)

        return ksi in self.Qa