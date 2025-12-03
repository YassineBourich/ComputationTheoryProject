from UtilityFunctions.Math import vect_all_lte
from tqdm import tqdm
from UtilityFunctions.NumpyGrid import *


class MutatedSymbolicModel:
    def __init__(self, symb_model, Automaton, h1):
        self.symb_model = symb_model
        self.Automaton = Automaton
        self.h1 = h1

    # Method to calculate successor of ksi_tield (Abandoned)
    def getSetOfSuccessors(self, ksi_tield, sigma):
        #print("Resolving successors of (" + str(ksi_tield) + ", " + str(sigma) + ")...")
        qmin, qmax, includes_0 = self.symb_model.g[(ksi_tield[1], sigma)]
        ksi_successors = self.symb_model.getSetOfSuccessors(qmin, qmax, includes_0)
        successors = set()

        for ksi_successor in ksi_successors:
            psi_successor = self.h1[(ksi_tield[0], ksi_successor)]
            successors.add((psi_successor, ksi_successor))

        return successors

    def Pre(self, R):
        """
        Calculate predecessors of set R.
        
        Args:
            R: Set of states (psi, ksi) tuples
        
        Returns:
            Set of predecessor states
        """
        R_prime = construct_R_dictionary(R)
        R_grid = construct_R_grid(self.symb_model.Nx, set(R_prime.keys()))
        compat_grids = construct_compatibility_grids(self.symb_model.Nx, self.Automaton.Q, self.h1, R_prime)

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
            # Check if the key exists in g before accessing (fixes KeyError bug)
            if (ksi_tield[1], sigma) not in self.symb_model.g:
                continue
            q_min, q_max, includes_0 = self.symb_model.g[(ksi_tield[1], sigma)]
            if includes_0:
                continue
            if not rectangle_in_R(q_min, q_max, R_grid):
                continue
            if self.states_are_compatible_grid(q_min, q_max, ksi_tield[0], compat_grids):
                return True
        return False

    # method to return the commands such that g(ksi_tield, sigma) is in R
    def sigma_st_g_ksi_sigma_is_in_R(self, ksi_tield, compat_grids, R_grid):
        sigma_set = set()
        for sigma in self.symb_model.getAllCommands():
            # Check if the key exists in g before accessing (fixes KeyError bug)
            if (ksi_tield[1], sigma) not in self.symb_model.g:
                continue
            q_min, q_max, includes_0 = self.symb_model.g[(ksi_tield[1], sigma)]
            if includes_0:
                continue
            if not rectangle_in_R(q_min, q_max, R_grid):
                continue
            if self.states_are_compatible_grid(q_min, q_max, ksi_tield[0], compat_grids):
                sigma_set.add(sigma)
        return sigma_set

    def states_are_compatible_grid(self, q_min, q_max, psi, compat_grids):
        """
        Fast compatibility check using precomputed grids.
        Assumes that rectangle_in_R(q_min, q_max, R_grid) has already been
        verified, so every point in the rectangle is in R.
        """
        grid = compat_grids[psi]
        return rectangle_in_R(q_min, q_max, grid)

    def getAllStates(self):
        states = set()
        for ksi in self.symb_model.getAllStates():
            for psi in self.Automaton.Q:
                states.add((psi, ksi))

        return states

    def getAllCommands(self):
        """
        The mutated model shares the same command space as the underlying
        symbolic model, so we simply delegate.
        """
        return self.symb_model.getAllCommands()