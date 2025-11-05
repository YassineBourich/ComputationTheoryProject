from Math.Math import vec_add, vec_sub, vec_mul_scalar, mat_vec_mul

class TwoDimentionalModel:
    def __init__(self, tau):
        self.tau = tau
        self.dim_x = 2
        self.dim_u = 2
        self.dim_w = 2

    def f(self, x, u, w):
        """
        x(t+1) = x + tau * (u + w)
        """
        try:
            return vec_add(x, vec_mul_scalar(vec_add(u, w), self.tau))
        except:
            raise