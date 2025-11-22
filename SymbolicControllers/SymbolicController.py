import pickle

class SymbolicController:
    def save_controller(self, filename):
        try:
            with open(filename, "wb") as f:
                pickle.dump(self, f)
        except:
            raise

    @classmethod
    def load_model(self, filename):
        try:
            with open(filename, "rb") as f:
                model = pickle.load(f)
                return model
        except:
            raise