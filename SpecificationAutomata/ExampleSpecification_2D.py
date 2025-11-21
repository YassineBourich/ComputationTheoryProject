from SpecificationAutomata.Automaton import Automaton
from ProjectMath.Math import vect_all_lte


class ExampleSpecification2D(Automaton):
    def __init__(self, symb_model):
        self.symb_model = symb_model

        self.Regions = {
            ((4, 8.5), (5, 9.5)): ['green', 'lightgreen'],
            ((8.5, 2), (9.5, 3)): ['blue', 'lightblue'],
            ((2, 0.5), (3, 1.5)): ['gold', 'yellow'],
            ((3, 3), (7, 7)): ['orangered', 'lightsalmon'],
        }

        Q = {'a', 'b', 'c', 'd', 'e'}
        SIGMA = {0, 1, 2, 3, 4}
        delta = self.transitions_function()
        q0 = 'a'
        F = {'d'}
        super().__init__(Q, SIGMA, delta, q0, F)

    def transitions_function(self):
        return {
            ('a', 0): 'a',
            ('a', 1): 'b',
            ('a', 2): 'c',
            ('a', 3): 'a',
            ('a', 4): 'e',

            ('b', 0): 'b',
            ('b', 1): 'b',
            ('b', 2): 'e',
            ('b', 3): 'd',
            ('b', 4): 'e',

            ('c', 0): 'c',
            ('c', 1): 'e',
            ('c', 2): 'c',
            ('c', 3): 'd',
            ('c', 4): 'e',

            ('d', 0): 'd',
            ('d', 1): 'd',
            ('d', 2): 'd',
            ('d', 3): 'd',
            ('d', 4): 'd',

            ('e', 0): 'e',
            ('e', 1): 'e',
            ('e', 2): 'e',
            ('e', 3): 'e',
            ('e', 4): 'e',
        }

    def l(self, ksi):
        if ksi == 0: return 4

        x_min, x_max = self.symb_model.discretizator.KSI.getPartitionMinAndMax(ksi)

        for i, region in enumerate(self.Regions):
            if vect_all_lte(region[0], x_min) and vect_all_lte(x_max, region[1]):
                return i + 1

        return 0