import string

from Automata import DFA, generate_dfa_out_of_list

type_automata = DFA(string.ascii_lowercase,
                    [(0, 'i', 1), (1, 'n', 2), (2, 't', 13),
                     (0, 'c', 3), (3, 'h', 4), (4, 'a', 5), (5, 'r', 13),
                     (0, 'b', 6), (6, 'o', 7), (7, 'o', 8), (8, 'l', 13),
                     (0, 'f', 9), (9, 'l', 10), (10, 'o', 11), (11, 'a', 12), (12, 't', 13)],
                    0, [13])
INT = DFA(string.digits+"-",
          [(0, '0', 1), (0, '123456789', 3), (0, '-', 2), (2, '123456789', 3), (3, string.digits, 3)], 0, [1, 3])
STRING = generate_dfa_out_of_list([])
ID = generate_dfa_out_of_list([])
WHITESPACE = generate_dfa_out_of_list([])
FLOAT = generate_dfa_out_of_list([])


TYPE = generate_dfa_out_of_list(['int', 'char', 'float', 'bool'])
BOOLEAN = generate_dfa_out_of_list(['true', 'false'])
KEYWORD = generate_dfa_out_of_list(['if', 'else', 'while', 'for', 'return'])
ARITHMETIC = generate_dfa_out_of_list(['+', '-', '*', '/'])
BITWISE = generate_dfa_out_of_list(['<<', '>>', '&', '|'])
ASSIGNMENT = generate_dfa_out_of_list([';'])
COMPARISON = generate_dfa_out_of_list(['<', '>', '==', '!=', '<=', '>='])
SEMICOLON = generate_dfa_out_of_list([';'])
BRACE = generate_dfa_out_of_list(['{', '}'])
PARENTHESES = generate_dfa_out_of_list(['(', ')'])
SEPARATOR = generate_dfa_out_of_list([','])

print(KEYWORD.transition_functions)
print(KEYWORD.final_state)
KEYWORD.process('whilee')

INT.process('1010')
INT.setstate(0)
print()

INT.process('1111')
INT.setstate(0)
print()

INT.process('-0')
INT.setstate(0)
print()

INT.process('-12314')
INT.setstate(0)
print()

INT.process('01')
INT.setstate(0)
print()