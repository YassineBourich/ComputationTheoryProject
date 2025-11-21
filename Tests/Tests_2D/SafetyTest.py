from SymbolicControllers.SafetyController import SafetyController
from Concretization.ConcreteModel import ConcreteModel
from Visualization.PlotingUtility import plot_trajectory

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

        return concrete_model

    def run_tests(self):
        self.test_set1()
        self.test_set2()
        self.test_set3()
        self.test_set4()

#__________________________________________Test Set1_____________________________________________

    def test_set1(self):
        print("Running test1...")
        concrete_model = self.get_concrete_model(self.Qs1, "[2, 4]x[2, 4]")

        print("\n_______________Calculating trajectories_______________")
        self.test_1_1(concrete_model)
        self.test_1_2(concrete_model)
        self.test_1_3(concrete_model)
        self.test_1_4(concrete_model)
        self.test_1_5(concrete_model)
        self.test_1_6(concrete_model)
        self.test_1_7(concrete_model)
        self.test_1_8(concrete_model)
        self.test_1_9(concrete_model)
        self.test_1_10(concrete_model)
        self.test_1_11(concrete_model)
        self.test_1_12(concrete_model)

        plot_trajectory(concrete_model.trajectories.values(),
                        ['red', 'red', 'red', 'red', 'blue', 'blue', 'blue', 'blue', 'orange', 'orange', 'orange', 'orange', 'purple', 'purple','purple', 'purple'],
                        {((2, 2), (4, 4)): ['green', 'lightgreen']}
        )

    def test_1_1(self, concrete_model=None):
        this_is_an_independant_test = False
        if concrete_model == None:
            this_is_an_independant_test = True

            print("Running Test 1_1")
            concrete_model = self.get_concrete_model(self.Qs1, "[2, 4]x[2, 4]")

        w1 = [0.0, 0.0]
        x1 = [2, 2]
        print("\t\u2022Calculating the trajectory (w1, x1)...")
        concrete_model.construct_trajectory(w1, x1)

        if this_is_an_independant_test:
            plot_trajectory(concrete_model.trajectories.values(), ['red'], {((2, 2), (4, 4)): ['green', 'lightgreen']})

    def test_1_2(self, concrete_model=None):
        this_is_an_independant_test = False
        if concrete_model == None:
            this_is_an_independant_test = True

            print("Running Test 1_2")
            concrete_model = self.get_concrete_model(self.Qs1, "[2, 4]x[2, 4]")

        w1 = [0.0, 0.0]
        x2 = [2.7, 3.9]
        print("\t\u2022Calculating the trajectory (w1, x2)...")
        concrete_model.construct_trajectory(w1, x2)

        if this_is_an_independant_test:
            plot_trajectory(concrete_model.trajectories.values(), ['red'], {((2, 2), (4, 4)): ['green', 'lightgreen']})

    def test_1_3(self, concrete_model=None):
        this_is_an_independant_test = False
        if concrete_model == None:
            this_is_an_independant_test = True

            print("Running Test 1_3")
            concrete_model = self.get_concrete_model(self.Qs1, "[2, 4]x[2, 4]")

        w1 = [0.0, 0.0]
        x3 = [5, 5]
        print("\t\u2022Calculating the trajectory (w1, x3)...")
        concrete_model.construct_trajectory(w1, x3)

        if this_is_an_independant_test:
            plot_trajectory(concrete_model.trajectories.values(), ['red'], {((2, 2), (4, 4)): ['green', 'lightgreen']})

    def test_1_4(self, concrete_model=None):
        this_is_an_independant_test = False
        if concrete_model == None:
            this_is_an_independant_test = True

            print("Running Test 1_4")
            concrete_model = self.get_concrete_model(self.Qs1, "[2, 4]x[2, 4]")

        w1 = [0.0, 0.0]
        x4 = [1, 0.62]
        print("\t\u2022Calculating the trajectory (w1, x4)...")
        concrete_model.construct_trajectory(w1, x4)

        if this_is_an_independant_test:
            plot_trajectory(concrete_model.trajectories.values(), ['red'], {((2, 2), (4, 4)): ['green', 'lightgreen']})

    def test_1_5(self, concrete_model=None):
        this_is_an_independant_test = False
        if concrete_model == None:
            this_is_an_independant_test = True

            print("Running Test 1_5")
            concrete_model = self.get_concrete_model(self.Qs1, "[2, 4]x[2, 4]")

        w2 = [0.017, -0.035]
        x1 = [2, 2]
        print("\t\u2022Calculating the trajectory (w2, x1)...")
        concrete_model.construct_trajectory(w2, x1)

        if this_is_an_independant_test:
            plot_trajectory(concrete_model.trajectories.values(), ['red'], {((2, 2), (4, 4)): ['green', 'lightgreen']})

    def test_1_6(self, concrete_model=None):
        this_is_an_independant_test = False
        if concrete_model == None:
            this_is_an_independant_test = True

            print("Running Test 1_6")
            concrete_model = self.get_concrete_model(self.Qs1, "[2, 4]x[2, 4]")

        w2 = [0.017, -0.035]
        x2 = [2.7, 3.9]
        print("\t\u2022Calculating the trajectory (w2, x2)...")
        concrete_model.construct_trajectory(w2, x2, 10)

        if this_is_an_independant_test:
            plot_trajectory(concrete_model.trajectories.values(), ['red'], {((2, 2), (4, 4)): ['green', 'lightgreen']})

    def test_1_7(self, concrete_model=None):
        this_is_an_independant_test = False
        if concrete_model == None:
            this_is_an_independant_test = True

            print("Running Test 1_7")
            concrete_model = self.get_concrete_model(self.Qs1, "[2, 4]x[2, 4]")

        w2 = [0.017, -0.035]
        x3 = [5, 5]
        print("\t\u2022Calculating the trajectory (w2, x3)...")
        concrete_model.construct_trajectory(w2, x3)

        if this_is_an_independant_test:
            plot_trajectory(concrete_model.trajectories.values(), ['red'], {((2, 2), (4, 4)): ['green', 'lightgreen']})

    def test_1_8(self, concrete_model=None):
        this_is_an_independant_test = False
        if concrete_model == None:
            this_is_an_independant_test = True

            print("Running Test 1_8")
            concrete_model = self.get_concrete_model(self.Qs1, "[2, 4]x[2, 4]")

        w2 = [0.017, -0.035]
        x4 = [1, 0.62]
        print("\t\u2022Calculating the trajectory (w2, x4)...")
        concrete_model.construct_trajectory(w2, x4)

        if this_is_an_independant_test:
            plot_trajectory(concrete_model.trajectories.values(), ['red'], {((2, 2), (4, 4)): ['green', 'lightgreen']})

    def test_1_9(self, concrete_model=None):
        this_is_an_independant_test = False
        if concrete_model == None:
            this_is_an_independant_test = True

            print("Running Test 1_9")
            concrete_model = self.get_concrete_model(self.Qs1, "[2, 4]x[2, 4]")

        w3 = [-0.02, -0.04]
        x1 = [2, 2]
        print("\t\u2022Calculating the trajectory (w3, x1)...")
        concrete_model.construct_trajectory(w3, x1)

        if this_is_an_independant_test:
            plot_trajectory(concrete_model.trajectories.values(), ['red'], {((2, 2), (4, 4)): ['green', 'lightgreen']})

    def test_1_10(self, concrete_model=None):
        this_is_an_independant_test = False
        if concrete_model == None:
            this_is_an_independant_test = True

            print("Running Test 1_10")
            concrete_model = self.get_concrete_model(self.Qs1, "[2, 4]x[2, 4]")

        w3 = [-0.02, -0.04]
        x2 = [2.7, 3.9]
        print("\t\u2022Calculating the trajectory (w3, x2)...")
        concrete_model.construct_trajectory(w3, x2)

        if this_is_an_independant_test:
            plot_trajectory(concrete_model.trajectories.values(), ['red'], {((2, 2), (4, 4)): ['green', 'lightgreen']})

    def test_1_11(self, concrete_model=None):
        this_is_an_independant_test = False
        if concrete_model == None:
            this_is_an_independant_test = True

            print("Running Test 1_11")
            concrete_model = self.get_concrete_model(self.Qs1, "[2, 4]x[2, 4]")

        w3 = [-0.02, -0.04]
        x3 = [5, 5]
        print("\t\u2022Calculating the trajectory (w3, x3)...")
        concrete_model.construct_trajectory(w3, x3)

        if this_is_an_independant_test:
            plot_trajectory(concrete_model.trajectories.values(), ['red'], {((2, 2), (4, 4)): ['green', 'lightgreen']})

    def test_1_12(self, concrete_model=None):
        this_is_an_independant_test = False
        if concrete_model == None:
            this_is_an_independant_test = True

            print("Running Test 1_12")
            concrete_model = self.get_concrete_model(self.Qs1, "[2, 4]x[2, 4]")

        w3 = [-0.02, -0.04]
        x4 = [1, 0.62]
        print("\t\u2022Calculating the trajectory (w3, x4)...")
        concrete_model.construct_trajectory(w3, x4)

        if this_is_an_independant_test:
            plot_trajectory(concrete_model.trajectories.values(), ['red'],{((2, 2), (4, 4)): ['green', 'lightgreen']})

