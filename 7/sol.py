from typing import List

def solve(file : str) -> int :
    sum_good1, sum_good2 = 0, 0
    with open(file, 'r') as f :
        for line in f :
            test_value, equation = line.strip().split(': ')
            equation = [int(n) for n in equation.split(' ')]
            test_value = int(test_value)
            sum_good1 += good(test_value, equation)
            sum_good2 += good(test_value, equation, is_part2 = True)
    return sum_good1, sum_good2

def good(test_value: str, equation: List[int], is_part2=False) :
    def backtrack(i, res) -> bool :
        if i == len(equation) :
            return res == test_value
        plus = backtrack(i+1, equation[i] + res )
        product = backtrack(i+1,equation[i] * res)
        concat = backtrack(i+1, int(str(res) + str(equation[i]))) if is_part2 else False
        return plus or product or concat
    return test_value if backtrack(1, equation[0]) else 0
        


print(solve('example.txt')) # 3749, 11387
print(solve('input.txt')) # 5702958180383, 92612386119138