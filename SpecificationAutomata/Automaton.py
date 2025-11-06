class Automaton:
    def __init__(self, Q:set, SIGMA:set, delta, q0, F:set):
        self.Q = Q
        self.SIGMA = SIGMA
        self.delta = delta
        self.q0 = q0
        self.F = F

        self.current_state = q0

    # This is a DFA
    def next_state(self, symbol):
        return self.delta[(self.current_state, symbol)]

    def in_accept_state(self):
        return self.current_state in self.F