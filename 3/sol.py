import re

def solve(file: str, part1=True) -> int :
    ans = 0
    last_was_do = True
    with open(file, 'r') as f :
        for line in f :
            valid = re.findall("mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))", line) # [('2', '4', '', ''), ('', '', '', "don't()"), ('5', '5', '', ''), ('11', '8', '', ''), ('', '', 'do()', ''), ('8', '5', '', '')]
            for a, b, do, dont in valid :
                if a != '' and (last_was_do or part1) :
                    ans += int(a) * int(b)
                if do :
                    last_was_do = True
                if dont :
                    last_was_do = False
                    
    return ans
            
    

print(solve('example.txt'))     # 161
print(solve('input.txt'))                 # 174561379
print(solve('example2.txt', part1=False)) # 48
print(solve('input.txt', part1=False))      # 106921067   