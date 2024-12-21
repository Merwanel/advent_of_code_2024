import collections
import heapq
import math
import sys
sys.setrecursionlimit(100_000)


def solve(file : str, saving_target_at_least: int, cheat_time_max:int=2) -> tuple[int, int] :
    grid : list[str] = []
    with open(file, 'r') as f :
        for line in f :
            grid.append(list(line.strip()))
    N, M = len(grid), len(grid[0])
    r_start, c_start = 0, 0 
    
    for r in range(N) : 
        for c in range(M) :
            if grid[r][c] == 'S' :
                r_start, c_start = r, c
            if grid[r][c] == 'E' :
                r_end, c_end = r, c
    time_without_cheating = {}
    DIRECTIONS = ((0,1), (1,0), (0,-1), (-1,0))
    def dfs(r,c, prev_r=-1, prev_c=-1, target='E') :
        if grid[r][c] == target :
            return 0
        for dr, dc in DIRECTIONS :
            r2, c2 = r+dr,c+dc
            if 0 <= r2 < N and 0 <= c2 < M and (r2, c2) != (prev_r, prev_c) and grid[r2][c2] != '#': 
                time_without_cheating[(r, c)] = 1 + dfs(r2, c2, prev_r=r, prev_c=c,target=target)
        return time_without_cheating[(r, c)]

    def bfs(base_time=-1,is_cheating_allowed=False, cheat_last_time:int=-1,saving_target=-math.inf) :
        q = collections.deque([(r_start, c_start, is_cheating_allowed, cheat_last_time-1, set([(r_start, c_start)]), [])])
        # q = collections.deque([(r_start, c_start, is_cheating_allowed, cheat_last_time-1, set([(r_start, c_start)]))])
        ans = 0
        time = 0
        time_max = base_time - saving_target 
        while time <= time_max :
            size = len(q)
            for _ in range(size) :
                r, c, is_cheat_available, cheat_remaining_time, seen,path  = q.popleft()
                # r, c, is_cheat_available, cheat_remaining_time, seen  = q.popleft()
                is_cheat_available = is_cheat_available and cheat_remaining_time >= 0
                is_cheat_activated = is_cheat_available and cheat_remaining_time < cheat_last_time-1
                
                # if (r,c)==(7,7) :
                #     print(path, len(path), is_cheat_available, cheat_remaining_time)
                for dr, dc in DIRECTIONS :
                    r2, c2 = r+dr,c+dc
                    if 0 <= r2 < N and 0 <= c2 < M and (r2, c2) not in seen :   
                        if grid[r2][c2] == 'E' :
                            ans += 1
                        elif grid[r2][c2] == '.' :
                            if time + time_without_cheating[(r2,c2)] <= time_max :
                                ans += 1
                                print((r2,c2), cheat_remaining_time, path)
                            elif is_cheat_available : 
                                if not is_cheat_activated :
                                    q.append((r2, c2 , is_cheat_available, cheat_remaining_time, seen | {(r2,c2)}, path + [(r2,c2)]))
                                    # q.append((r2, c2 , is_cheat_available, cheat_remaining_time, seen | {(r2,c2)}))
                                elif is_cheat_activated and  cheat_remaining_time > 0 :
                                    q.append((r2, c2 , is_cheat_available, cheat_remaining_time-1, seen | {(r2,c2)}, path + [(r2,c2,'h')]))
                                    # q.append((r2, c2 , is_cheat_available, cheat_remaining_time-1, seen | {(r2,c2)}))
                                    # print(r2, c2 , is_cheat_available, cheat_remaining_time-1, seen | {(r2,c2)})
                        elif is_cheat_available and cheat_remaining_time > 0 :
                            q.append((r2, c2 , is_cheat_available,cheat_remaining_time-1, seen | {(r2,c2)}, path + [(r2,c2,True)]))
                            # q.append((r2, c2 , is_cheat_available,cheat_remaining_time-1, seen | {(r2,c2)}))
            time += 1
        # print([print(r) for r in q])
        return ans
    base_time = dfs(r_start, c_start)
    time_without_cheating_from_start_to_end = time_without_cheating.copy()
    time_without_cheating_from_start_to_end[(r_end,c_end)] = 0
    time_without_cheating = {}
    # print(time_without_cheating_from_start_to_end)
    dfs(r_end, c_end, target='S')
    time_without_cheating_from_end_to_start = time_without_cheating.copy()
    time_without_cheating_from_end_to_start[(r_start,c_start)] = 0
    # print(time_without_cheating_from_end_to_start)
    ans = 0
    target_time = base_time - saving_target_at_least
    for r1 in range(N) : 
        # print(r1)
        for c1 in range(M) :
            if grid[r1][c1] == '#' :
                continue
            for r2 in range(N) : 
                for c2 in range(M) :
                    if grid[r2][c2] == '#' :
                        continue
                    dist_manhathan = abs(r1-r2) + abs(c1-c2)
                    if dist_manhathan <= cheat_time_max and time_without_cheating_from_end_to_start[(r1,c1)] + dist_manhathan + time_without_cheating_from_start_to_end[(r2,c2)] <= target_time :
                        ans += 1
                        # print((r1,c1), (r2,c2), dist_manhathan, time_without_cheating_from_end_to_start[(r1,c1)] + dist_manhathan + time_without_cheating_from_start_to_end[(r2,c2)] , target_time)
    return ans
    nb=0
    # print(good_path)
    # nb = bfs(base_time=base_time, is_cheating_allowed=True, cheat_last_time=cheat_last_time, saving_target=saving_target_at_least)
    ans = set()
    path = []
    def dfs2(r,c, time, time_max, cheat_remaining_time, is_cheat_activated, start:tuple[int,int], seen ) :
        # if (r, c) == (7,7) :
        if time > time_max :
            return
        if grid[r][c] == 'E' or (grid[r][c] == '.' and time + time_without_cheating.get((r,c), math.inf)  <= time_max) :
            ans.add((*start, r,c))
            print('H',time, time_max,start,(r,c),grid[r][c] , cheat_remaining_time,is_cheat_activated, path)
            # cheats can last any amount of time up to and including 20 picoseconds (but can still only end when the program is on normal track)
            # return
        if is_cheat_activated and cheat_remaining_time == 0 :
            return
        for dr, dc in DIRECTIONS :
            r2, c2 = r+dr, c+dc
            if 0 <= r2 < N and 0 <= c2 < M and (r2, c2) not in seen :
                if is_cheat_activated and cheat_remaining_time > 0: 
                    path.append((r2,c2))
                    dfs2(r2, c2, time+1, time_max, cheat_remaining_time-1, is_cheat_activated, start, seen | {(r2,c2)})
                    path.pop()
                elif grid[r2][c2] == '#' and not is_cheat_activated : 
                    path.append((r2,c2, True))
                    dfs2(r2, c2, time+1, time_max, cheat_remaining_time-1, True, (r,c), seen | {(r2,c2)})
                    path.pop()
                elif grid[r2][c2] == '.' :
                    path.append((r2,c2))
                    dfs2(r2, c2, time+1, time_max, cheat_remaining_time, is_cheat_activated, start, seen | {(r2,c2)})
                    path.pop()
    dfs2(r_start, c_start, 0, base_time - saving_target_at_least , cheat_time_max, False, (-1,-1), set())
    print(ans)
    return len(ans)

