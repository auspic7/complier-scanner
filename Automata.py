import enum


class Life(enum.Enum):
    ALIVE = 0
    DEAD = 1




class Automata:
    def __init__(self,  alphabet, transition_functions, initial_state, final_states):
        self.life = Life.ALIVE
        self.alphabet = alphabet
        self.transition_functions = transition_functions
        self.state = initial_state
        self.final_state = final_states


class NFA(Automata):
    def __init__(self, alphabet, transition_functions, initial_state, final_states):
        super().__init__(alphabet, transition_functions, initial_state, final_states)


class DFA(Automata):
    def __init__(self, alphabet, transition_functions, initial_state, final_states):
        super().__init__(alphabet, transition_functions, initial_state, final_states)

    def process(self, input_alphabet):
        for char in input_alphabet:
            if char not in self.alphabet:
                print(f'{char}: undefined alphabet')
                self.life = Life.DEAD
                return

            if self.life == Life.DEAD:
                print(f'{char}: automata dead')
                return

            for transition_function in self.transition_functions:
                if transition_function[0] == self.state and char in transition_function[1]:
                    self.state = transition_function[2]
                    print(f'{transition_function[0]} ---{char}---> {isfinal(transition_function[2])}')
                    break
            else:
                print(f'{char}: function undefined')
                self.life = Life.DEAD
                return


    def isfinal(self):
        return self.state in self.final_state and self.life == Life.ALIVE

    def setstate(self, state):
        self.state = state
        self.life = Life.ALIVE



def generate_dfa_out_of_list(lexemes):
    alphabet = set(item for sublist in lexemes for item in sublist) # flatten list and generate alphabet
    result = DFA(alphabet, list(), 0, list())

    state_index = 1
    for word in lexemes:
        result.transition_functions.append((0, word[0], state_index))

        for char in word[1:]:
            result.transition_functions.append((state_index, char, state_index+1))
            state_index += 1
        result.final_state.append(state_index)
        state_index += 1

    return result
