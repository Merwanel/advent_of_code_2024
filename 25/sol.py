
def solve(file : str) -> int :
    grids = [[]]
    with open(file, 'r') as f :
        for line in f :
            if line == "\n" :
                grids.append([])
            else :
                grids[-1].append(line.strip())
    locks, keys = [], []
    for grid in grids :
        vals = []
        for c in range(len(grid[0])) :
            vals.append(-1)
            for r in range(len(grid)) :
                vals[-1] += grid[r][c] == '#'
        if grid[0].count('#') == len(grid[0]) :
            locks.append(vals)
        else :
            keys.append(vals)
    fit = 0
    for lock in locks :
        for key in keys :
            fit += all(l+k <= 5 for l, k in zip(lock, key))
    return fit


print(solve('example.txt')) # 3
print(solve('input.txt')) # 3077