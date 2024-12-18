import collections


def solve(file : str, N: int, M: int, first: int) -> int :
    bits : set[tuple[str,str]] = set()
    b = 1
    with open(file, 'r') as f :
        for line in f :
            c, r = line.strip().split(',')
            bits.add((int(r), int(c)))
            b += 1
            if b > first :
                break
    q = collections.deque([(0,0)])
    seen = set([(0,0)])
    DIRECTIONS = ((0,1), (1,0), (0,-1), (-1,0))
    step = 0
    while q :
        step += 1
        size = len(q)
        for _ in range(size) :
            r, c = q.popleft()
            for dr, dc in DIRECTIONS :
                r2, c2 = r + dr , c + dc
                if (r2,c2) == (N-1, M-1) :
                    return step
                if 0 <= r2 < N and 0 <= c2 < M and (r2,c2) not in seen and (r2,c2) not in bits :
                    q.append((r2, c2))
                    seen |= {(r2,c2)}
                
    return -1



######
#    part 1
#####
print(solve('example.txt', N=7, M=7, first=12)) # 22
print(solve('input.txt', N=71, M=71, first=1024)) # 262

######
#    part 2
#####
def binary_search(file: str, N: int, M: int) :
    high = 12
    low = 0
    while solve(file=file, N=N, M=M, first=high) != -1 :
        low = high
        high *= 2
    best = high
    while low <= high :
        mid = low + (high - low) // 2
        if solve(file=file, N=N, M=M, first=mid) == -1 :
            best = mid
            high = mid - 1
        else :
            low = mid + 1
        
    return best
print(binary_search('example.txt', N=7, M=7)) # 21  => 6,1 in the file
print(binary_search('input.txt', N=71, M=71)) # 2974  => 22,20 in the file
        