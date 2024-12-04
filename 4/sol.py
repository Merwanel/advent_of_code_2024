from typing import List

next_expected = { None :'X', 'X':'M', 'M':'A', 'A': 'S'}
def count(grid: List[List[str]], r: int, c: int, dr: int, dc: int) -> int :
    N, M = len(grid), len(grid[0])
    prev = None
    ans = 0
    while 0 <= r < N and 0 <= c < M :
        if grid[r][c] == next_expected[prev] :
            prev = grid[r][c]
            if grid[r][c] == 'S' :
                ans += 1
                prev = None
        elif  grid[r][c] == 'X' :
            prev = 'X'
        else :
            prev = None
        r += dr
        c += dc
        
    prev= None
    r -= dr
    c -= dc
    while 0 <= r < N and 0 <= c < M :        
        if grid[r][c] == next_expected[prev] :
            prev = grid[r][c]
            if grid[r][c] == 'S' :
                ans += 1
                prev = None
        elif  grid[r][c] == 'X' :
            prev = 'X'
        else :
            prev = None
        r -= dr
        c -= dc
        
    return ans
        
    
def part2(grid : List[List[str]]) :
    N, M = len(grid), len(grid[0])
            
    ans = 0
    for r in range(1, N-1) :
        for c in range(1, M-1) :
            if grid[r][c] != 'A' :
                continue
            if grid[r-1][c-1] + grid[r+1][c+1] in ('MS', 'SM') and grid[r+1][c-1] + grid[r-1][c+1] in ('MS', 'SM'):
                ans += 1
    return ans
                

def solve(file: str) -> int :
    grid = []
    with open(file, 'r') as f :
        grid = [line.strip() for line in f] 
        
    N, M = len(grid), len(grid[0])
            
    ans = 0
    for r in range(N) :
        # rows
        ans += count(grid=grid, r=r, c=0 , dr=0, dc=1)
    for c in range(M) :
        # columns
        ans += count(grid=grid, r=0, c=c , dr=1, dc=0)
        
    # diags
    for r in range(N)  :
        # diags left - downright
        ans += count(grid=grid, r=r, c=0 , dr=1, dc=1)
        # diags left - upright
        ans += count(grid=grid, r=r, c=0 , dr=-1, dc=1)
    for c in range(1,M)  :
        # diags left - downright
        ans += count(grid=grid, r=0, c=c , dr=1, dc=1)
        # diags left - upright
        ans += count(grid=grid, r=N-1, c=c , dr=-1, dc=1)
              
    return ans, part2(grid)
            
    

print(solve('example_small.txt'))  #  4    , 0       
print(solve('example.txt'))  #  18, 3         
print(solve('example2.txt'))  #  18, 9     
print(solve('example3.txt'))  #  0, 9         
print(solve('input.txt'))  #  2378, 1796