import z3
import collections
import heapq


def solve(file : str, is_part2 : bool) -> int :
    cost_min = 0
    coords = []
    with open(file, 'r') as f :
        for line in f :
            if line == '\n' :
                coords = []
            elif line[0] == 'B' :
                coords.append(tuple( int(incr[2:]) for incr in line.strip()[10:].split(', ')))
            else :
                if is_part2 :
                    coord_prize = tuple( int(incr[2:]) + 10000000000000 for incr in line.strip()[7:].split(', '))
                    cost_min += solve_w_z3(*coords[0], *coords[1], *coord_prize)
                
                else :
                    coord_prize = tuple( int(incr[2:]) for incr in line.strip()[7:].split(', '))
                    cost_min += dijkstra(*coords[0], *coords[1], *coord_prize, is_part2)
                    # cost_min += way2(*coords[0], *coords[1], *coord_prize)
    return cost_min

# quicker than the other 2 way
def solve_w_z3(xa, ya, xb, yb , xp, yp) : 
    A = z3.Int('A')
    B = z3.Int('B')
    cost = z3.Int('cost')
    
    o = z3.Optimize()

    # Add constraints
    o.add(A * xa + B * xb == xp)
    o.add(A * ya + B * yb == yp)
    o.add(cost == A * 3 + B)
    o.minimize(cost)
    if o.check():
        res = o.model()[cost] 
        return res.as_long() if res is not None else 0
    return 0
    
def way2(xa, ya, xb, yb , xp, yp) :
    bestCost = None
    for nbA in range(100+1) :
        xtarget, ytarget = xp - xa * nbA , yp - ya * nbA
        if xtarget < 0 or ytarget < 0 :
            break 
        nbBx, modx = divmod(xtarget , xb)
        nbBy, mody = divmod(ytarget , yb)
        if modx == mody == 0 and nbBx == nbBy :
            cur_cost = nbA * 3 + nbBx
            if bestCost == None or bestCost > cur_cost :
                bestCost = cur_cost 
    return bestCost if bestCost != None else 0 

    
                
def dijkstra(xa, ya, xb, yb , xp, yp, is_part2) -> int :
    min_heap = [(0, 0, 0, 0, 0)]
    best = collections.defaultdict(int)
    while min_heap :
        # print(len(min_heap))
        cost, x, y, nbA, nbB = heapq.heappop(min_heap)
        if (x, y) == (xp, yp) :
            return cost
        if (is_part2 or nbA+1 <= 100) and x + xa <= xp and y + ya <= yp and ((x + xa,y + ya) not in best or best[(x + xa, y + ya)] > cost + 3) :
            best[(x + xa,y + ya)] = cost + 3
            heapq.heappush(min_heap, (cost + 3, x + xa, y + ya, nbA + 1, nbB))
        if (is_part2 or nbB+1 <= 100) and x + xb <= xp and y + yb <= yp and ((x + xb,y + yb) not in best or best[(x + xb, y + yb)] > cost + 1) :
            best[(x + xb,y + yb)] = cost + 1
            heapq.heappush(min_heap, (cost + 1, x + xb, y + yb, nbA, nbB + 1))
    return 0



print(solve('example.txt', False)) # 480
print(solve('input.txt', False)) # 27105
print(solve('example.txt', True)) # 875318608908 
print(solve('input.txt', True)) # 101726882250942

