class ReachabilityController:
    def __init__(self, symb_model, Qa: set):
        self.symb_model = symb_model
        self.Qa = Qa
        self.R_list = self.getReachabilityDomain()
        self.h = self.construct_controller()

    def getReachabilityDomain(self):
        R_list = [self.Qa.copy()]

        Rkp1 = R_list[0].union(self.symb_model.Pre(R_list[-1]))
        R_list.append(Rkp1)
        while R_list[-1] != R_list[-2]:
            Rkp1 = R_list[0].union(self.symb_model.Pre(R_list[-1]))
            R_list.append(Rkp1)

        return R_list

    def construct_controller(self):
        h = {}
        for k in range(len(self.R_list) - 1, 0, -1):
            for ksi in self.R_list[k]:
                sigma = self.symb_model.sigma_st_g_ksi_sigma_is_in_R(ksi, self.R_list[k - 1])
                if sigma:
                    h[ksi] = list(sigma)[0]

        for ksi in self.symb_model.getAllStates():
            if ksi not in h:
                h[ksi] = 1

        return h

    def isInReachableSet(self, x):
        ksi = self.symb_model.discretizator.q(x)

        return ksi in self.Qa