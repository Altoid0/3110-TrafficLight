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
        try:
            for char in string:
                if char not in self.alphabet:
                    raise ValueError(f"Invalid character '{char}' in input string.")
                current_state = self.transitions[current_state][char]
            return current_state in self.accept_states
        except KeyError as e:
            print(f"Transition error: {e}. This input string leads to an undefined state.")
            return False

if __name__ == "__main__":
    states = {'Red', 'Green', 'Yellow', 'Emergency_Active'}
    # t = timer
    # e = emergency_trigger
    # c = emergecny_clear
    # s = sensor
    alphabet = {'t', 'e', 'c', 's'}
    transitions = {
        'Red': {'t': 'Green', 'e': 'Emergency_Active'},
        'Green': {'t': 'Yellow', 'e': 'Emergency_Active'},
        'Yellow': {'t': 'Red', 'e': 'Emergency_Active'},
        'Emergency_Active': {'t': 'Emergency_Active', 'c': "Red", 's': 'Emergency_Active'}
    }
    start_state = 'Red'
    accept_states = {'Red', 'Green', 'Emergency_Active'}

    dfa = DFA(states, alphabet, transitions, start_state, accept_states)

    while True:
        user_input = input("Enter a string of inputs using ['t', 'e', 'c' and 's'] (or type 'exit' to quit): ").strip()
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            break
        try:
            if dfa.accepts(user_input):
                print(f"The DFA accepts the string '{user_input}'.")
            else:
                print(f"The DFA does not accept the string '{user_input}'.")
        except ValueError as e:
            print(e)
