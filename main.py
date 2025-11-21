from SymbolicModels.SymbolicModel import SymbolicModel
from Reachability.ReachabilityMethods import ReachabilityMethods
from Reachability.Reachability import Reachability
from ContinuousModels.Model_2D import TwoDimentionalModel
from SymbolicControllers.AutomatonBasedController import AutomatonBasedController
from SpecificationAutomata.ExampleSpecification import ExpambleSpecification
from Concretisation.ConcreteModel import ConcreteModel
from Visualization.PlotingUtility import plot_trajectory
from Visualization.Visualization_3D import visualize_trajectory

tau = 1
continuous_sys = TwoDimentionalModel(tau)

Dx = lambda u : [[1, 0], [0, 1]]
Dw = lambda u: [[tau, 0], [0, tau]]
reachability = Reachability(continuous_sys, Dx, Dw)
reachability_method = ReachabilityMethods.BoundedJacobianMethod
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
"""
h1 = {}
for ksi in range(model.num_of_sym_states + 1):
    for psi in Automaton.Q:
        h1[(psi, ksi)] = Automaton.delta[(psi, Automaton.l(ksi))]

final_reachable_states = set()
for ksi in range(model.num_of_sym_states + 1):
    for psi in Automaton.F:
        ksi_tield_f = (psi, ksi)
        final_reachable_states.add(ksi_tield_f)

mutated_symb_model = MutatedSymbolicModel(model, Automaton, h1)

mutated_reachability_controller = ReachabilityController(mutated_symb_model, final_reachable_states)
"""
print("Concrete model: ")
concrete_model = ConcreteModel(continuous_sys, AC)
"""
ksi0 = 2823

def construct_trajectory(Mmodel, controller, x0, w):
    t = 0
    #psi_init = controller.A.q0
    #psi_t = psi_init
    Conc_traj = [x0]
    ksi0 = model.discretisator.q(x0)
    psi_0 = h1[(Automaton.q0, ksi0)]
    ksi_tield_0 = (psi_0, ksi0)
    S = [ksi_tield_0]
    print(Mmodel.g_tield)
    visited = {ksi_tield_0}
    while S[-1] not in final_reachable_states:#t < 100:
        print(S)
        t += 1
        #psi_t = controller.h1[(psi_t, S[-1])]
        sigma_t = controller.h[S[-1]]

        xtp1 = continuous_sys.f(Conc_traj[-1], model.discretisator.p(sigma_t), w)
        Conc_traj.append(xtp1)

        next_states = Mmodel.g_tield[(S[-1], sigma_t)]
        for ksi_tp1 in next_states:
            if ksi_tp1 not in visited:
                S.append(ksi_tp1)
                visited.add(ksi_tp1)

                print("ksi at " + str(t) + " is " + str(ksi_tp1))
                break

    print(controller.R_list)
    return S, Conc_traj

print("Running the program...")
traj, Conc_traj = construct_trajectory(mutated_symb_model, mutated_reachability_controller, [0.8, 4.5], (0.02, 0.01))
print(traj)

concrete_traj = [model.discretisator.getPartitionCenter(ksi_tield[1]) for ksi_tield in traj]
"""

w = (0.02, 0.01)

print(concrete_model.construct_trajectory(w, [0.8, 4.5]))

#TrajectoryPloter(concrete_model.trajectories[w])


#colors = ['red', 'blue']

#TrajectoryPloter(concrete_traj)[Conc_traj, traj]
t = [
    [[0.4, 8.2], [0.5, 9], [1.232, 7]],
    [[3.2, 6.8], [3.9, 7.0], [2.8, 6.9], [2.5, 5], [2, 4]],
    [[1.2, 3.4], [1.9, 4], [3, 9], [2, 7], [4.4, 8.2]]
]

#colors = ['red', 'blue', 'yellow']
"""Regions = {
            ((4, 8.5), (5, 9.5)): ['green', 'lightgreen'],
            ((8.5, 2), (9.5, 3)): ['blue', 'lightblue'],
            ((2, 0.5), (3, 1.5)): ['gold', 'yellow'],
            ((3, 3), (7, 7)): ['orangered', 'lightsalmon'],
        }"""
#plot_trajectory(t, colors, Regions)

#plot_trajectory([Conc_traj, concrete_traj], colors, Regions)

#plot_trajectory([concrete_model.trajectories[w]], ['red'], Automaton.Regions)

visualize_trajectory(Automaton, concrete_model.trajectories[w])