# __________________________________________Test Set2_____________________________________________

    def test_set2(self):
        print("Running test2...")
        concrete_model = self.get_concrete_model(self.Qs2, "[0, 2]x[0, 2]")

        print("\n_______________Calculating trajectories (Set 2)_______________")

        self.test_2_1(concrete_model)
        self.test_2_2(concrete_model)
        self.test_2_3(concrete_model)
        self.test_2_4(concrete_model)
        self.test_2_5(concrete_model)
        self.test_2_6(concrete_model)

        plot_trajectory(
            concrete_model.trajectories.values(),
            ['red', 'blue', 'orange', 'purple', 'black', 'pink'],
            {((0, 0), (2, 2)): ['green', 'lightgreen']}
        )

    def test_2_1(self, concrete_model=None):
        this_is_independent_test = concrete_model is None
        if this_is_independent_test:
            print("Running Test 2_1")
            concrete_model = self.get_concrete_model(self.Qs2, "[0, 2]x[0, 2]")

        w = [0.0, 0.0]
        x = [0.2, 0.2]
        print("\t• Calculating trajectory (w0, xA)...")
        concrete_model.construct_trajectory(w, x)

        if this_is_independent_test:
            plot_trajectory(concrete_model.trajectories.values(), ['red'],
                            {((0, 0), (2, 2)): ['green', 'lightgreen']})

    def test_2_2(self, concrete_model=None):
        this_is_independent_test = concrete_model is None
        if this_is_independent_test:
            print("Running Test 2_2")
            concrete_model = self.get_concrete_model(self.Qs2, "[0, 2]x[0, 2]")

        w = [0.0, 0.0]
        x = [1.5, 1.8]
        print("\t• Calculating trajectory (w0, xB)...")
        concrete_model.construct_trajectory(w, x)

        if this_is_independent_test:
            plot_trajectory(concrete_model.trajectories.values(), ['blue'],
                            {((0, 0), (2, 2)): ['green', 'lightgreen']})

    def test_2_3(self, concrete_model=None):
        this_is_independent_test = concrete_model is None
        if this_is_independent_test:
            print("Running Test 2_3")
            concrete_model = self.get_concrete_model(self.Qs2, "[0, 2]x[0, 2]")

        w = [0.015, 0.02]
        x = [0.2, 0.2]
        print("\t• Calculating trajectory (w_pos, xA)...")
        concrete_model.construct_trajectory(w, x)

        if this_is_independent_test:
            plot_trajectory(concrete_model.trajectories.values(), ['orange'],
                            {((0, 0), (2, 2)): ['green', 'lightgreen']})

    def test_2_4(self, concrete_model=None):
        this_is_independent_test = concrete_model is None
        if this_is_independent_test:
            print("Running Test 2_4")
            concrete_model = self.get_concrete_model(self.Qs2, "[0, 2]x[0, 2]")

        w = [0.015, 0.02]
        x = [1.5, 1.8]
        print("\t• Calculating trajectory (w_pos, xB)...")
        concrete_model.construct_trajectory(w, x)

        if this_is_independent_test:
            plot_trajectory(concrete_model.trajectories.values(), ['purple'],
                            {((0, 0), (2, 2)): ['green', 'lightgreen']})

    def test_2_5(self, concrete_model=None):
        this_is_independent_test = concrete_model is None
        if this_is_independent_test:
            print("Running Test 2_5")
            concrete_model = self.get_concrete_model(self.Qs2, "[0, 2]x[0, 2]")

        w = [-0.025, -0.01]
        x = [2.5, 2.5]  # outside domain
        print("\t• Calculating trajectory (w_neg, xC)...")
        concrete_model.construct_trajectory(w, x)

        if this_is_independent_test:
            plot_trajectory(concrete_model.trajectories.values(), ['black'],
                            {((0, 0), (2, 2)): ['green', 'lightgreen']})

    def test_2_6(self, concrete_model=None):
        this_is_independent_test = concrete_model is None
        if this_is_independent_test:
            print("Running Test 2_6")
            concrete_model = self.get_concrete_model(self.Qs2, "[0, 2]x[0, 2]")

        w = [-0.025, -0.01]
        x = [-0.5, 0.3]  # outside domain
        print("\t• Calculating trajectory (w_neg, xD)...")
        concrete_model.construct_trajectory(w, x)

        if this_is_independent_test:
            plot_trajectory(concrete_model.trajectories.values(), ['pink'],
                            {((0, 0), (2, 2)): ['green', 'lightgreen']})

