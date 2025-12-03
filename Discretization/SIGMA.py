from Discretization.DiscretSpace import DiscretSpace
from ProjectExceptions.Exceptions import CommandError
from UtilityFunctions.Math import vect_all_lte

class SIGMA(DiscretSpace):
    def __init__(self, u_min, u_max, Nu):
        super().__init__(u_min, u_max, Nu)
        self.u_min = self.vect_min
        self.u_max = self.vect_max
        self.Nu = self.Nv
        self.num_of_commands = self.num_of_discret_elmnts
        self.dim_u = self.dim_v

    # concretisation interface
    def p(self, sigma):
        """
        Concretization interface.

        `sigma` can be either:
          - an integer command index in [1, num_of_commands], or
          - a tuple/list of per-dimension indices (1-based) of length dim_u.
        """
        # Accept integer indices by converting them to per-dimension coordinates
        if (vect_all_lte(sigma, (0,) * self.dim_u) and sigma != (0,) * self.dim_u) or (not vect_all_lte(sigma, self.Nu)):
            raise CommandError("the index of the command is out of range")

        u = []

        # Calculating the central position of the command in its coordinates
        for n in range(self.dim_u):
            partition_width = (self.u_max[n] - self.u_min[n]) / self.Nu[n]
            u.append(self.u_min[n] + partition_width * (sigma[n] - 0.5))

        return tuple(u)

    def getAllCommands(self):
        symb_commands = set()
        sigma = [1] * self.dim_u
        while vect_all_lte(sigma, self.Nu):
            symb_commands.add(tuple(sigma.copy()))
            sigma[0] += 1
            for i in range(self.dim_u - 1):
                if sigma[i] > self.Nu[i]:
                    sigma[i] = 1
                    sigma[i + 1] += 1

        return symb_commands