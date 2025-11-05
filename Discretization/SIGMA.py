from Exceptions.Exceptions import DimensionError, CommandError
from Math.Math import PI

class SIGMA:
    def __init__(self, u_min, u_max, Nu):
        self.u_min = u_min
        self.dim_u = self.getDimU()
        self.setU_max(u_max)
        self.setNu(Nu)
        self.num_of_commands = PI(self.Nu)


    # getters
    def getDimU(self):
        return len(self.u_min)

    def getU_min(self):
        return self.u_min

    def getU_max(self):
        return self.u_max

    def getNu(self):
        return self.Nu

    #setters
    def setDimU(self, dim_u):
        if dim_u == self.dim_u:
            return
        elif dim_u < self.dim_u:
            del self.u_min[dim_u:]
            del self.u_max[dim_u:]
            del self.Nu[dim_u:]
        elif dim_u > self.dim_u:
            self.u_min.extend([0] * (self.dim_u - dim_u))
            self.u_max.extend([0] * (self.dim_u - dim_u))
            self.Nu.extend([0] * (self.dim_u - dim_u))

        self.dim_u = dim_u

    def setU_min(self, u_min):
        if len(u_min) != self.dim_u:
            raise DimensionError("Err1")

        self.u_min = u_min

    def setU_max(self, u_max):
        if len(u_max) != self.dim_u:
            raise DimensionError("Err1")

        self.u_max = u_max

    def setNu(self, Nu):
        if len(Nu) != self.dim_u:
            raise DimensionError("Err1")

        self.Nu = Nu

    # Check dimension
    def check_dimension(self, u):
        if len(u) != self.dim_u:
            raise DimensionError("Err2")

    # Using the congruance to resolve the coordinate of the command in the command space
    def getCommandCoordinates(self, sigma:int):
        command_space_idx = [0] * self.dim_u

        congruance = self.num_of_commands / self.Nu[len(self.Nu) - 1]

        for n in range(self.dim_u - 1, -1, -1):
            command_space_idx[n] = int(sigma / congruance)
            sigma = sigma % congruance
            if n > 0:
                congruance /= self.Nu[n - 1]

        return command_space_idx

    # concretisation interface
    def p(self, sigma):
        if sigma <= 0 or sigma > self.num_of_commands:
            raise CommandError("the index of the command is out of range")

        sigma -= 1
        command_coords = self.getCommandCoordinates(sigma)

        u = []

        # Calculating the central position of the command in its coordinates
        for n in range(self.dim_u):
            partition_width = (self.u_max[n] - self.u_min[n]) / self.Nu[n]
            u.append(self.u_min[n] + partition_width * (command_coords[n] + 1/2))

        return u
