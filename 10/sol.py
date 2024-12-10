def solve(file : str) -> tuple[int,int] :
    grid = []
    with open(file, 'r') as f :
        for line in f :
            grid.append([int(n) for n in line.strip()])
    N, M = len(grid), len(grid[0])
    
    def score_and_rating(r: int, c :int) -> int :
        if grid[r][c] == 9 :
            if (r, c) in nines_seen :
                return 0, 1
            nines_seen.add((r,c))
            return 1, 1
        score, rating = 0, 0
        for dr , dc in ((0,1), (1,0), (-1,0), (0,-1)) :
            r2 , c2 = r + dr, c + dc
            if 0 <= r2 < N and 0 <= c2 < M and grid[r2][c2] == 1 + grid[r][c] :
                score_from_here, rating_from_here = score_and_rating(r2, c2)
                score, rating = score + score_from_here, rating + rating_from_here
        return score, rating
    
    score, rating = 0, 0
    for r in range(N) :
        for c in range(M) :
            if grid[r][c] == 0:
                nines_seen = set()
                score_from_here, rating_from_here = score_and_rating(r, c)
                score, rating = score + score_from_here, rating + rating_from_here
    return score, rating 



print(solve('example.txt')) # 36, 81
print(solve('input.txt')) # 825, 1805