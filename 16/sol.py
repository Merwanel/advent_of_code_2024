import heapq
import math


def solve(file : str) -> tuple[int, int] :
    grid : list[str] = []
    with open(file, 'r') as f :
        for line in f :
            grid.append(list(line.strip()))
    N, M = len(grid), len(grid[0])
    r_start, c_start = 0, 0
    r_end, c_end = 0, 0
    
    
    for r in range(N) : 
        for c in range(M) :
            if grid[r][c] == 'S' :
                r_start, c_start = r, c
            if grid[r][c] == 'E' :
                r_end, c_end = r, c
                
    DIRECTIONS = ((0,1), (1,0), (0,-1), (-1,0))
    best = {(r_start, c_start, 0) : 0, (r_end, c_end):math.inf}
    min_heap = [(0, r_start, c_start, 0, set([(r_start, c_start)]))]
    tot_seen = set()
    while min_heap :
        cost, r, c, i_direction, seen  = heapq.heappop(min_heap)
            
        if cost  > best[(r_end, c_end)] :
            return best[(r_end, c_end)], len(tot_seen)
        if (r, c) == (r_end, c_end) :
            best[(r_end, c_end)] = cost
            tot_seen |= seen
            continue
        
        dr, dc = DIRECTIONS[i_direction]
        if grid[r+dr][c+dc] != '#' and best.get((r+dr,c+dc, i_direction), math.inf) >= cost + 1 :  # equal to get all the paths of minimum cost 
            best[(r+dr,c+dc, i_direction)] = cost + 1
            heapq.heappush(min_heap, (cost + 1 ,r+dr,c+dc, i_direction, seen | set([(r+dr,c+dc)])))
            
            
        for turn in (1,-1) :
            if best.get((r, c, (i_direction+turn)%len(DIRECTIONS)), math.inf) >= cost + 1000 :
                best[(r, c, (i_direction+turn)%len(DIRECTIONS))] = cost + 1000
                heapq.heappush(min_heap, (cost + 1000 , r, c, (i_direction+turn)%len(DIRECTIONS), seen.copy()))        
    
    return -1
    


print(solve('example.txt')) # 7036, 45
print(solve('example2.txt')) # 11048, 64
print(solve('input.txt')) # 79404, 451