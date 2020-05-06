import argparse
import os
from Automata import Life
from PredefinedDFA import DFAs, DFAs_solution
from tabulate import tabulate

parser = argparse.ArgumentParser()
parser.add_argument('input_file_name', help='Desired file name to analyze', type=str)
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument('-l', '--list', help='list shaped output for module use', action="store_true")
parser.add_argument('-s', '--solution', help='use solution dfa list to resolve ambiguity problem', action="store_true")
args = parser.parse_args()


def print_and_write(file, string):
    print(string)
    file.write(string+"\n")


# function for printing error message
def print_error(file, text, i):
    line_no = text[:i].count('\n') + 1
    line_starting = text[:i].rfind('\n')
    print_and_write(file_out, f'error occurred on line {line_no}')
    print_and_write(file_out, f'{text.splitlines()[line_no-1]}')
    print_and_write(file_out, ' ' * (i - line_starting - 1) + '^')
    print_and_write(file_out, 'unexpected character')
    return


# lexical analyze string using dfa_list
def lexically_analyze(string_to_scan, dfa_list):
    # lexemes list scanned so far
    lexemes = []
    # starting index of token
    lexeme_start = 0
    # index used to traverse string
    i = 0
    # candidate dfa, which becomes a dfa used to scan string when every dfa halted
    determined_dfa = lexeme_end = None

    # traverse file from beginning to end
    while i < len(string_to_scan):
        # list of dfa not halted
        alive_dfa = [item for item in dfa_list if item.process(string_to_scan[i]) == Life.ALIVE]
        # list of dfa in final state
        final_dfa = [item for item in dfa_list if item.isfinal()]

        # if there exists a dfa not halted and in final state
        if final_dfa:
            # that dfa will be candidate dfa to scan token
            (determined_dfa, lexeme_end) = (final_dfa[0], i)
        # (else) do nothing because there is some possibility becoming final state when a dfa get new input

        # when every dfa helts
        if not alive_dfa:
            # if there is no candidate dfa(a dfa which makes longest token starting from lexeme_start)
            # which means string from lexeme_start cannot be parsed with dfa provided
            if not determined_dfa:
                # print error message
                print_error(file, string_to_scan, i)
                return
            # every dfa halted, and some lexeme was able to parsed. so parse it and add to list
            if not determined_dfa.name == "WHITESPACE":
                lexemes.append((string_to_scan[lexeme_start:lexeme_end + 1], determined_dfa.name, determined_dfa.state))
            # starting point of next token will be ending point of last token + 1
            i = lexeme_start = lexeme_end + 1
            # initialization, revive every dfa and remove candidate dfa since we read nothing
            determined_dfa = lexeme_end = None
            for dfa in dfa_list:
                dfa.setstate(0)
            continue
        # verbose output
        if args.verbose:
            print_and_write(file_out, f'alive_dfa({string_to_scan[i]}): {[item.name for item in alive_dfa]}')
            print_and_write(file_out, f'final_dfa({string_to_scan[i]}): {[item.name for item in final_dfa]}')
            print_and_write(file_out, f'lexemes({string_to_scan[i]}): {lexemes}')
        # read next character
        i += 1

    # could not parse last lexeme
    if not determined_dfa:
        # print error
        print_error(file, string_to_scan, i)
        return
    # add last lexeme to the list
    if not determined_dfa.name == "WHITESPACE":
        lexemes.append((string_to_scan[lexeme_start:lexeme_end + 1], determined_dfa.name, determined_dfa.state))
    return lexemes


# file input
file = open(args.input_file_name)
file_out = open(os.path.splitext(args.input_file_name)[0]+".out", "w")
file_txt = file.read()
if args.verbose:
    print_and_write(file_out, file_txt)

# lexical analyze
if not args.solution:
    tokens = lexically_analyze(file_txt, DFAs)
else:
    tokens = lexically_analyze(file_txt, DFAs_solution)

# have no error
if tokens:
    if args.list:
        print_and_write(file_out, tokens)
    else:
        # make a fancy table to represent output
        tabulated = tabulate(tokens, ('opt_value', 'token_name', 'state'), "fancy_grid")
        print_and_write(file_out, tabulated)

# have error
else:
    exit(2)