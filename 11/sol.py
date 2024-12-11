import collections

def solve(file : str, nb_blink: int) -> tuple[int,int] :
    stones = collections.defaultdict(int)
    with open(file, 'r') as f :
        for line in f :
            for n in line.strip().split() :
                stones[n] += 1 
    for k in range(nb_blink) :
        new_stones = collections.defaultdict(int)
        for stone, cpt in stones.items() :
            if stone == '0' :
                new_stones['1'] += cpt
            elif len(stone) % 2 == 0 :
                new_stones[stone[:len(stone) // 2]] += cpt
                new_stones[str(int(stone[len(stone) // 2:]))] += cpt  # new numbers don't keep extra leading zeroes
            else :
                new_stones[str(int(stone) * 2024)] += cpt  
                
        stones = new_stones      
    return sum(stones.values())



print(solve('example.txt', 1)) # 7
print(solve('example2.txt', 1)) # 3
print(solve('example2.txt', 2)) # 4
print(solve('example2.txt', 3)) # 5
print(solve('example2.txt', 4)) # 9
print(solve('example2.txt', 5)) # 13
print(solve('example2.txt', 6)) # 22
print(solve('example2.txt', 25)) # 55312
print(solve('input.txt', 25)) # 186996
print(solve('input.txt', 75)) # 221683913164898