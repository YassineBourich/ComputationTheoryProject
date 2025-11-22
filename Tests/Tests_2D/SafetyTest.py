from SymbolicControllers.SafetyController import SafetyController
from Concretization.ConcreteModel import ConcreteModel
from Visualization.PlotingUtility import plot_trajectory
from ..RandomXGenerator import generate_random_x

class SafetyTest:
    def __init__(self, symb_model):
        self.symb_model = symb_model

        self.Qs1 = set()
        for i in range(20, 41):
            for j in range(20, 41):
                self.Qs1.add(i * 100 + j)  # vect_min = [2, 2], and vect_max = [4, 4]

        # Define Qs domain [0,2]x[0,2]
        self.Qs2 = set()
        for i in range(0, 21):
            for j in range(0, 21):
                self.Qs2.add(i * 100 + j)

        # Qs domain [4,6]x[4,6]
        self.Qs3 = self.symb_model.discretizator.KSI.getAllStates()
        for i in range(40, 61):
            for j in range(40, 61):
                self.Qs3.remove(i * 100 + j)
        self.Qs3.remove(0)

    def get_concrete_model(self, Qs, Qs_domain):
        print("\t\u2022Defining Safety domain...")

        print("\t\u2022Safety domain defined: " + Qs_domain + ".")

        print("\t\u2022Constructing Safety controller")
        safety_controller = SafetyController(self.symb_model, Qs)
        print("\t\u2022Safety controller constructed.")
        concrete_model = ConcreteModel(self.symb_model.continuous_model, safety_controller)
        print("\t\u2022Concrete model defined.")

        return concrete_model, safety_controller.R_list[-1]

    def run_single_test(self, test_name, domain, domain_name, w, concrete_model=None, R_star=None, color=None, regions=None):
        this_is_an_independant_test = concrete_model is None
        if this_is_an_independant_test:
            print("Running " + str(test_name))
            concrete_model, R_star = self.get_concrete_model(domain, domain_name)

        x = generate_random_x(R_star, self.symb_model)
        print("\t\u2022Calculating the trajectory...")
        concrete_model.construct_trajectory(w, x)

        if this_is_an_independant_test:
            plot_trajectory(concrete_model.trajectories.values(), [color], regions)

    def run_tests(self):
        self.test_set1()
        self.test_set2()
        self.test_set3()

#__________________________________________Test Set1_____________________________________________

    def test_set1(self):
        print("Running test1...")
        concrete_model, R_star = self.get_concrete_model(self.Qs1, "[2, 4]x[2, 4]")

        regions = {((2, 2), (4, 4)): ['green', 'lightgreen']}
        traj_colors = ['red', 'red', 'red', 'blue', 'blue', 'blue', 'orange', 'orange', 'orange', 'purple','purple', 'purple']

        print("\n_______________Calculating trajectories (Test Set 1)_______________")
        self.test_1_1(concrete_model, R_star)
        self.test_1_1(concrete_model, R_star)
        self.test_1_1(concrete_model, R_star)
        self.test_1_1(concrete_model, R_star)
        self.test_1_2(concrete_model, R_star)
        self.test_1_2(concrete_model, R_star)
        self.test_1_2(concrete_model, R_star)
        self.test_1_2(concrete_model, R_star)
        self.test_1_3(concrete_model, R_star)
        self.test_1_3(concrete_model, R_star)
        self.test_1_3(concrete_model, R_star)
        self.test_1_3(concrete_model, R_star)

        plot_trajectory(concrete_model.trajectories.values(), traj_colors, regions)

    def test_1_1(self, concrete_model=None, R_star=None, regions=None, traj_color='red'):
        if regions is None: regions = {((2, 2), (4, 4)): ['green', 'lightgreen']}

        self.run_single_test("Test 1_1", self.Qs1,
                             "[2, 4]x[2, 4]", [0.0, 0.0],
                             concrete_model, R_star, traj_color, regions)

    def test_1_2(self, concrete_model=None, R_star=None, regions=None, traj_color='red'):
        if regions is None: regions = {((2, 2), (4, 4)): ['green', 'lightgreen']}

        self.run_single_test("Test 1_2", self.Qs1,
                             "[2, 4]x[2, 4]", [0.017, -0.035],
                             concrete_model, R_star, traj_color, regions)

    def test_1_3(self, concrete_model=None, R_star=None, regions=None, traj_color='red'):
        if regions is None: regions = {((2, 2), (4, 4)): ['green', 'lightgreen']}

        self.run_single_test("Test 1_3", self.Qs1,
                             "[2, 4]x[2, 4]", [-0.02, -0.04],
                             concrete_model, R_star, traj_color, regions)

