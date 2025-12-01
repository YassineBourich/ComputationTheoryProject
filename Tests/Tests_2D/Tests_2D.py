from Concretization.ConcreteModel import ConcreteModel
from SymbolicControllers.AutomatonBasedController import AutomatonBasedController
from SymbolicControllers.ReachabilityController import ReachabilityController
from SymbolicControllers.SafetyController import SafetyController
from SymbolicModels.SymbolicModel import SymbolicModel
from Reachability.ReachabilityMethods import ReachabilityMethods
from Reachability.Reachability import Reachability
from ContinuousModels.Model_2D import ContinuousModel2D
from .SafetyTest import SafetyTest
from .ReachabilityTest import ReachabilityTest
from .SpecificationTest import SpecificationTest
from Tests.RandomXGenerator import *
from Visualization.PlotingUtility import plot_trajectory
from SpecificationAutomata.ExampleSpecification_2D import ExampleSpecification2D

tau = 1
def Dx(u):
    return [
        [1, 0],
        [0, 1]]
def Dw(u):
    return [[tau, 0],
            [0, tau]]

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
    reachability = Reachability(continuous_sys, Dx, Dw)
    reachability_method = ReachabilityMethods.BoundedJacobianMethod
    print("Reachability method defined.")

    # Constructing the Symbolic model
    Nx = [100, 100]
    Nu = [3, 3]
    symb_model = SymbolicModel(continuous_sys, reachability, reachability_method, Nx , Nu)

    Qs = set()
    for ksi in symb_model.getAllStates():
        local_x_min, local_x_max = symb_model.discretizator.KSI.getPartitionMinAndMax(ksi)
        obstacle_overlap = (local_x_min[0] < 7 and local_x_max[0] > 3 and
                            local_x_min[1] < 7 and local_x_max[1] > 3)
        if obstacle_overlap:
            Qs.add(ksi)

    #s = SafetyController(symb_model, Qs)
    #print(len(s.R_list[-1]))

    A = ExampleSpecification2D(symb_model)
    s = AutomatonBasedController(A, symb_model)

    c = ConcreteModel(continuous_sys, s)

    c.construct_trajectory(generate_random_w(symb_model), generate_random_x(s.Q0, symb_model))

    plot_trajectory(c.trajectories.values(), ['red'], A.Regions)#{((3, 3), (7, 7)): ['green', 'lightgreen']})

    #symb_model.save_model("SymbolicModel2D_0.mdl")

    #symb_model = SymbolicModel.load_model("SymbolicModel2D_0.mdl")

    #SafetyTest(symb_model).test_set2()
    #ReachabilityTest(symb_model).test_set2()
    #SpecificationTest(symb_model).test_n_perturbation(50)