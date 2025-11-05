from Discretization.KSI import KSI
from Discretization.SIGMA import SIGMA

class Discretizator:
    def __init__(self, x_min, x_max, u_min, u_max, Nx, Nu):
        self.KSI = KSI(x_min, x_max, Nx)
        self.SIGMA = SIGMA(u_min, u_max, Nu)

    # abstraction interface
    def q(self, x):
        try:
            return self.KSI.q(x)
        except:
            raise

    # method to get partition min and max
    def getPartitionMinAndMax(self, ksi: int):
        try:
            return self.KSI.getPartitionMinAndMax(ksi)
        except:
            raise

    # concretisation interface
    def p(self, sigma: int):
        try:
            return self.SIGMA.p(sigma)
        except:
            raise