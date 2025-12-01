import numpy as np
from ProjectMath.Math import vect_all_lte
from tqdm import tqdm

class MutatedSymbolicModel:
    def __init__(self, symb_model, Automaton, h1):
        self.symb_model = symb_model
        self.Automaton = Automaton
        self.h1 = h1
        self.g_tield = self.construct_model()

    def construct_model(self):
        model = {}
        print("Constructing the mutated symbolic model...")
        bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
        for ksi in tqdm(self.symb_model.getAllStates(), bar_format=bar_format, ncols=80):
            for psi in self.Automaton.Q:
                ksi_tield = (psi, ksi)
                for sigma in self.symb_model.getAllCommands():
                    model[(ksi_tield, sigma)] = self.symb_model.g[(ksi, sigma)] #self.getSetOfSuccessors(ksi_tield, sigma)

        print("Mutated symbolic model constructed: DONE")
        return model

    def getSetOfSuccessors(self, ksi_tield, sigma):
        print("Resolving successors of (" + str(ksi_tield) + ", " + str(sigma) + ")...")
        ksi_successors = self.symb_model.g[(ksi_tield[1], sigma)]
        successors = set()

        for ksi_successor in ksi_successors:
            psi_successor = self.h1[(ksi_tield[0], ksi_successor)]
            successors.add((psi_successor, ksi_successor))

        return successors

    def Pre(self, R):
        R_prime = self.construct_R_dictionary(R)
        R_grid = self.construct_R_grid(set(R_prime.keys()))
        compat_grids = self.construct_compatibility_grids(R_prime)

        predecessors = set()
        bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
        for ksi_tield in tqdm(self.getAllStates(), bar_format=bar_format, ncols=80):
            if self.exists_sigma_st_ksi_is_pre(ksi_tield, compat_grids, R_grid):
                predecessors.add(ksi_tield)
        return predecessors

    # method to check if there is a command such that g(ksi, sigma) is in R (such that ksi
    # is a predecessor)
    def exists_sigma_st_ksi_is_pre(self, ksi_tield, compat_grids, R_grid):
        for sigma in self.symb_model.getAllCommands():
            if (ksi_tield, sigma) in self.g_tield:
                q_min, q_max = self.g_tield[(ksi_tield, sigma)]
                if not self.rectangle_in_R(q_min, q_max, R_grid):
                    continue
                if self.states_are_compatible_grid(q_min, q_max, ksi_tield[0], compat_grids):
                    return True
        return False

    # method to return the command such that g(ksi_tield, sigma) is in R
    def sigma_st_g_ksi_sigma_is_in_R(self, ksi_tield, compat_grids, R_grid):
        sigma_set = set()
        for sigma in self.symb_model.getAllCommands():
            if (ksi_tield, sigma) in self.g_tield:
                q_min, q_max = self.g_tield[(ksi_tield, sigma)]
                if not self.rectangle_in_R(q_min, q_max, R_grid):
                    continue
                if self.states_are_compatible_grid(q_min, q_max, ksi_tield[0], compat_grids):
                    sigma_set.add(sigma)
        return sigma_set

    def construct_R_dictionary(self, R: set):
        R_dict = {}

        for ksi_tield in R:
            if ksi_tield[1] in R_dict:
                R_dict[ksi_tield[1]].add(ksi_tield[0])
            else:
                R_dict[ksi_tield[1]] = {ksi_tield[0]}

        return R_dict

    def states_are_compatible(self, q_min, q_max, psi, R_prime):
        for ksi_plus in R_prime:
            if vect_all_lte(q_min, ksi_plus) and vect_all_lte(ksi_plus, q_max):
                if self.h1[(psi, ksi_plus)] not in R_prime[ksi_plus]:
                    return False
        return True

    def construct_R_grid(self, R: set):
        R_grid = np.zeros([self.symb_model.Nx[i] + 1 for i in range(self.symb_model.continuous_model.get_dim_x())], dtype=bool)
        for v in R:
            R_grid[v] = True

        return R_grid

    def rectangle_in_R(self, q_min, q_max, R_grid):
        # Build slice for each dimension
        slices = tuple(slice(a, b + 1) for a, b in zip(q_min, q_max))
        # Check if all states in rectangle are in R
        return R_grid[slices].all()

    def construct_compatibility_grids(self, R_prime):
        """
        Precompute, for each automaton state psi, a boolean grid over the
        symbolic state space such that grid_psi[ksi] is True iff:
          - ksi is in R (i.e. appears in R_prime), and
          - h1[(psi, ksi)] is also in the allowed set R_prime[ksi].

        This turns the per-rectangle universal check into a fast NumPy slice
        `.all()` instead of iterating over all states in R for every rectangle.
        """
        # Shape of the state grid
        shape = [self.symb_model.Nx[i] + 1 for i in range(self.symb_model.continuous_model.get_dim_x())]

        # Start with all True; cells not in R will be filtered out by R_grid
        compat_grids = {
            psi: np.ones(shape, dtype=bool) for psi in self.Automaton.Q
        }

        # Only states present in R_prime matter for compatibility
        for ksi_plus, psi_set in R_prime.items():
            for psi in self.Automaton.Q:
                # Compatible if successor is one of the allowed psi for this ksi_plus
                compat_grids[psi][ksi_plus] = self.h1[(psi, ksi_plus)] in psi_set

        return compat_grids

    def states_are_compatible_grid(self, q_min, q_max, psi, compat_grids):
        """
        Fast compatibility check using precomputed grids.
        Assumes that rectangle_in_R(q_min, q_max, R_grid) has already been
        verified, so every point in the rectangle is in R.
        """
        grid = compat_grids[psi]
        return self.rectangle_in_R(q_min, q_max, grid)

    def getAllStates(self):
        states = set()
        for ksi in self.symb_model.getAllStates():
            for psi in self.Automaton.Q:
                states.add((psi, ksi))

        return states