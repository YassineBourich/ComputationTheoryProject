from Exceptions.Exceptions import DimensionError

# function to calculate the product
def PI(L):
    p = 1

    for i in range(len(L)):
        p *= L[i]

    return p

# Abandoned
def PI_2(L1, L2):
    p = 1

    for i in range(len(L1)):
        p *= L2[i] - L1[i]

    return p

# Linear algebra functions
def vec_add(u, v):
    if len(u) != len(v):
        raise DimensionError("Cannot add two vectors of different dimensions")

    return [u[i] + v[i] for i in range(len(u))]

def vec_sub(u, v):
    if len(u) != len(v):
        raise DimensionError("Cannot subtract two vectors of different dimensions")

    return [u[i] - v[i] for i in range(len(u))]

def vec_mul_scalar(u, s):
    return [u[i] * s for i in range(len(u))]

def mat_vec_mul(M, v):
    if len(M[0]) != len(v):
        raise DimensionError("Cannot multiply a vector with a matrix of different dimensions")

    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]

def vec_abs(v):
    return [abs(v[i]) for i in range(len(v))]

# Vectorial comparison function: check if v1 is less than or equals to v2 in all terms
def vect_all_lte(v1, v2):
    if len(v1) != len(v2):
        raise DimensionError("Cannot compare two vectors of different dimensions")

    for i in range(len(v1)):
        if v1[i] > v2[i]:
            return False

    return True