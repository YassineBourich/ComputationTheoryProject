from ProjectMath.Math import vec_add, vec_sub, vec_mul_scalar, mat_vec_mul, vec_abs


class Reachability:
    def __init__(self, model, D_x=None, D_w=None):
        self.f = model.f
        self.D_x = D_x
        self.D_w = D_w

    # monotone approximation method
    def reachable_interval_Monotone(self, x_lower, x_upper, u, w_lower, w_upper):
        f_min = self.f(x_lower, u, w_lower)
        f_max = self.f(x_upper, u, w_upper)
        return f_min, f_max

    # approximation with Bounds
    def reachable_interval_Bounds(self, x_lower, x_upper, u, w_lower, w_upper):
        if self.D_x is None or self.D_w is None:
            raise ValueError("D_x and D_w must be defined")

        try:
            # x* = (x_upper + x_lower)/2
            # w* = (w_upper + w_lower)/2
            x_star = vec_mul_scalar(vec_add(x_lower, x_upper), 0.5)
            w_star = vec_mul_scalar(vec_add(w_lower, w_upper), 0.5)

            # delta_x = (x_upper - x_lower)/2
            # delta_w = (w_upper - w_lower)/2
            delta_x = vec_mul_scalar(vec_sub(x_upper, x_lower), 0.5)
            delta_w = vec_mul_scalar(vec_sub(w_upper, w_lower), 0.5)

            #f* = f(x*, u, w*)
            f_star = self.f(x_star, u, w_star)

            Dx_delta_x = mat_vec_mul(self.D_x(u), delta_x)
            Dw_delta_w = mat_vec_mul(self.D_w(u), delta_w)

            abs_margin = vec_add(vec_abs(Dx_delta_x), vec_abs(Dw_delta_w))  # Dx delta(x) + Dw delta(w)

            f_lower = vec_sub(f_star, abs_margin)
            f_upper = vec_add(f_star, abs_margin)

            return f_lower, f_upper
        except:
            raise