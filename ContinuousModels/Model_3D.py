from .ContinuousSystem import ContinuousSystem
from math import cos, sin, pi

class ContinuousModel3D(ContinuousSystem):
    def __init__(self, tau, X, U, W):
        super().__init__(X, U, W)
        self.tau = tau

    def f(self, x, u, w):
        """
        x1(t+1) = x1(t) + tau * (u1(t) * cos(x3(t)) + w1(t))
        x2(t+1) = x2(t) + tau * (u1(t) * sin(x3(t)) + w2(t))
        x3(t+1) = (x3(t) + tau * (u2(t) + w3(t))) % (2 * pi)
        """
        try:
            f1 = x[0] + self.tau * (u[0] * cos(x[2]) + w[0])
            f2 = x[1] + self.tau * (u[0] * sin(x[2]) + w[1])
            f3 = ((x[2] + self.tau * (u[1] + w[2])) % (2 * pi)) - pi

            return [f1, f2, f3]
        except:
            raise