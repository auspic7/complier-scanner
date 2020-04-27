import enum


class Life(enum.Enum):
    ALIVE = 0
    DEAD = 1


class Automata:
    def __init__(self, alphabet, transition_functions, initial_state, final_states):
        self.life = Life.ALIVE
        self.alphabet = alphabet
        self.transition_functions = transition_functions
        self.state = initial_state
        self.final_state = final_states
        self.name = None


# unused
class NFA(Automata):
    def __init__(self, alphabet, transition_functions, initial_state, final_states):
        super().__init__(alphabet, transition_functions, initial_state, final_states)


# deterministic finite automaton
class DFA(Automata):
    def __init__(self, alphabet, transition_functions, initial_state, final_states):
        super().__init__(alphabet, transition_functions, initial_state, final_states)

    # gets string and does transition
    def process(self, input_alphabet):
        for char in input_alphabet:
            # input character not defined: halt
            if char not in self.alphabet:
                # print(f'{self.name}|{char}: undefined alphabet')
                self.life = Life.DEAD
                return self.life

            # automata already halted
            if self.life == Life.DEAD:
                # print(f'{self.name}|{char}: automata dead')
                return self.life

            # find transition function with state and input character
            for transition_function in self.transition_functions:
                if transition_function[0] == self.state and char in transition_function[1]:
                    # do state transition
                    self.state = transition_function[2]
                    # print(f'{self.name}|{transition_function[0]} ---{char}---> {"("+str(self.state)+")" if self.isfinal() else self.state}')
                    return self.life
            # transition function not found: halt
            else:
                # print(f'{self.name}|{char}: function undefined')
                self.life = Life.DEAD
                return self.life

    # function that returns if automata is not halted and in final state
    def isfinal(self):
        return self.state in self.final_state and self.life == Life.ALIVE

    # force set automata state and revive
    def setstate(self, state):
        self.state = state
        self.life = Life.ALIVE

# utility function generates dfa out of list of lexemes can be accepted
def generate_dfa_out_of_list(lexemes):
    # flatten list and generate alphabet
    alphabet = set(item for sublist in lexemes for item in sublist)
    # initialize dfa
    result = DFA(alphabet, list(), 0, list())

    state_index = 1
    for word in lexemes:
        # from starting state to first character state
        result.transition_functions.append((0, word[0], state_index))

        # from first character state to final character state
        for char in word[1:]:
            result.transition_functions.append((state_index, char, state_index + 1))
            state_index += 1
        # final character state would be the accepting state
        result.final_state.append(state_index)
        state_index += 1

    return result