# __________________________________________Test Set2_____________________________________________

    def test_set2(self):
        print("Running test2...")
        concrete_model, R_star = self.get_concrete_model(self.Qs2, "[0, 2]x[0, 2]")

        regions = {((0, 0), (2, 2)): ['green', 'lightgreen']}
        traj_colors = ['red', 'blue', 'orange', 'purple', 'black', 'pink']

        print("\n_______________Calculating trajectories (Test Set 2)_______________")

        self.test_2_1(concrete_model, R_star)
        self.test_2_1(concrete_model, R_star)
        self.test_2_3(concrete_model, R_star)
        self.test_2_1(concrete_model, R_star)
        self.test_2_1(concrete_model, R_star)
        self.test_2_3(concrete_model, R_star)

        plot_trajectory(
            concrete_model.trajectories.values(),
            traj_colors,
            regions
        )

    def test_2_1(self, concrete_model=None, R_star=None, regions=None, traj_color='red'):
        if regions is None: regions = {((0, 0), (2, 2)): ['green', 'lightgreen']}

        self.run_single_test("Test 2_1", self.Qs2,
                             "[0, 2]x[0, 2]", [0.0, 0.0],
                             concrete_model, R_star, traj_color, regions)

    def test_2_2(self, concrete_model=None, R_star=None, regions=None, traj_color='red'):
        if regions is None: regions = {((0, 0), (2, 2)): ['green', 'lightgreen']}

        self.run_single_test("Test 2_2", self.Qs2,
                             "[0, 2]x[0, 2]", [0.015, 0.02],
                             concrete_model, R_star, traj_color, regions)

    def test_2_3(self, concrete_model=None, R_star=None, regions=None, traj_color='red'):
        if regions is None: regions = {((0, 0), (2, 2)): ['green', 'lightgreen']}

        self.run_single_test("Test 2_3", self.Qs2,
                             "[0, 2]x[0, 2]", [-0.025, -0.01],
                             concrete_model, R_star, traj_color, regions)

# __________________________________________Test Set3_____________________________________________

    def test_set3(self):
        print("Running test3...")

        concrete_model, R_star = self.get_concrete_model(self.Qs3, "[4, 6]x[4, 6]")

        print("\n_______________Calculating trajectories (Test Set 3)_______________")

        self.test_3_1(concrete_model, R_star)
        self.test_3_2(concrete_model, R_star)
        self.test_3_1(concrete_model, R_star)
        self.test_3_2(concrete_model, R_star)
        self.test_3_3(concrete_model, R_star)

        plot_trajectory(
            concrete_model.trajectories.values(),
            ['cyan', 'magenta', 'red', 'brown', 'gray'],
            {((4, 4), (6, 6)): ['green', 'lightgreen']}
        )

    def test_3_1(self, concrete_model=None, R_star=None, regions=None, traj_color='red'):
        if regions is None: regions = {((4, 4), (6, 6)): ['green', 'lightgreen']}

        self.run_single_test("Test 3_1", self.Qs3,
                             "[4, 6]x[4, 6]", [0.0, 0.0],
                             concrete_model, R_star, traj_color, regions)

    def test_3_2(self, concrete_model=None, R_star=None, regions=None, traj_color='red'):
        if regions is None: regions = {((4, 4), (6, 6)): ['green', 'lightgreen']}

        self.run_single_test("Test 3_1", self.Qs3,
                             "[4, 6]x[4, 6]", [0.02, -0.015],
                             concrete_model, R_star, traj_color, regions)

    def test_3_3(self, concrete_model=None, R_star=None, regions=None, traj_color='red'):
        if regions is None: regions = {((4, 4), (6, 6)): ['green', 'lightgreen']}

        self.run_single_test("Test 3_1", self.Qs3,
                             "[4, 6]x[4, 6]", [-0.03, 0.01],
                             concrete_model, R_star, traj_color, regions)

