
DIGIT_PAD = [
    ['7','8','9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [None, '0', 'A']
]
DIRECTIONAL_PAD = [
    [None,'^','A'],
    ['<', 'v', '>']
]
def solve(file : str, it=2) -> int :
    combinaisons : list[str] = []
    with open(file, 'r') as f :
        for line in f :
            combinaisons.append(line.strip())
    
    SYMBOL_TO_DIRECTIONS = {'>':(0,1), 'v':(1,0), '<':(0,-1), '^':(-1,0)}
    def get_a_few_valid_paths_hopefully_one_will_maybe_lead_to_the_right_answer(cur_symbol: str, target_symbol: str, pad) :
        rpad = {pad[r][c]: (r,c) for r in range(len(pad)) for c in range(len(pad[0]))}
        r, c = rpad[cur_symbol]
        r_target, c_target = rpad[target_symbol] 
        dr = r_target - r
        dc = c_target - c
        symbol_vertical = "^" if dr < 0 else "v" 
        symbol_horizontal = "<" if dc < 0 else ">"
        ans = []
        p1 = symbol_vertical * abs(dr) + symbol_horizontal * abs(dc) + "A"
        p2 = symbol_horizontal * abs(dc) + symbol_vertical * abs(dr) + "A"
        def is_valid_path(r, c, p) :
            for symbol in p[:-1] :
                dr, dc = SYMBOL_TO_DIRECTIONS[symbol]
                r, c = r + dr, c + dc
                if pad[r][c] == None :
                    return False
            return True
        if is_valid_path(r, c, p1) :
            ans.append(p1)
        if is_valid_path(r, c, p2) :
            ans.append(p2)
        return ans
    
    cache = {}
    def getMinLen(change:str, cur_depth:int) :
        if (change, cur_depth) in cache :
            return cache[(change, cur_depth)]
        paths_depthplus = []
        pad = DIGIT_PAD if cur_depth == 0 else DIRECTIONAL_PAD
        paths_depthplus = get_a_few_valid_paths_hopefully_one_will_maybe_lead_to_the_right_answer(change[0], change[1], pad)
        min_min_length = None  
        for p in paths_depthplus :
            min_length_for_p = helper(p, cur_depth+1)
            if min_min_length is None or min_min_length > min_length_for_p :
                min_min_length = min_length_for_p 
        cache[(change, cur_depth)] = min_min_length
        return min_min_length  
    
    def helper(path:str, cur_depth:int) :
        if cur_depth > it :
            return len(path)
        ans = 0
        path = 'A' + path
        for i in range(len(path)-1) :
            ans += getMinLen(path[i:i+2], cur_depth)
        return ans
    
    return sum((helper('A' + combinaison, 0)-1) * int(combinaison[:-1]) for combinaison in combinaisons)

print(solve('example.txt', it=2)) # 126384
print(solve('input.txt', it=2)) # 128962
print(solve('input.txt', it=19)) # 673831729488
print(solve('input.txt', it=20)) # 1676242092046
print(solve('input.txt', it=21)) # 4169862782078
print(solve('input.txt', it=22)) # 10373054975052
print(solve('input.txt', it=23)) # 25804283056352
print(solve('input.txt', it=24)) # 64191383208792 
print(solve('input.txt', it=25)) # 159684145150108 => answer for part 2
