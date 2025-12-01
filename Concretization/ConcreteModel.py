from SymbolicControllers.AutomatonBasedController import AutomatonBasedController
from SymbolicControllers.ReachabilityController import ReachabilityController
from SymbolicControllers.SafetyController import SafetyController
from ProjectExceptions.Exceptions import ControllerTypeError

class ConcreteModel:
    def __init__(self, continuous_sys, symb_controller):
        self.continuous_sys = continuous_sys
        self.symb_controller = symb_controller
        self.q = self.symb_controller.symb_model.discretizator.q
        self.p = self.symb_controller.symb_model.discretizator.p

        self.trajectories = {}

    def construct_trajectory(self, w, x0, max_iter=100):
        if isinstance(self.symb_controller, AutomatonBasedController):
            return self.construct_trajectory_using_dynamic_controller(w, x0, max_iter)
        elif isinstance(self.symb_controller, ReachabilityController):
            return self.construct_trajectory_using_reachability_controller(w, x0, max_iter)
        elif isinstance(self.symb_controller, SafetyController):
            return self.construct_trajectory_using_safety_controller(w, x0, max_iter)
        else:
            raise ControllerTypeError("The controller used in concretization is not recognized.")

    def construct_trajectory_using_safety_controller(self, w, x0, max_iter):
        traj_id = (tuple(w), tuple(x0))         # defining the id of a specific trajectory with starting point x0 and a perturbation w
        self.trajectories[traj_id] = [x0]
        t = 0
        while t < max_iter:
            t += 1
            x_t = self.trajectories[traj_id][-1]
            si = self.symb_controller.h[self.q(x_t)]
            u_t = self.p(si)
            print("I am at : " + str(self.q(x_t)) + " - I choose : " + str(si))

            x_tp1 = self.continuous_sys.f(x_t, u_t, w)
            print("to go to: " + str(self.q(x_tp1)) + " from : " + str(
                self.symb_controller.symb_model.g[(self.q(x_t), si)]))
            print("=======================\n")
            self.trajectories[traj_id].append(x_tp1)

        return self.trajectories[traj_id]

    def construct_trajectory_using_reachability_controller(self, w, x0, max_iter):
        traj_id = (tuple(w), tuple(x0))         # defining the id of a specific trajectory with starting point x0 and a perturbation w
        self.trajectories[traj_id] = [x0]
        t = 0
        while (not self.symb_controller.isInReachableSet(self.trajectories[traj_id][-1])) and (t < max_iter):
            t += 1
            x_t = self.trajectories[traj_id][-1]
            si = self.symb_controller.h[self.q(x_t)]
            u_t = self.p(si)
            print("I am at : " + str(self.q(x_t)) + " - I choose : " + str(si))

            x_tp1 = self.continuous_sys.f(x_t, u_t, w)
            print("to go to: " + str(self.q(x_tp1)) + " from : " + str(
                self.symb_controller.symb_model.g[(self.q(x_t), si)]))
            print("=======================\n")
            self.trajectories[traj_id].append(x_tp1)

        return self.trajectories[traj_id]

    def construct_trajectory_using_dynamic_controller(self, w, x0, max_iter):
        traj_id = (tuple(w), tuple(x0))         # defining the id of a specific trajectory with starting point x0 and a perturbation w
        self.trajectories[traj_id] = [x0]  # Start with initial state
        t = 0

        psi_init = self.symb_controller.A.q0
        print(psi_init)
        psi_t = self.symb_controller.h1[(psi_init, self.q(x0))]
        x_t = x0

        print(self.symb_controller.initial_product_states())

        while (not self.symb_controller.isSpecificationAchieved(psi_t, x_t)) and (t < max_iter):
            t += 1

            # Stop if we leave the discretization grid to avoid invalid symbolic states
            if not self.symb_controller.symb_model.discretizator.KSI.in_grid(x_t):
                print("State left the discretization grid; stopping trajectory construction.")
                break

            psi_t = self.symb_controller.h1[(psi_t, self.q(x_t))]
            si = self.symb_controller.h2[(psi_t, self.q(x_t))]
            u_t = self.p(si)
            print("I am at : " + str((psi_t, self.q(x_t))) + "(transition: " + str(self.symb_controller.A.l(self.q(x_t))) + ")" + " - I choose : " + str(si))

            x_tp1 = self.continuous_sys.f(x_t, u_t, w)
            print("to go to: " + str(self.q(x_tp1)) + " from : " + str(
                self.symb_controller.symb_model.g[(self.q(x_t), si)]))
            print("=======================\n")

            # Append the new state
            self.trajectories[traj_id].append(x_tp1)
            x_t = x_tp1

        return self.trajectories[traj_id]