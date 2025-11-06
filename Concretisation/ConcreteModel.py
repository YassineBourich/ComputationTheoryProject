class ConcreteModel:
    def __init__(self, continuous_sys, symb_controller):
        self.continuous_sys = continuous_sys
        self.symb_controller = symb_controller
        self.q = self.symb_controller.symb_model.discretisator.q
        self.p = self.symb_controller.symb_model.discretisator.p

        self.trajectories = {}

    def construct_trajectory(self, w, x0):
        self.trajectories[w] = [x0]
        t = 0
        #psi_init = self.symb_controller.A.q0
        #psi_t = psi_init
        while t < 100:
            print(self.trajectories[w])
            t += 1
            x_t = self.trajectories[w][-1]
            #psi_t = self.symb_controller.h1[(psi_t, self.q(x_t))]
            u_t = self.p(self.symb_controller.h[self.q(x_t)])

            x_tp1 = self.continuous_sys.f(x_t, u_t, w)
            self.trajectories[w].append(x_tp1)

        return self.trajectories[w]