from SpecificationAutomata.Automaton import Automaton
from Math.Math import vect_all_lte


class ExpambleSpecification(Automaton):
    def __init__(self, symb_model):
        self.symb_model = symb_model

        self.Regions = [[[4, 8.5], [5, 9.5]],
            [[8.5, 2], [9.5, 3]],
            [[2, 0.5], [3, 1.5]],
            [[3, 3], [7, 7]]]

        Q = {1, 2, 3, 4, 5}
        SIGMA = {0, 1, 2, 3, 4}
        delta = self.transitions_function()
        super().__init__(Q, SIGMA, delta, 1, {5})

    def transitions_function(self):
        return {
            (1, 0): 1,
            (1, 1): 2,
            (1, 2): 3,
            (1, 3): 1,
            (1, 4): 5,

            (2, 0): 2,
            (2, 1): 2,
            (2, 2): 5,
            (2, 3): 4,
            (2, 4): 5,

            (3, 0): 3,
            (3, 1): 5,
            (3, 2): 3,
            (3, 3): 4,
            (3, 4): 5,

            (4, 0): 4,
            (4, 1): 4,
            (4, 2): 4,
            (4, 3): 4,
            (4, 4): 4,

            (5, 0): 5,
            (5, 1): 5,
            (5, 2): 5,
            (5, 3): 5,
            (5, 4): 5,
        }

    def l(self, ksi):
        if ksi == 0: return 0

        x_min, x_max = self.symb_model.discretisator.KSI.getPartitionMinAndMax(ksi)

        for i in range(len(self.Regions)):
            if vect_all_lte(self.Regions[i][0], x_min) and vect_all_lte(x_max, self.Regions[i][1]):
                return i + 1

        return 0