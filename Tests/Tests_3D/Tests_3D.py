from SpecificationAutomata.Automaton import Automaton
from SymbolicControllers.AutomatonBasedController import AutomatonBasedController
from SymbolicModels.SymbolicModel import SymbolicModel
from Reachability.ReachabilityMethods import ReachabilityMethods
from Reachability.Reachability import Reachability
from ContinuousModels.Model_3D import ContinuousModel3D
from .SafetyTest import SafetyTest
from .ReachabilityTest import ReachabilityTest
from .SpecificationTest import SpecificationTest
from math import pi
from SymbolicControllers.SafetyController import SafetyController
from Tests.RandomXGenerator import *
from Concretization.ConcreteModel import ConcreteModel
from SymbolicControllers.ReachabilityController import ReachabilityController
from SpecificationAutomata.ExampleSpecification_3D import ExampleSpecification3D
from Visualization.PlotingUtility import plot_trajectory

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
    symb_model = SymbolicModel(continuous_sys, reachability, reachability_method, Nx , Nu)
    #symb_model = SymbolicModel.load_model("SymbolicModel3D_2.mdl")

    #print(symb_model.g)
    print(symb_model.continuous_model)
    symb_model.save_model("SymbolicModel3D_0.mdl")

    Qs = set()
    for ksi in symb_model.getAllStates():
        local_x_min, local_x_max = symb_model.discretizator.KSI.getPartitionMinAndMax(ksi)
        obstacle_overlap = (local_x_min[0] <= 7 and local_x_max[0] >= 3 and
                            local_x_min[1] <= 7 and local_x_max[1] >= 3)
        if obstacle_overlap:
            Qs.add(ksi)

    #s = ReachabilityController(symb_model, Qs)
    # print(len(s.R_list[-1]))
    #s = ReachabilityController.load_model("ReachabilityController3D_3x7_3x7.ctl")
    #s.save_controller("ReachabilityController3D_3x7_3x7.ctl")


    A = ExampleSpecification3D(symb_model)

    s = AutomatonBasedController(A, symb_model)
    s.save_controller("SpecificationController3D_0.ctl")

    c = ConcreteModel(continuous_sys, s)

    c.construct_trajectory(generate_random_w(symb_model), generate_random_x(s.Q0, symb_model))

    plot_trajectory(c.trajectories.values(), ['red'], A.Regions)#{((3, 3), (7, 7)): ['green', 'lightgreen']})

    """Qs1 = set()
    for i in range(20, 41):
        for j in range(20, 41):
            for k in range(0, 10):
                Qs1.add(k * 100 + i * 10 + j)
    s = SafetyController(symb_model, Qs1)"""



    #SafetyTest(symb_model).test_set3()
    #ReachabilityTest(symb_model).test_set1()
    #SpecificationTest(symb_model).test_1_2()