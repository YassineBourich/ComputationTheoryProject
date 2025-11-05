from SymbolicModel import SymbolicModel
from Reachability.ReachabilityMethods import ReachabilityMethods
from Reachability.Reachability import Reachability
from ContinuousModels.Model_2D import TwoDimentionalModel

model = TwoDimentionalModel(0.1)
reachability = Reachability(model)
reachability_method = ReachabilityMethods.MonotonyBasedMethod
X = [
    [0, 0],
    [10, 10]
]
U = [
    [-1, 1],
    [-1, 1]
]
W = [
    [-1, 1],
    [-1, 1]
]
Nx = [10, 10]
Nu = [3, 3]

s = SymbolicModel(reachability, reachability_method, X, U, W, Nx , Nu)

print(s.getSetOfSuccessors([7.5, 7.2], [9.9, 8.8]))
print(s.g)
print(s.Pre({11, 12, 13, 14, 15, 16, 17, 25, 26, 35, 36}))