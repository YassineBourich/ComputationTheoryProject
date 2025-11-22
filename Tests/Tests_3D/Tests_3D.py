from SymbolicModels.SymbolicModel import SymbolicModel
from Reachability.ReachabilityMethods import ReachabilityMethods
from Reachability.Reachability import Reachability
from ContinuousModels.Model_3D import ContinuousModel3D
from .SafetyTest import SafetyTest
from .ReachabilityTest import ReachabilityTest
from .SpecificationTest import SpecificationTest
from math import pi

tau = 1
def Dx(u):
    return [
        [1, 0, tau * abs(u[0])],
        [0, 1, tau * abs(u[0])],
        [0, 0, 1]]
def Dw(u):
    return [[tau, 0, 0],
            [0, tau, 0],
            [0, 0, tau]]

def Test3DModel():
    # Defining the continuous_model
    X = [
        [0, 0, (-1) * pi],
        [10, 10, pi]
    ]
    U = [
        [0.25, -1],
        [1, 1]
    ]
    W = [
        [-0.05, -0.05, -0.05],
        [0.05, 0.05, 0.05]
    ]
    tau = 1
    continuous_sys = ContinuousModel3D(tau, X, U, W)
    print("Continuous system defined.")

    # Defining the reachability method used to construct the symbolic model
    reachability = Reachability(continuous_sys, Dx, Dw)
    reachability_method = ReachabilityMethods.BoundedJacobianMethod
    print("Reachability method defined.")

    # Constructing the Symbolic model
    Nx = [100, 100, 30]
    Nu = [3, 5]
    #symb_model = SymbolicModel(continuous_sys, reachability, reachability_method, Nx , Nu)
    symb_model = SymbolicModel.load_model("SymbolicModel3D_0.mdl")

    print(symb_model.g)
    print(symb_model.continuous_model)
    #symb_model.save_model("SymbolicModel3D_0.mdl")

    #SafetyTest(symb_model).test_set3()
    ReachabilityTest(symb_model).test_set1()
    #SpecificationTest(symb_model).test_n_perturbation(50)