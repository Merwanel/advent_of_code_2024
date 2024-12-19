import functools


def solve(file : str) -> int :
    patterns: set[str] = []
    nb_valid = 0
    nb_ways = 0
    with open(file, 'r') as f :
        line = next(f)
        patterns = set(line.strip().split(', '))
        for line in f :
            if line == '\n' :
                continue
            design = line.strip()
            
            @functools.cache
            def nb_ways_design_valid(i: int=0) :
                if i == len(design) :
                    return 1
                
                nb_ways = 0
                for j in range(i, len(design)) :
                    if design[i:j+1] in patterns :
                        nb_ways += nb_ways_design_valid(j+1)
                return nb_ways
            
            nb_ways_this_design = nb_ways_design_valid()
            
            nb_ways += nb_ways_this_design
            nb_valid +=  nb_ways_this_design > 0
    return nb_valid, nb_ways



######
#    part 1
#####
print(solve('example.txt')) # 6, 16
print(solve('input.txt')) # 240, 848076019766013