# __________________________________________Test Set3_____________________________________________

    def test_set3(self):
        print("Running test3...")

        concrete_model = self.get_concrete_model(self.Qs3, "[4, 6]x[4, 6]")

        print("\n_______________Calculating trajectories (Set 3)_______________")

        self.test_3_1(concrete_model)
        self.test_3_2(concrete_model)
        self.test_3_3(concrete_model)
        self.test_3_4(concrete_model)
        self.test_3_5(concrete_model)

        plot_trajectory(
            concrete_model.trajectories.values(),
            ['cyan', 'magenta', 'red', 'brown', 'gray'],
            {((4, 4), (6, 6)): ['green', 'lightgreen']}
        )

    def test_3_1(self, concrete_model=None):
        this_is_independent_test = concrete_model is None
        if this_is_independent_test:
            print("Running Test 3_1")
            concrete_model = self.get_concrete_model(self.Qs3, "[4, 6]x[4, 6]")

        w = [0.0, 0.0]
        x = [4.2, 4.1]
        print("\t• Calculating trajectory (w1, xA)...")
        concrete_model.construct_trajectory(w, x)

        if this_is_independent_test:
            plot_trajectory(concrete_model.trajectories.values(), ['cyan'],
                            {((4, 4), (6, 6)): ['green', 'lightgreen']})

    def test_3_2(self, concrete_model=None):
        this_is_independent_test = concrete_model is None
        if this_is_independent_test:
            print("Running Test 3_2")
            concrete_model = self.get_concrete_model(self.Qs3, "[4, 6]x[4, 6]")

        w = [0.0, 0.0]
        x = [6.5, 6.8]
        print("\t• Calculating trajectory (w1, xB)...")
        concrete_model.construct_trajectory(w, x)

        if this_is_independent_test:
            plot_trajectory(concrete_model.trajectories.values(), ['magenta'],
                            {((4, 4), (6, 6)): ['green', 'lightgreen']})

    def test_3_3(self, concrete_model=None):
        this_is_independent_test = concrete_model is None
        if this_is_independent_test:
            print("Running Test 3_3")
            concrete_model = self.get_concrete_model(self.Qs3, "[4, 6]x[4, 6]")

        w = [0.02, -0.015]
        x = [5.3, 6.2]
        print("\t• Calculating trajectory (w2, xA)...")
        concrete_model.construct_trajectory(w, x)

        if this_is_independent_test:
            plot_trajectory(concrete_model.trajectories.values(), ['red'],
                            {((4, 4), (6, 6)): ['green', 'lightgreen']})

    def test_3_4(self, concrete_model=None):
        this_is_independent_test = concrete_model is None
        if this_is_independent_test:
            print("Running Test 3_4")
            concrete_model = self.get_concrete_model(self.Qs3, "[4, 6]x[4, 6]")

        w = [0.02, -0.015]
        x = [7.0, 4.2]  # outside
        print("\t• Calculating trajectory (w2, xC)...")
        concrete_model.construct_trajectory(w, x)

        if this_is_independent_test:
            plot_trajectory(concrete_model.trajectories.values(), ['brown'],
                            {((4, 4), (6, 6)): ['green', 'lightgreen']})

    def test_3_5(self, concrete_model=None):
        this_is_independent_test = concrete_model is None
        if this_is_independent_test:
            print("Running Test 3_5")
            concrete_model = self.get_concrete_model(self.Qs3, "[4, 6]x[4, 6]")

        w = [-0.03, 0.01]
        x = [3.5, 3.5]  # outside
        print("\t• Calculating trajectory (w3, xD)...")
        concrete_model.construct_trajectory(w, x)

        if this_is_independent_test:
            plot_trajectory(concrete_model.trajectories.values(), ['gray'],
                            {((4, 4), (6, 6)): ['green', 'lightgreen']})