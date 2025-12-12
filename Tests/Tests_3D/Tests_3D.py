import os
from SpecificationAutomata.Automaton import Automaton
from SymbolicControllers.AutomatonBasedController import AutomatonBasedController
from SymbolicControllers.SymbolicController import SymbolicController
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
from Visualization.Visualization_3D import visualize_trajectory

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

    # Constructing or loading the symbolic model (cache to speed up repeated runs)
    Nx = [50, 50, 15]
    Nu = [3, 5]
    model_filename = "SymbolicModel3D_50x50x15"
    if os.path.exists(model_filename + ".mdl"):
        symb_model = SymbolicModel.load_model(model_filename)
        print(f"Loaded symbolic model from '{model_filename}'.mdl.")
    else:
        symb_model = SymbolicModel(continuous_sys, reachability, reachability_method, Nx , Nu)
        symb_model.save_model(model_filename)
        print(f"Constructed and saved symbolic model to '{model_filename}'.mdl.")


    # You may try to test these blocks of code or try to run tests
    """
    controller_filename = "SpecificationController3D_50x50x15"
    # Always (re)build the specification controller to ensure compatibility
    # with the current model and reachability implementation.
    Automaton = ExampleSpecification3D(symb_model)
    #s = AutomatonBasedController(Automaton, symb_model)
    #s.save_controller(controller_filename)
    s = AutomatonBasedController.load_controller(controller_filename)
    print(f"Constructed and saved specification controller to '{controller_filename}'.")

    c = ConcreteModel(continuous_sys, s)

    # If no initial states satisfy the specification, fall back to all symbolic states
    print("Q0: " + str(s.Q0))
    initial_states = s.Q0 if getattr(s, "Q0", None) else set(symb_model.getAllStates())
    #initial_states = s.R_star
    c.construct_trajectory(generate_random_w(symb_model), generate_random_x(initial_states, symb_model))

    plot_trajectory(c.trajectories.values(), ['red'], Automaton.Regions)
    visualize_trajectory(Automaton.Regions, list(c.trajectories.values())[0])
    """
    # Specialized tests from the module Tests:

    #SafetyTest(symb_model).run_tests()
    #ReachabilityTest(symb_model).run_tests()
    #SpecificationTest(symb_model).test_n_perturbation(50)