#########################
########  part 1
#########################
# for the example :
    # There are 14 cheats that save 2 picoseconds.
    # There are 14 cheats that save 4 picoseconds.
    # There are 2 cheats that save 6 picoseconds.
    # There are 4 cheats that save 8 picoseconds.
    # There are 2 cheats that save 10 picoseconds.
    # There are 3 cheats that save 12 picoseconds.
    # There is one cheat that saves 20 picoseconds.
    # There is one cheat that saves 36 picoseconds.
    # There is one cheat that saves 38 picoseconds.
    # There is one cheat that saves 40 picoseconds.
    # There is one cheat that saves 64 picoseconds.

print(solve('example.txt', saving_target_at_least=2, cheat_time_max=2)) # 44
print(solve('example.txt', saving_target_at_least=4, cheat_time_max=2)) # 30
print(solve('example.txt', saving_target_at_least=6, cheat_time_max=2)) # 16
print(solve('example.txt', saving_target_at_least=8, cheat_time_max=2)) # 14
print(solve('example.txt', saving_target_at_least=10, cheat_time_max=2)) # 10
print(solve('example.txt', saving_target_at_least=12, cheat_time_max=2)) # 8
print(solve('example.txt', saving_target_at_least=20, cheat_time_max=2)) # 5
print(solve('example.txt', saving_target_at_least=36, cheat_time_max=2)) # 4
print(solve('example.txt', saving_target_at_least=38, cheat_time_max=2)) # 3
print(solve('example.txt', saving_target_at_least=40, cheat_time_max=2)) # 2
print(solve('example.txt', saving_target_at_least=64, cheat_time_max=2)) # 1


print(solve('input.txt', saving_target_at_least=100, cheat_time_max=2)) # 1395


#########################
########  part 2
#########################
print()
# for the example with a cheat lasting 20 : 
    # There are 32 cheats that save 50 picoseconds.
    # There are 31 cheats that save 52 picoseconds.
    # There are 29 cheats that save 54 picoseconds.
    # There are 39 cheats that save 56 picoseconds.
    # There are 25 cheats that save 58 picoseconds.
    # There are 23 cheats that save 60 picoseconds.
    # There are 20 cheats that save 62 picoseconds.
    # There are 19 cheats that save 64 picoseconds.
    # There are 12 cheats that save 66 picoseconds.
    # There are 14 cheats that save 68 picoseconds.
    # There are 12 cheats that save 70 picoseconds.
    # There are 22 cheats that save 72 picoseconds.
    # There are 4 cheats that save 74 picoseconds.
    # There are 3 cheats that save 76 picoseconds.
print(solve('example.txt', saving_target_at_least=50, cheat_time_max=20)) # 285
print(solve('example.txt', saving_target_at_least=52, cheat_time_max=20)) # 253
print(solve('example.txt', saving_target_at_least=54, cheat_time_max=20)) # 222
print(solve('example.txt', saving_target_at_least=56, cheat_time_max=20)) # 193
print(solve('example.txt', saving_target_at_least=58, cheat_time_max=20)) # 154
print(solve('example.txt', saving_target_at_least=60, cheat_time_max=20)) # 129
print(solve('example.txt', saving_target_at_least=62, cheat_time_max=20)) # 106
print(solve('example.txt', saving_target_at_least=64, cheat_time_max=20)) # 86
print(solve('example.txt', saving_target_at_least=66, cheat_time_max=20)) # 67
print(solve('example.txt', saving_target_at_least=68, cheat_time_max=20)) # 55
print(solve('example.txt', saving_target_at_least=70, cheat_time_max=20)) # 41
print(solve('example.txt', saving_target_at_least=72, cheat_time_max=20)) # 29
print(solve('example.txt', saving_target_at_least=74, cheat_time_max=20)) # 7
print(solve('example.txt', saving_target_at_least=76, cheat_time_max=20)) # 3

print(solve('input.txt', saving_target_at_least=100, cheat_time_max=20)) # 993178