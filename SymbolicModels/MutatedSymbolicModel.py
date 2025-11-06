class MutatedSymbolicModel:
    def __init__(self, symb_model, Automaton, h1):
        self.symb_model = symb_model
        self.Automaton = Automaton
        self.h1 = h1
        self.g_tield = self.construct_model()

    def construct_model(self):
        model = {}

        for ksi in range(0, self.symb_model.num_of_sym_states + 1):
            for psi in self.Automaton.Q:
                ksi_tield = (psi, ksi)
                for sigma in range(1, self.symb_model.num_of_commands + 1):
                    model[(ksi_tield, sigma)] = self.getSetOfSuccessors(ksi_tield, sigma)

        return model

    def getSetOfSuccessors(self, ksi_tield, sigma):
        ksi_successors = self.symb_model.g[(ksi_tield[1], sigma)]
        successors = set()

        for ksi in ksi_successors:
            psi_successor = self.h1[(ksi_tield[0], ksi)]
            successors.add((psi_successor, ksi))

        return successors

    def Pre(self, R):
        predecessors = set()
        for ksi in range(self.symb_model.num_of_sym_states + 1):
            for psi in self.Automaton.Q:
                ksi_tield = (psi, ksi)
                if self.exists_sigma_st_ksi_is_pre(ksi_tield, R):
                    predecessors.add(ksi_tield)

        return predecessors

    # method to check if there is a command such that g(ksi, sigma) is in R (such that ksi
    # is a predecessor)
    def exists_sigma_st_ksi_is_pre(self, ksi_tield, R):
        for sigma in range(1, self.symb_model.num_of_commands + 1):
            if self.g_tield[(ksi_tield, sigma)] and self.g_tield[(ksi_tield, sigma)].issubset(R):
                return True
        return False

    # method to return the command such that g(ksi_tield, sigma) is in R
    def sigma_st_g_ksi_sigma_is_in_R(self, ksi_tield, R: set):
        for sigma in range(1, self.symb_model.num_of_commands + 1):
            if self.g_tield[(ksi_tield, sigma)] and self.g_tield[(ksi_tield, sigma)].issubset(R):
                return sigma
        return None