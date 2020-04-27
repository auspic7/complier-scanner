import string, copy
from Automata import DFA, generate_dfa_out_of_list, Life

positive = '123456789'
INT = DFA(string.digits + "-",
          [(0, '0', 1), (0, positive, 3), (0, '-', 2), (2, positive, 3), (3, string.digits, 3)], 0, [1, 3])
FLOAT = DFA(string.digits + '-.', [(0, '-', 1), (0, '0', 2), (0, positive, 3), (1, '0', 2), (1, positive, 3),
                                   (3, string.digits, 3), (3, '.', 4), (2, '.', 4), (4, string.digits, 5),
                                   (5, positive, 5), (5, '0', 6), (6, positive, 5), (6, '0', 6), (5, positive, 5)], 0, [5])
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

file = open('input.c')
file_inp = file.read()
print(file_inp)


def print_error(text, i):
    # 에러 메시지 출력
    line_no = text[:i].count('\n') + 1
    line_starting = text[:i].rfind('\n')
    print(f'error occurred on line {line_no}')
    print(f'{text.splitlines()[line_no-1]}')
    print(' ' * (i - line_starting - 1) + '^')
    print('unexpected character')
    return


# DFA_LIST를 이용해 string을 lexical analyze
def lexically_analyze(string_to_scan, dfa_list):
    # 결과가 되는 렉심 리스트
    lexemes = []
    # 이번 토큰의 시작지점
    lexeme_start = 0
    # string을 순회하기 위한 index
    i = 0
    # 후보 dfa, 이번 토큰의 끝지점
    determined_dfa = lexeme_end = None

    # 파일의 끝까지 순회
    while i < len(string_to_scan):
        # halt되지 않은 dfa의 리스트
        alive_dfa = [item for item in dfa_list if item.process(string_to_scan[i]) == Life.ALIVE]
        # final state에 있는 dfa의 리스트
        final_dfa = [item for item in dfa_list if item.isfinal()]

        # final state에 있고 살아있는 dfa가 있다면
        if final_dfa:
            # 그 중 최상위 우선순위를 가지는 dfa를 후보로 선정, 토큰의 끝 또한 저장
            (determined_dfa, lexeme_end) = (final_dfa[0], i)

        # 모든 dfa가 halt되었다면
        if not alive_dfa:
            # 후보 dfa(lexeme_start부터 찾아봤을 때 가장 긴 토큰을 만드는 dfa)가 존재하지 않는다면(lexeme_start부터 토큰이 없음)
            if not determined_dfa:
                # 에러 메시지 출력
                print_error(string_to_scan, i)
                return
            # 후보 dfa가 존재하므로 이 dfa가 답이다. lexemes에 렉심과 dfa를 추가함
            lexemes.append((string_to_scan[lexeme_start:lexeme_end + 1], determined_dfa.name))
            # 다음 토큰의 시작지점은 이번 토큰의 끝지점 다음 글자. 당연히 i도 같음
            i = lexeme_start = lexeme_end + 1
            # i번 글자부터 새로 파싱을 시작하기 위한 초기화
            determined_dfa = lexeme_end = None
            for dfa in dfa_list:
                dfa.setstate(0)
            continue
        print([item.name for item in alive_dfa])
        print([item.name for item in final_dfa])
        print(lexemes)
        i += 1

    # 마지막 토큰을 parse할 수 없는 경우
    if not determined_dfa:
        print_error(string_to_scan, i)
        return
    # 마지막 토큰을 추가
    lexemes.append((string_to_scan[lexeme_start:lexeme_end + 1], determined_dfa.name))
    return lexemes


print("\n".join(map(str, lexically_analyze(file_inp, DFAs))))

# Arithmatic operation: 마이너스인가? 빼기인가? 이것을 scanner가 해결 가능?
