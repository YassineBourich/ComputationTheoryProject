from SymbolicModels.SymbolicModel import SymbolicModel
from Reachability.ReachabilityMethods import ReachabilityMethods
from Reachability.Reachability import Reachability
from ContinuousModels.Model_2D import ContinuousModel2D
from .SafetyTest import SafetyTest

def Test2DModel():
    # Defining the continuous_model
    X = [
        [0, 0],
        [10, 10]
    ]
    U = [
        [-1, -1],
        [1, 1]
    ]
    W = [
        [-0.05, -0.05],
        [0.05, 0.05]
    ]
    tau = 1
    continuous_sys = ContinuousModel2D(tau, X, U, W)
    print("Continuous system defined.")

    # Defining the reachability method used to construct the symbolic model
    Dx = lambda u : [[1, 0], [0, 1]]
    Dw = lambda u: [[tau, 0], [0, tau]]
    reachability = Reachability(continuous_sys, Dx, Dw)
    reachability_method = ReachabilityMethods.BoundedJacobianMethod
    print("Reachability method defined.")

    # Constructing the Symbolic model
    Nx = [100, 100]
    Nu = [3, 3]
    print("Constructing the symbolic model...")
    symb_model = SymbolicModel(continuous_sys, reachability, reachability_method, Nx , Nu)
    print("Symbolic model constructed.")

    SafetyTest(symb_model).test_set3()