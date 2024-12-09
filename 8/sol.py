import collections
import math
def solve(file : str) -> int :
    grid = []
    with open(file, 'r') as f :
        for line in f :
            grid.append(line.strip())
    N, M = len(grid), len(grid[0])
    positions = collections.defaultdict(list)
    for r in range(N) :
        for c in range(M) :
            if grid[r][c] == '.' :
                continue
            positions[grid[r][c]].append((r,c))
    ans_part1, ans_part2 = 0, 0
    res = [list(row) for row in grid]
    res2 = [list(row) for row in grid]
    for letter in positions :
        for i in range(len(positions[letter])) :
            r1, c1 = positions[letter][i]
            for j in range(len(positions[letter])) :
                if i == j :
                    continue
                r2, c2 = positions[letter][j]
                dr, dc = abs(r1 - r2), abs(c1 - c2)
                for sign_r, sign_dc in ((1,1), (1,-1), (-1,1), (-1,-1)) :
                    r3, c3, = r1 + dr * sign_r, c1 + dc * sign_dc
                    if good(r1, c1, r2, c2, r3, c3, N, M) and res[r3][c3] != '#' :
                        ans_part1 += 1
                        res[r3][c3] = '#'
                    if good(r1, c1, r2, c2, r3, c3, N, M) :
                        while 0 <= r3 < N and 0 <= c3 < M :
                            if res2[r3][c3] != '#' :
                                ans_part2 += 1
                                res2[r3][c3] = '#'
                            r3, c3, = r3 + dr * sign_r, c3 + dc * sign_dc
                if res2[r2][c2] != '#':
                    ans_part2 += 1
                    res2[r2][c2] = '#'
    # [print("".join(row)) for row in res]
    # [print("".join(row)) for row in res2]
    return ans_part1, ans_part2

def good(rmid: int, cmid: int, r1: int, c1: int, r2: int, c2: int, N: int, M: int) -> bool :
    if not (0 <= r2 < N and 0 <= c2 < M) :
        return False
    distance_mid_r1 = (rmid - r1) ** 2 + (cmid - c1) ** 2
    distance_mid_r2 = (rmid - r2) ** 2 + (cmid - c2) ** 2
    if distance_mid_r1 != distance_mid_r2 :
        return False
    # translate the 3 points so that (rmid, cmid) is at the origin,
    # then compute the angle they each make with the the x-axis, the diff is the angle searched for
    angle_rad = math.atan2(c2 - cmid, r2 - rmid) - math.atan2(c1 - cmid, r1 - rmid)
    return round(abs(angle_rad),4) == round(math.pi,4)



print(solve('small.txt')) # 4, 8
print(solve('example.txt')) # 14, 34
print(solve('example2.txt')) # 3, 9
print(solve('input_small.txt')) # 51, 176
print(solve('input.txt')) # 367, 1285