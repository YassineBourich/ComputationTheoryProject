import random

# Generate a random vector x that is inside the set of symbolic states S
def generate_random_x(S: set, model, state_divisions=100):
    random_state = random.choice(list(S))

    state_x_min, state_x_max = model.discretizator.getPartitionMinAndMax(random_state)

    x = []
    for i in range(model.continuous_model.get_dim_x()):
        r = random.randint(0, state_divisions)
        x.append(state_x_min[i] + ((state_x_max[i] - state_x_min[i]) * (r / state_divisions)))

    return x

# Generate a random perturbation vector out of a range of vect_min, vect_max
def generate_random_w(model):
    w_min = model.continuous_model.getW()[0]
    w_max = model.continuous_model.getW()[1]

    w = []

    for i in range(model.continuous_model.get_dim_w()):
        w.append(random.uniform(w_min[i], w_max[i]))

    return w