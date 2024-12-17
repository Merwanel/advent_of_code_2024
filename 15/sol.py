from matplotlib import pyplot as plt
import numpy as np


def solve(file : str) -> tuple[int, int] :
    grid : list[str] = []
    grid_part2 : list[str] = []
    moves = ""
    is_grid = True
    with open(file, 'r') as f :
        for line in f :
            if line == '\n' :
                is_grid = False
            elif is_grid :
                grid.append(list(line.strip()))
                grid_part2.append([])
                for c in grid[-1] :
                    if c == '#' :
                        grid_part2[-1].extend(['#','#'])
                    if c == 'O' :
                        grid_part2[-1].extend(['[',']'])
                    if c == '.' :
                        grid_part2[-1].extend(['.','.'])
                    if c == '@' :
                        grid_part2[-1].extend(['@','.'])
            else :
                moves += line.strip()
    return get_sum(moves, grid), get_sum(moves, grid_part2)

def get_moved_blocks(moves: str, grid : list[str], r_to_move: int, c_to_move: int, dr: int, dc: int) -> tuple[list[tuple[int,int]], bool]:
    N, M = len(grid), len(grid[0])
    
    if grid[r_to_move][c_to_move] == 'O' :
        moved_blocks , can_move = get_moved_blocks(moves, grid, r_to_move+dr, c_to_move+dc, dr, dc)
        if not can_move :
            return [], can_move
        return [(r_to_move, c_to_move)] + moved_blocks, can_move
    elif grid[r_to_move][c_to_move] == '[' : 
        moved_blocks_left , can_move_left = [] , True
        if dc == 1 :
            moved_blocks_left , can_move_left = get_moved_blocks(moves, grid, r_to_move, c_to_move+2, dr, dc)
        elif dc == -1 :
            moved_blocks_left , can_move_left = get_moved_blocks(moves, grid, r_to_move, c_to_move-1, dr, dc)
        elif dr != 0 :
            moved_blocks_left , can_move_left = get_moved_blocks(moves, grid, r_to_move+dr, c_to_move, dr, dc)
        moved_blocks_right , can_move_right = [] , True
        if dc == 0 :
            moved_blocks_right , can_move_right = get_moved_blocks(moves, grid, r_to_move+dr, c_to_move+1+dc, dr, dc)
        if not can_move_left or not can_move_right :
            return [], can_move_left and can_move_right
        return [(r_to_move, c_to_move)] + moved_blocks_left + moved_blocks_right, can_move_left and can_move_right
    elif grid[r_to_move][c_to_move] == ']' : 
        if dr != 0 :
            return get_moved_blocks(moves, grid, r_to_move, c_to_move-1, dr, dc)
        if dc == -1 :
            return get_moved_blocks(moves, grid, r_to_move, c_to_move-1, dr, dc)
    elif grid[r_to_move][c_to_move] == '.' : 
        return [], True
    
    return [], False
    
    
def get_sum(moves: str, grid : list[str]) -> int :
    N, M = len(grid), len(grid[0])
    r_robot, c_robot = None, None
    for r in range(N) :
        for c in range(M) :
            if grid[r][c] == '@' :
                r_robot, c_robot = r, c
    moves_map = {'^':(-1,0), '>':(0,1), 'v':(1,0), '<':(0,-1)}
    for move in moves :
        dr, dc = moves_map[move]
        r, c = r_robot, c_robot
        moved_blocks, can_move = get_moved_blocks(moves, grid, r+dr, c+dc, dr, dc)
        # duplicate are possible
        #  ...v....
        #  ...[]...
        #  ..[][]..
        #  .[]..[].
        #  []....[]
        #  .[]..[].
        #  ..[][]..
        #  ...[]... -> will appear two times
        if not can_move :
            continue
        seen = set()
        for r_to_move, c_to_move in reversed(moved_blocks) :
            
            if (r_to_move, c_to_move) in seen :
                continue
            seen.add((r_to_move, c_to_move))
            if grid[r_to_move][c_to_move] == 'O' :
                grid[r_to_move][c_to_move] = '.'
                grid[r_to_move+dr][c_to_move+dc] = 'O'
            if grid[r_to_move][c_to_move] == '[' :
                grid[r_to_move][c_to_move] = '.'
                grid[r_to_move][c_to_move+1] = '.'
                grid[r_to_move+dr][c_to_move+dc] = '['
                grid[r_to_move+dr][c_to_move+1+dc] = ']'
                    
        grid[r+dr][c+dc] , grid[r][c] = grid[r][c], grid[r+dr][c+dc]
        r_robot, c_robot = r_robot + dr, c_robot + dc
        
    sum_coord = 0
    for r in range(N) :
        for c in range(M) :
            if grid[r][c] == 'O' :
                sum_coord += 100 * r + c
            if grid[r][c] == '[' :
                sum_coord += 100 * r + c
        
    return sum_coord


print(solve('example_small.txt')) # 2028, 1751
print(solve('example.txt')) # 10092, 9021
print(solve('input.txt')) # 1465152, 1511259
