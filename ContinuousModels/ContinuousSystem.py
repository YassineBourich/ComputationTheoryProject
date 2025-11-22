from ProjectExceptions.Exceptions import ContinuousSpaceError

class ContinuousSystem:
    def __init__(self, X, U, W):
        self.setX(X)
        self.setU(U)
        self.setW(W)

    # getters
    def getX(self):
        return self.X

    def getU(self):
        return self.U

    def getW(self):
        return self.W

    def get_dim_x(self):
        return self.dim_x

    def get_dim_u(self):
        return self.dim_u

    def get_dim_w(self):
        return self.dim_w

    # setters
    def setX(self, X):
        try:
            # check the number of elements in the space
            self.check_space_definition(X)
            # checking the dimension of the space
            self.check_space_dimension(X)
            # it these tests passed, assign X
            self.X = X
            self.dim_x = len(self.X[0])
        except:
            raise

    def setU(self, U):
        try:
            # check the number of elements in the space
            self.check_space_definition(U)
            # checking the dimension of the space
            self.check_space_dimension(U)
            # it these tests passed, assign U
            self.U = U
            self.dim_u = len(self.U[0])
        except:
            raise

    def setW(self, W):
        try:
            # check the number of elements in the space
            self.check_space_definition(W)
            # checking the dimension of the space
            self.check_space_dimension(W)
            # it these tests passed, assign W
            self.W = W
            self.dim_w = len(self.W[0])
        except:
            raise

    def check_space_definition(self, E):
        if len(E) != 2:
            raise ContinuousSpaceError("The compact must be defined as: (vect_min, vect_max).")

    def check_space_dimension(self, E):
        if len(E[0]) != len(E[1]):
            raise ContinuousSpaceError("The dimension of the space cannot be predicted from vect_min that has different dimension than vect_max.")