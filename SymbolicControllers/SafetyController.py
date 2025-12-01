from SymbolicControllers.SymbolicController import SymbolicController
import random
import numpy as np

class SafetyController(SymbolicController):
    def __init__(self, symb_model, Qs: set):
        print("Constructing the safety controller...")
        self.symb_model = symb_model
        self.Qs = Qs
        self.R_star = self.getSafetyDomain()
        self.h = self.construct_controller()
        print("Constructing the safety controller: DONE")

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

    def construct_controller(self):
        print("Constructing the controller function...")
        R_star_grid = self.construct_R_grid(self.R_star)
        h = {}
        for ksi in self.R_star:
            sigmas = self.symb_model.sigma_st_g_ksi_sigma_is_in_R(ksi, R_star_grid)
            if sigmas:
                h[ksi] = random.choice(list(sigmas))

        for ksi in self.symb_model.getAllStates():
            if ksi not in h:
                h[ksi] = 1

        return h

    def construct_R_grid(self, R: set):
        R_grid = np.zeros([self.symb_model.Nx[i] + 1 for i in range(self.symb_model.continuous_model.get_dim_x())], dtype=bool)
        for v in R:
            R_grid[v] = True

        return R_grid