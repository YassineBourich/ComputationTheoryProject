from SpecificationAutomata.Automaton import Automaton
from UtilityFunctions.Math import vect_all_lte


class ExampleSpecification2D_1(Automaton):
    def __init__(self, symb_model):
        self.symb_model = symb_model

        self.Regions = {
            ((0.5, 0.5), (1.5, 1.5)): ['green', 'lightgreen'],
            ((0, 2.5), (7.5, 4)): ['blue', 'lightblue'],
            ((2.5, 6), (10, 7.5)): ['gold', 'yellow'],
            ((8, 8), (10, 10)): ['orangered', 'lightsalmon'],
        }

        Q = {'a', 'b', 'c', 'd'}
        SIGMA = {0, 1, 2, 3, 4}
        delta = self.transitions_function()
        q0 = 'a'
        F = {'c'}
        super().__init__(Q, SIGMA, delta, q0, F)

    def transitions_function(self):
        return {
            ('a', 0): 'a',
            ('a', 1): 'b',
            ('a', 2): 'd',
            ('a', 3): 'd',
            ('a', 4): 'a',

            ('b', 0): 'b',
            ('b', 1): 'b',
            ('b', 2): 'd',
            ('b', 3): 'd',
            ('b', 4): 'c',

            ('c', 0): 'c',
            ('c', 1): 'c',
            ('c', 2): 'c',
            ('c', 3): 'c',
            ('c', 4): 'c',

            ('d', 0): 'd',
            ('d', 1): 'd',
            ('d', 2): 'd',
            ('d', 3): 'd',
            ('d', 4): 'd',
        }

    def l(self, ksi):
        if ksi == (0,) * self.symb_model.continuous_model.get_dim_x(): return 4

        x_min, x_max = self.symb_model.discretizator.KSI.getPartitionMinAndMax(ksi)

        for i, region in enumerate(self.Regions):
            if vect_all_lte(region[0], x_min) and vect_all_lte(x_max, region[1]):
                return i + 1

        return 0