from SymbolicModels.MutatedSymbolicModel import MutatedSymbolicModel
from SymbolicControllers.ReachabilityController import ReachabilityController
from SymbolicControllers.SymbolicController import SymbolicController

class AutomatonBasedController(SymbolicController):
    def __init__(self, Automaton, symb_model):
        self.A = Automaton
        self.symb_model = symb_model

        self.h1 = self.construct_controller_h1()
        self.h2, self.Q0 = self.construct_controller_h2()

    # method to construct h1 using the automaton transition function
    def construct_controller_h1(self):
        h1 = {}
        for ksi in range(self.symb_model.num_of_sym_states + 1):
            for psi in self.A.Q:
                h1[(psi, ksi)] = self.A.delta[(psi, self.A.l(ksi))]

        return h1

    # method to construct h2 using the mutated model g_tield and the reachability controller
    def construct_controller_h2(self):
        # Calculating the mutated model g_tield
        mutated_symb_model = MutatedSymbolicModel(self.symb_model, self.A, self.h1)
        # Calculating the reachable states PSI_f x KSI
        reachable_states = self.final_product_states()

        # Introducing the reachability controller
        mutated_reachability_controller = ReachabilityController(mutated_symb_model, reachable_states)

        # Extracting the controller's data
        Q0_tield = mutated_reachability_controller.R_list[-1]
        h_tield = mutated_reachability_controller.h

        # Constructing the set Q0 and returning the results
        Q0 = set()
        for ksi in range(self.symb_model.num_of_sym_states + 1):
            if (self.h1[(self.A.q0, ksi)], ksi) in Q0_tield:
                Q0.add(ksi)

        return h_tield, Q0

    def final_product_states(self):
        final_reachable_states = set()
        for ksi in range(self.symb_model.num_of_sym_states + 1):
            for psi in self.A.F:
                ksi_tield_f = (psi, ksi)
                final_reachable_states.add(ksi_tield_f)

        return final_reachable_states

    def initial_product_states(self):
        initial_product_states = set()
        for ksi in range(self.symb_model.num_of_sym_states + 1):
            psi_0 = self.A.q0
            ksi_tield_f = (psi_0, ksi)
            initial_product_states.add(ksi_tield_f)

        return initial_product_states

    def isSpecificationAchieved(self, psi, x):
        ksi_tield = (psi, self.symb_model.discretizator.KSI.q(x))

        return ksi_tield in self.final_product_states()