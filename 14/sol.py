from matplotlib import pyplot as plt
import numpy as np


def solve(file : str, N: int, M: int, sec: int, print_grid=False) -> tuple[int, int, int] :
    limitup, limitdown, limitleft, limitright = N // 2 - 1,  N // 2 + 1, M // 2 - 1, M // 2 + 1

    grid = [[0] * M for _ in range(N)]
    q1, q2, q3, q4 = 0, 0, 0, 0
    xs, ys = [], []
    with open(file, 'r') as f :
        for line in f :
                p, v = line.strip().split()
                px, py = map( int, p[2:].split(','))
                vx, vy = map( int, v[2:].split(','))
                px_new, py_new = (px + vx * sec) % M, ( py + vy * sec) % N
                xs.append(py_new)
                ys.append(px_new)
                grid[py_new][px_new] += 1
                if px_new <= limitleft and py_new <= limitup :
                    q1 += 1
                if px_new >= limitright and py_new <= limitup :
                    q2 += 1
                if px_new <= limitleft and py_new >= limitdown :
                    q3 += 1
                if px_new >= limitright and py_new >= limitdown :
                    q4 += 1

    if print_grid :
        [print("".join(map(lambda c : '*' if c > 0 else ' ', row))) for row in grid]
        
    return q1 * q2 * q3 * q4, np.var(xs), np.var(ys)


##############################################
########## part1
##############################################
print(solve('example.txt', 7, 11, 100)[0]) # 12
print(solve('input.txt', 103, 101, 100)[0]) # 211692000


##############################################
########## part2
##############################################
varx, vary = [], []
SEC_MAX = 10_000
for sec in range(1, SEC_MAX) :
    _ , vx, vy = solve('input.txt', 103, 101, sec)
    varx.append(vx)
    vary.append(vy)


plt.scatter(range(1, SEC_MAX), varx, s=.5)
plt.ylabel('varx')
plt.xlabel('secondes')
plt.show()  # -> few under 500
plt.scatter(range(1, SEC_MAX), vary, s=.5)
plt.ylabel('vary')
plt.xlabel('secondes')
plt.show()  # -> few under 400

for i, (vx, vy) in enumerate(zip(varx, vary)) :
    if vx < 500 and vy < 400 :
        print('sec=',i+1)
        solve('input.txt', 103, 101, sec=i+1, print_grid=True)  # -> easter egg at 6587
        
