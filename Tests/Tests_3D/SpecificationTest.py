from SymbolicControllers.AutomatonBasedController import AutomatonBasedController
from SpecificationAutomata.ExampleSpecification_3D import ExampleSpecification3D
from Concretization.ConcreteModel import ConcreteModel
from Visualization.PlotingUtility import plot_trajectory
from ..RandomXGenerator import generate_random_x, generate_random_w

class SpecificationTest:
    def __init__(self, symb_model):
        self.symb_model = symb_model

        self.specification_automaton = ExampleSpecification3D(self.symb_model)

    def get_concrete_model(self, specification_automaton):
        print("\t\u2022Defining Safety domain...")

        print("\t\u2022Specification automaton defined.")

        automaton_controller = AutomatonBasedController(specification_automaton, self.symb_model)
        concrete_model = ConcreteModel(self.symb_model.continuous_model, automaton_controller)
        print("\t\u2022Concrete model defined.")

        return concrete_model, automaton_controller.Q0

    def run_single_test(self, test_name, w, specification_automaton=None, concrete_model=None, Q0=None, color=None,
                        regions=None):
        this_is_an_independant_test = concrete_model is None
        if this_is_an_independant_test:
            print("Running " + str(test_name))
            concrete_model, Q0 = self.get_concrete_model(specification_automaton)

        x = generate_random_x(Q0, self.symb_model)
        print("\t\u2022Calculating the trajectory...")
        concrete_model.construct_trajectory(w, x)

        if this_is_an_independant_test:
            plot_trajectory(concrete_model.trajectories.values(), [color], regions)

    def run_tests(self):
        self.test_set1()
        self.test_n_perturbation()

    # __________________________________________Test Set1_____________________________________________

    def test_set1(self):
        print("Running test1...")
        concrete_model, Q0 = self.get_concrete_model(self.specification_automaton)

        regions = self.specification_automaton.Regions
        traj_colors = ['red', 'red', 'red', 'blue', 'blue', 'blue', 'orange', 'orange', 'orange', 'purple', 'purple',
                       'purple']

        print("\n_______________Calculating trajectories (Test Set 1)_______________")
        self.test_1_1(concrete_model, Q0)
        self.test_1_1(concrete_model, Q0)
        self.test_1_1(concrete_model, Q0)
        self.test_1_1(concrete_model, Q0)
        self.test_1_2(concrete_model, Q0)
        self.test_1_2(concrete_model, Q0)
        self.test_1_2(concrete_model, Q0)
        self.test_1_2(concrete_model, Q0)
        self.test_1_3(concrete_model, Q0)
        self.test_1_3(concrete_model, Q0)
        self.test_1_3(concrete_model, Q0)
        self.test_1_3(concrete_model, Q0)

        plot_trajectory(concrete_model.trajectories.values(), traj_colors, regions)

    def test_1_1(self, concrete_model=None, Q0=None, regions=None, traj_color='red'):
        if regions is None: regions = self.specification_automaton.Regions

        self.run_single_test("Test 1_1", [0.0, 0.0, 0.0] , self.specification_automaton,
                             concrete_model, Q0, traj_color, regions)

    def test_1_2(self, concrete_model=None, Q0=None, regions=None, traj_color='red'):
        if regions is None: regions = self.specification_automaton.Regions

        self.run_single_test("Test 1_2", [0.017, -0.035, 0.02], self.specification_automaton,
                             concrete_model, Q0, traj_color, regions)

    def test_1_3(self, concrete_model=None, Q0=None, regions=None, traj_color='red'):
        if regions is None: regions = self.specification_automaton.Regions

        self.run_single_test("Test 1_3", [-0.02, 0.0, -0.04], self.specification_automaton,
                             concrete_model, Q0, traj_color, regions)

    # __________________________________________n perturbation sample Test_____________________________________________
    def test_n_perturbation(self, n):
        print(f"Running {n} perturbation sample test...")

        concrete_model, Q0 = self.get_concrete_model(self.specification_automaton)
        regions = self.specification_automaton.Regions
        traj_colors = ['red']

        x = generate_random_x(Q0, self.symb_model)

        for i in range(n):
            w = generate_random_w(self.symb_model)
            print("\t\u2022Calculating the trajectory...")
            concrete_model.construct_trajectory(w, x)

        plot_trajectory(concrete_model.trajectories.values(), traj_colors, regions)