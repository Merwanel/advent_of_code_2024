import collections
from typing import List
    
def solve(file : str) -> tuple[int, int] :
    dependsOn = collections.defaultdict(list)
    before = collections.defaultdict(list)
    part1, part2 = 0, 0
    with open(file, 'r') as f :
        for line in f :
            if line == '\n' :
                break
            a, b = line.split('|')
            dependsOn[b.strip()].append(a)
            before[a].append(b.strip())
        for line in f :
            good, nogood = getMiddle(dependsOn, before, line)
            part1 += good
            part2 += nogood 
    return part1, part2

def getMiddle(dependsOn: collections.defaultdict[str, list], before: collections.defaultdict[str, list], line: str) -> tuple[int, int] :
    forbidden = set()
    updates = [update.strip() for update in line.split(',')]
    for update in updates :
        if update in forbidden :
            return 0 , reorder(before, updates)
        for dependance in dependsOn[update] :
            forbidden.add(dependance)
    return int(updates[len(updates) // 2]), 0

def reorder(before: collections.defaultdict[str, list], updates: List[str]) -> int :
    cur_dependsOn = collections.defaultdict(list)
    updates = set(updates)
    source = updates.copy()
    nb_degree_in = collections.defaultdict(int)
    for update in updates :
        for before_node in before[update] :
            if before_node in updates :
                cur_dependsOn[update].append(before_node)
                nb_degree_in[before_node] += 1
                if before_node in source :
                    source.remove(before_node)
    path = []
    def dfs(update) :
        path.append(update)
        for next_update in before[update] :
            nb_degree_in[next_update] -= 1
            if nb_degree_in[next_update] == 0 :
                dfs(next_update)
    
    for update in source :
        dfs(update) 
    return int(path[len(path) // 2])
    


print(solve('example.txt')) # (143, 123)
print(solve('input.txt')) # (4766, 6257)