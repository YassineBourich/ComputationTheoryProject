import numpy as np

def construct_R_grid(Nx, R: set):
    R_grid = np.zeros([Nx[i] + 1 for i in range(len(Nx))],
                      dtype=bool)
    for v in R:
        R_grid[v] = True

    return R_grid

def construct_compatibility_grids(Nx, Q, h1, R_prime):
    # Shape of the state grid
    shape = [Nx[i] + 1 for i in range(len(Nx))]

    # Start with all False; only set to True for compatible states
    compat_grids = {
        psi: np.zeros(shape, dtype=bool) for psi in Q
    }

    # Only states present in R_prime matter for compatibility
    for ksi_plus, psi_set in R_prime.items():
        for psi in Q:
            # Compatible if the automaton state after transition (h1[(psi, ksi_plus)])
            # is one of the allowed automaton states for ksi_plus in R
            compat_grids[psi][ksi_plus] = h1[(psi, ksi_plus)] in psi_set

    return compat_grids

# function to check if a hyper rectangle delimited by q_min and q_max is included in R
def rectangle_in_R(q_min, q_max, R_grid):
    # Build slice for each dimension
    slices = tuple(slice(a, b + 1) for a, b in zip(q_min, q_max))
    # Check if all states in rectangle are in R
    return R_grid[slices].all()

# function to tranform a set of pairs to dictionary
def construct_R_dictionary(R: set):
    R_dict = {}

    for ksi_tield in R:
        if ksi_tield[1] in R_dict:
            R_dict[ksi_tield[1]].add(ksi_tield[0])
        else:
            R_dict[ksi_tield[1]] = {ksi_tield[0]}

    return R_dict