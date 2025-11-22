from SymbolicControllers.SymbolicController import SymbolicController

class SafetyController(SymbolicController):
    def __init__(self, symb_model, Qs: set):
        self.symb_model = symb_model
        self.Qs = Qs
        self.R_list = self.getSafetyDomain()
        self.h = self.construct_controller()

    def getSafetyDomain(self):
        R_list = [self.Qs.copy()]

        Rkp1 = R_list[0].intersection(self.symb_model.Pre(R_list[-1]))
        R_list.append(Rkp1)
        while R_list[-1] != R_list[-2]:
            Rkp1 = R_list[0].intersection(self.symb_model.Pre(R_list[-1]))
            R_list.append(Rkp1)

        return R_list

    def construct_controller(self):
        h = {}
        for ksi in self.R_list[-1]:
            sigma = self.symb_model.sigma_st_g_ksi_sigma_is_in_R(ksi, self.R_list[-1])
            if sigma:
                h[ksi] = list(sigma)[0]

        for ksi in self.symb_model.getAllStates():
            if ksi not in h:
                h[ksi] = 1

        return h