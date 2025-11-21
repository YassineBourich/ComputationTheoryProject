from Discretization.DiscretSpace import DiscretSpace
from ProjectExceptions.Exceptions import CommandError

class SIGMA(DiscretSpace):
    def __init__(self, u_min, u_max, Nu):
        super().__init__(u_min, u_max, Nu)
        self.u_min = self.vect_min
        self.u_max = self.vect_max
        self.Nu = self.Nv
        self.num_of_commands = self.num_of_discret_elmnts
        self.dim_u = self.dim_v

    # Using the congruance to resolve the coordinate of the command in the command space
    def commandToIndex(self, sigma:int):
        command_idx = [0] * self.dim_u

        congruance = self.num_of_commands / self.Nu[len(self.Nu) - 1]

        for n in range(self.dim_u - 1, -1, -1):
            command_idx[n] = int(sigma / congruance)
            sigma = sigma % congruance
            if n > 0:
                congruance /= self.Nu[n - 1]

        return command_idx

    # concretisation interface
    def p(self, sigma):
        if sigma <= 0 or sigma > self.num_of_commands:
            raise CommandError("the index of the command is out of range")

        sigma -= 1
        command_coords = self.commandToIndex(sigma)

        u = []

        # Calculating the central position of the command in its coordinates
        for n in range(self.dim_u):
            partition_width = (self.u_max[n] - self.u_min[n]) / self.Nu[n]
            u.append(self.u_min[n] + partition_width * (command_coords[n] + 1/2))

        return u