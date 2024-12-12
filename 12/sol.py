def solve(file : str) -> tuple[int,int] :
    DIRECTIONS = ((0,1), (1,0), (-1,0), (0,-1))
    grid = []
    with open(file, 'r') as f :
        for line in f :
            grid.append(line.strip())
    N, M = len(grid), len(grid[0])
    seen = [[False] * M for _ in range(N)]
    
    def area_and_perimeter(r: int, c :int) -> tuple[int, int] :
        seen[r][c] = True
        area, perimeter = 1, 0
        for dr , dc in DIRECTIONS :
            r2 , c2 = r + dr, c + dc
            if 0 <= r2 < N and 0 <= c2 < M and grid[r][c] == grid[r2][c2] :
                if not seen[r2][c2]  :
                    area_from_here, perimeter_from_here = area_and_perimeter(r2, c2)
                    area, perimeter = area + area_from_here, perimeter + perimeter_from_here
            else :
                perimeter += 1
                unconnected_sides.add((r, c, r2,c2))
        return area, perimeter
    
    def connect_sides(r: int, c :int) -> int :
        nb_side = 0
        tmp = []
        while unconnected_sides :
            nb_side += 1
            r1, c1, r2, c2 = unconnected_sides.pop()
            is_a_vertical_limit = r1 == r2
            if is_a_vertical_limit :
                directions = ((1,0), (-1,0))
            else :
                directions = ((0,1), (0,-1))
            
            for dr , dc in directions :
                r1k , c1k = r1 + dr , c1 + dc
                r2k , c2k = r2 + dr , c2 + dc
                while (r1k , c1k, r2k , c2k) in unconnected_sides :
                    unconnected_sides.remove((r1k , c1k, r2k , c2k))
                    tmp.append((r1k , c1k, r2k , c2k))
                    r1k , c1k = r1k + dr , c1k + dc
                    r2k , c2k = r2k + dr , c2k + dc
                
        return nb_side
        
        
    sum_price, sum_price_discounted = 0, 0
    for r in range(N) :
        for c in range(M) :
            if not seen[r][c] :
                unconnected_sides : set[tuple[int, int, int, int]] = set()
                area, perimeter = area_and_perimeter(r, c)
                sum_price += area * perimeter
                sum_price_discounted +=  area * connect_sides(r,c)
    return sum_price, sum_price_discounted



print(solve('example.txt')) # 140, 80
print(solve('example2.txt')) # 772, 436
print(solve('E.txt')) # 692, 236
print(solve('example4.txt')) # 1184, 368
print(solve('example3.txt')) # 1930, 1206
print(solve('input.txt')) # 1449902, 908042