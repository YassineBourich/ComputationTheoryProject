from SymbolicModels.SymbolicModel import SymbolicModel
from Reachability.ReachabilityMethods import ReachabilityMethods
from Reachability.Reachability import Reachability
from ContinuousModels.Model_2D import TwoDimentionalModel
from SymbolicControllers.AutomatonBasedController import AutomatonBasedController
from SpecificationAutomata.ExampleSpecification import ExpambleSpecification
from Concretisation.ConcreteModel import ConcreteModel
from SymbolicControllers.SafetyController import SafetyController
from SymbolicControllers.ReachabilityController import ReachabilityController
from PlotingUtility import TrajectoryPloter

tau = 1
continuous_sys = TwoDimentionalModel(tau)
reachability = Reachability(continuous_sys)
reachability_method = ReachabilityMethods.MonotonyBasedMethod
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
Nx = [100, 100]
Nu = [3, 3]

print("Constructing the symbolic model...")
model = SymbolicModel(reachability, reachability_method, X, U, W, Nx , Nu)
"""Qs = set()

for j in range(40, 61):
    for i in range(30, 51):
        Qs.add(j * 100 + i)"""

Qs = {43, 44, 45, 53, 54, 55, 63, 64, 65}

#c = SafetyController(model, Qs)
#r = ReachabilityController(model, Qs)

#print(model.g)
#print(r.R_list)

print("Defining the specification automaton...")
Automaton = ExpambleSpecification(model)
print("Constructing the controller...")
AC = AutomatonBasedController(Automaton, model)

print("Concrete model: ")
concrete_model = ConcreteModel(continuous_sys, AC)
"""
ksi0 = 51

def construct_trajectory(model, controller, ksi0):
    S = [ksi0]
    t = 0
    #psi_init = controller.A.q0
    #psi_t = psi_init
    while t < 100:
        print(S)
        t += 1
        #psi_t = controller.h1[(psi_t, S[-1])]
        sigma_t = controller.h[S[-1]]

        ksi_tp1 = model.get_next_state(S[-1], sigma_t)
        print("ksi at " + str(t) + " is " + str(ksi_tp1))
        S.append(ksi_tp1)

    return S
"""
print("Running the program...")
#print(construct_trajectory(model, c, ksi0))

w = (0.02, 0.01)

print(concrete_model.construct_trajectory(w, [0.8, 4.5]))

TrajectoryPloter(concrete_model.trajectories[w])