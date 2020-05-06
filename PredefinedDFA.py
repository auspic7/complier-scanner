import string
from Automata import DFA, generate_dfa_out_of_list

positive = '123456789'
INT = DFA(string.digits + "-",
          [(0, '0', 1), (0, positive, 3), (0, '-', 2), (2, positive, 3), (3, string.digits, 3)], 0, [1, 3])
FLOAT = DFA(string.digits + '-.', [(0, '-', 1), (0, '0', 2), (0, positive, 3), (1, '0', 2), (1, positive, 3),
                                   (3, string.digits, 3), (3, '.', 4), (2, '.', 4), (4, string.digits, 5),
                                   (5, positive, 5), (5, '0', 6), (6, positive, 5), (6, '0', 6), (5, positive, 5)], 0,
            [5])
STRING = DFA(string.digits + string.ascii_letters + ' ' + '"',
             [(0, '"', 1), (1, string.digits + string.ascii_letters + ' ', 1), (1, '"', 2)], 0, [2])
ID = DFA(string.ascii_letters + string.digits + '_',
         [(0, string.ascii_letters + '_', 1), (1, string.ascii_letters + string.digits + '_', 1)], 0, [1])
WHITESPACE = DFA('\t\n ', [(0, '\t\n ', 1), (1, '\t\n ', 1)], 0, [1])

TYPE = generate_dfa_out_of_list(['int', 'char', 'float', 'bool'])
BOOLEAN = generate_dfa_out_of_list(['true', 'false'])
KEYWORD = generate_dfa_out_of_list(['if', 'else', 'while', 'for', 'return'])
ARITHMETIC = generate_dfa_out_of_list(['+', '-', '*', '/'])
BITWISE = generate_dfa_out_of_list(['<<', '>>', '&', '|'])
ASSIGNMENT = generate_dfa_out_of_list(['='])
COMPARISON = generate_dfa_out_of_list(['<', '>', '==', '!=', '<=', '>='])
SEMICOLON = generate_dfa_out_of_list([';'])
BRACE = generate_dfa_out_of_list(['{', '}'])
PARENTHESES = generate_dfa_out_of_list(['(', ')'])
SEPARATOR = generate_dfa_out_of_list([','])

DFAs = [INT, FLOAT, STRING, WHITESPACE, TYPE, BOOLEAN, KEYWORD, ARITHMETIC, BITWISE, ASSIGNMENT, COMPARISON, SEMICOLON,
        BRACE, PARENTHESES, SEPARATOR, ID]
names = ['INT', 'FLOAT', 'STRING', 'WHITESPACE', 'TYPE', 'BOOLEAN', 'KEYWORD', 'ARITHMETIC', 'BITWISE', 'ASSIGNMENT',
         'COMPARISON', 'SEMICOLON', 'BRACE', 'PARENTHESES', 'SEPARATOR', 'ID']

for (dfa, name) in zip(DFAs, names):
    dfa.name = name

# Solution section for solving ambiguity problem
FLOAT_SOLUTION = DFA(string.digits + ".", [(0, '0', 2), (0, positive, 3),
                                     (3, string.digits, 3), (3, '.', 4), (2, '.', 4), (4, string.digits, 5),
                                     (5, positive, 5), (5, '0', 6), (6, positive, 5), (6, '0', 6), (5, positive, 5)], 0,
                     [5])
INT_SOLUTION = DFA(string.digits,
                   [(0, '0', 1), (0, positive, 3), (3, string.digits, 3)], 0, [1, 3])
DFAs_solution = [INT_SOLUTION, FLOAT_SOLUTION, STRING, WHITESPACE, TYPE, BOOLEAN, KEYWORD, ARITHMETIC, BITWISE, ASSIGNMENT, COMPARISON, SEMICOLON,
        BRACE, PARENTHESES, SEPARATOR, ID]

for (dfa, name) in zip(DFAs_solution, names):
    dfa.name = name
# Solution section for solving ambiguity problem end