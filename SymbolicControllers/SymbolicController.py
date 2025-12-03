import pickle

class SymbolicController:
    def save_controller(self, filename):
        try:
            print("Saving symbolic controller...")
            with open(filename + ".ctl", "wb") as f:
                pickle.dump(self, f)
        except:
            raise

    @classmethod
    def load_controller(self, filename):
        try:
            print("Loading symbolic controller...")
            with open(filename + ".ctl", "rb") as f:
                model = pickle.load(f)
                return model
        except:
            raise