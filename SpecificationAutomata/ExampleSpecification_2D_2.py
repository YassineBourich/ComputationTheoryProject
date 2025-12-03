from SpecificationAutomata.Automaton import Automaton
from UtilityFunctions.Math import vect_all_lte


class ExampleSpecification2D_2(Automaton):
    def __init__(self, symb_model):
        self.symb_model = symb_model

        self.Regions = {
            ((0.5, 0.5), (1.5, 1.5)): ['green', 'lightgreen'],
            ((6.5, 2.5), (7.5, 4)): ['blue', 'lightblue'],
            ((0, 6), (2, 7.5)): ['gold', 'yellow'],
            ((8, 8), (10, 10)): ['orangered', 'lightsalmon'],
        }

        Q = {'a', 'b', 'c', 'd', 'e', 'f'}
        SIGMA = {0, 1, 2, 3, 4}
        delta = self.transitions_function()
        q0 = 'a'
        F = {'e'}
        super().__init__(Q, SIGMA, delta, q0, F)

    def transitions_function(self):
        return {
            ('a', 0): 'a',
            ('a', 1): 'b',
            ('a', 2): 'f',
            ('a', 3): 'f',
            ('a', 4): 'f',

            ('b', 0): 'b',
            ('b', 1): 'b',
            ('b', 2): 'c',
            ('b', 3): 'f',
            ('b', 4): 'f',

            ('c', 0): 'c',
            ('c', 1): 'f',
            ('c', 2): 'c',
            ('c', 3): 'd',
            ('c', 4): 'f',

            ('d', 0): 'd',
            ('d', 1): 'f',
            ('d', 2): 'f',
            ('d', 3): 'd',
            ('d', 4): 'e',

            ('e', 0): 'e',
            ('e', 1): 'e',
            ('e', 2): 'e',
            ('e', 3): 'e',
            ('e', 4): 'e',

            ('f', 0): 'f',
            ('f', 1): 'f',
            ('f', 2): 'f',
            ('f', 3): 'f',
            ('f', 4): 'f',
        }

    def l(self, ksi):
        if ksi == (0,) * self.symb_model.continuous_model.get_dim_x(): return 4

        x_min, x_max = self.symb_model.discretizator.KSI.getPartitionMinAndMax(ksi)

        for i, region in enumerate(self.Regions):
            if vect_all_lte(region[0], x_min) and vect_all_lte(x_max, region[1]):
                return i + 1

        return 0