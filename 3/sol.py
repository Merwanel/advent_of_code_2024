import re
from Parser import Parser

def solve(file: str, part1=True) -> int :
    ans = 0
    last_was_do = True
    with open(file, 'r') as f :
        for line in f :
            valid = re.findall("mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))", line)  # [('2', '4', '', ''), ('', '', '', "don't()"), ('5', '5', '', ''), ('11', '8', '', ''), ('', '', 'do()', ''), ('8', '5', '', '')]
            for a, b, do, dont in valid :
                if a != '' and (last_was_do or part1) :
                    ans += int(a) * int(b)
                if do :
                    last_was_do = True
                if dont :
                    last_was_do = False
                    
    return ans
def solve_w_parser(file: str, part1=True) -> int :
    with open(file, 'r') as f :
        parser = Parser(is_part1=part1, f=f)
        parser.parseIt()
    return parser.ans
            
    


print(solve('example.txt'))     # 161
print(solve('input.txt'))                 # 174561379
print(solve('example2.txt', part1=False)) # 48
print(solve('input.txt', part1=False))      # 106921067   
print()
print(solve_w_parser('example.txt'))     # 161
print(solve_w_parser('input.txt'))                 # 174561379
print(solve_w_parser('example2.txt', part1=False)) # 48
print(solve_w_parser('input.txt', part1=False))      # 106921067   