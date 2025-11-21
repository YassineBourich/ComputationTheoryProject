from ProjectMath.Math import vec_add, vec_mul_scalar
from .ContinuousSystem import ContinuousSystem

class ContinuousModel2D(ContinuousSystem):
    def __init__(self, tau, X, U, W):
        super().__init__(X, U, W)
        self.tau = tau

    def f(self, x, u, w):
        """
        x(t+1) = x + tau * (u + w)
        """
        try:
            return vec_add(x, vec_mul_scalar(vec_add(u, w), self.tau))
        except:
            raise