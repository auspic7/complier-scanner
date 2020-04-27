import argparse
from Automata import Life
from PredefinedDFA import DFAs
from tabulate import tabulate

parser = argparse.ArgumentParser()
parser.add_argument('input_file_name', help='Desired file name to analyze', type=str)
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument('-l', '--list', help='list shaped output for module use', action="store_true")
args = parser.parse_args()


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
        if args.verbose:
            print(f'alive_dfa({string_to_scan[i]}): {[item.name for item in alive_dfa]}')
            print(f'final_dfa({string_to_scan[i]}): {[item.name for item in final_dfa]}')
            print(f'lexemes({string_to_scan[i]}): {lexemes}')
        i += 1

    # 마지막 토큰을 parse할 수 없는 경우
    if not determined_dfa:
        print_error(string_to_scan, i)
        return
    # 마지막 토큰을 추가
    lexemes.append((string_to_scan[lexeme_start:lexeme_end + 1], determined_dfa.name))
    return lexemes

# 파일 입력
file = open(args.input_file_name)
file_txt = file.read()
if args.verbose:
    print(file_txt)

# 토큰 분석
tokens = lexically_analyze(file_txt, DFAs)

# 에러 없는 경우
if tokens:
    # 인자 주어진 경우 그대로 출력
    if args.list:
        print(tokens)
    else:
        # 표로 만들어서 출력
        escaped = [(repr(token[0]), token[1]) for token in tokens]
        print(tabulate(tokens, ('opt_value', 'token_name'), "fancy_grid"))
else:
    exit(2)