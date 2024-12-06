from typing import List
    
def solve(file : str) -> int :
    grid = []
    with open(file, 'r') as f :
        for line in f :
            grid.append(list(line.strip()))

    N, M = len(grid), len(grid[0])
    r_start, c_start = 0, 0
    for r in range(N) :
        for c in range(M) :
            if grid[r][c] == '^' :
                r_start, c_start = r, c
    DIRECTIONS = ((-1,0), (0,1), (1,0), (0,-1))
    def part1() :
        seen = set()
        r, c = r_start, c_start
        i_direction = 0
        while  0 <= r < N and 0 <= c < M :
            seen.add((r, c))
            dr, dc = DIRECTIONS[i_direction]

            if not (0 <= r + dr < N) or not (0 <= c + dc < M) :
                break
            if grid[r+dr][c+dc] == '#' :
                i_direction = (i_direction+1) % len(DIRECTIONS)
                continue
            r , c = r + dr, c + dc
        
        return len(seen)
    
    def part2() :
        # a closure in a closure lol
        def isThereACircle() -> bool :
            seen = set()
            r, c = r_start, c_start
            i_direction = 0
            prev_change = None
            while  0 <= r < N and 0 <= c < M :
                dr, dc = DIRECTIONS[i_direction]

                if not (0 <= r + dr < N) or not (0 <= c + dc < M) :
                    break
                if grid[r+dr][c+dc] == '#' :
                    if prev_change != None :
                        if (*prev_change, r, c) in seen :
                            return True
                        seen.add((*prev_change, r, c))
                    prev_change = (r, c)
                    i_direction = (i_direction+1) % len(DIRECTIONS)
                    continue
                r , c = r + dr, c + dc
            return False
            
        ans = 0
        for r in range(N) :
            for c in range(M) :
                if grid[r][c] != '#' :
                    grid[r][c] = '#'
                    ans += isThereACircle()
                    grid[r][c] = '.'
        return ans
    return part1(), part2()
    


print(solve('example.txt')) # 41, 6
print(solve('input.txt')) # 5199, 1915