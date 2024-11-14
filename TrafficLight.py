# How to make a DFA

class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def accepts(self, string):
        current_state = self.start_state
        for char in string:
            if char not in self.alphabet:
                return False
            current_state = self.transitions[current_state][char]
        return current_state in self.accept_states

if __name__ == "__main__":
    # Example DFA for strings ending in 'ab'
    states = {'q0', 'q1', 'q2'}
    alphabet = {'a', 'b'}
    transitions = {
        'q0': {'a': 'q0', 'b': 'q1'},
        'q1': {'a': 'q2', 'b': 'q1'},
        'q2': {'a': 'q0', 'b': 'q1'}
    }
    start_state = 'q0'
    accept_states = {'q2'}

    dfa = DFA(states, alphabet, transitions, start_state, accept_states)

    print(dfa.accepts("aba"))  # True
    print(dfa.accepts("abab"))  # True
    print(dfa.accepts("abb"))  # False
    print(dfa.accepts("a"))  # False