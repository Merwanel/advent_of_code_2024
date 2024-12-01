import collections
from typing import List


def part1(A: List[int], B: List[int]) -> int :
    A.sort()
    B.sort()
    return sum( abs(a - b) for a, b in zip(A, B))

def part2(A: List[int], B: List[int]) -> int:
    count_B = collections.Counter(B)
    return sum( a * count_B[a] for a in A)
    
def solve(file : str, part: callable) -> int :
    A, B = [], []
    with open(file, 'r') as f :
        for line in f :
            a, b = line.split('   ')
            A += [int(a)]
            B += [int(b)]
    return part(A, B)

print(solve('example.txt', part1))         
print(solve('input.txt', part1))         
print(solve('example.txt', part2))         
print(solve('input.txt', part2))         