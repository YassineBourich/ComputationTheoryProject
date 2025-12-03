from SymbolicControllers.SymbolicController import SymbolicController
import random
from UtilityFunctions.NumpyGrid import construct_R_grid

class SafetyController(SymbolicController):
    def __init__(self, symb_model, Qs: set):
        print("Constructing the safety controller...")
        self.symb_model = symb_model
        self.Qs = Qs
        self.R_star = self.getSafetyDomain()
        self.h = self.construct_controller()
        print("Constructing the safety controller: DONE")

    """
    Method to calculate the safety domain (R*) using the fixed point algorithm for safety
    """
    def getSafetyDomain(self):
        print("Constructing the safety domain...")
        k = 0
        Rk = self.Qs.copy()
        print(f"iter {k}: {len(Rk)}")
        Rkp1 = self.Qs.intersection(self.symb_model.Pre(Rk))
        while Rk != Rkp1:
            k += 1
            Rk = Rkp1
            print(f"iter {k}: {len(Rk)}")
            Rkp1 = self.Qs.intersection(self.symb_model.Pre(Rk))

        return Rk

    """
    Constructing the controller function by choosing a random sigma that satisfies
    staying in the safe domain. We use R_star_grip (a numpy grid) for fast computation
    """
    def construct_controller(self):
        print("Constructing the controller function...")
        R_star_grid = construct_R_grid(self.symb_model.Nx, self.R_star)
        h = {}
        default_sigma = next(iter(self.symb_model.getAllCommands()))
        for ksi in self.R_star:
            sigmas = self.symb_model.sigma_st_g_ksi_sigma_is_in_R(ksi, R_star_grid)
            if sigmas:
                h[ksi] = random.choice(list(sigmas))

        for ksi in self.symb_model.getAllStates():
            if ksi not in h:
                h[ksi] = default_sigma

        return h