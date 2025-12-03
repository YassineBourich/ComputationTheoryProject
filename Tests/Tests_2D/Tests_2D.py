import os
from Concretization.ConcreteModel import ConcreteModel
from SymbolicControllers.AutomatonBasedController import AutomatonBasedController
from SymbolicControllers.SymbolicController import SymbolicController
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
from Visualization.Visualization_3D import visualize_trajectory
from SpecificationAutomata.ExampleSpecification_2D_2 import ExampleSpecification2D_2

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

    continuous_sys = ContinuousModel2D(tau, X, U, W)
    print("Continuous system defined.")

    # Defining the reachability method used to construct the symbolic model
    reachability = Reachability(continuous_sys, Dx, Dw)
    reachability_method = ReachabilityMethods.BoundedJacobianMethod
    print("Reachability method defined.")

    # Constructing or loading the Symbolic model (cache to speed up repeated runs)
    Nx = [100, 100]
    Nu = [3, 3]

    model_filename = "SymbolicModel2D_1"
    if os.path.exists(model_filename + ".mdl"):
        symb_model = SymbolicModel.load_model(model_filename)
        print(f"Loaded symbolic model from '{model_filename}'.mdl.")
    else:
        symb_model = SymbolicModel(continuous_sys, reachability, reachability_method, Nx , Nu)
        symb_model.save_model(model_filename)
        print(f"Constructed and saved symbolic model to '{model_filename}'.mdl.")

    # You may try to test this block of code or try to run tests
    """
    controller_filename = "SpecificationController2D_0.ctl"
    # Always (re)build the specification controller to ensure compatibility
    # with the current model and reachability implementation.
    A = ExampleSpecification2D_2(symb_model)
    s = AutomatonBasedController(A, symb_model)
    s.save_controller(controller_filename)
    #s = AutomatonBasedController.load_controller(controller_filename)
    print(f"Constructed and saved specification controller to '{controller_filename}'.")

    c = ConcreteModel(continuous_sys, s)

    # If no initial states satisfy the specification, fall back to all symbolic states
    initial_states = s.Q0 if getattr(s, "Q0", None) else set(symb_model.getAllStates())

    c.construct_trajectory(generate_random_w(symb_model), generate_random_x(initial_states, symb_model))

    #plot_trajectory(c.trajectories.values(), ['red'], A.Regions)
    visualize_trajectory(A, list(c.trajectories.values())[0])

    """

    #SafetyTest(symb_model).run_tests()
    #ReachabilityTest(symb_model).run_tests()
    SpecificationTest(symb_model).test_n_perturbation(50)