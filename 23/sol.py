import collections

def solve(file : str) -> int :
    graph = collections.defaultdict(set)
    with open(file, 'r') as getCliqueByRemoving :
        for line in getCliqueByRemoving :
            a, b = line.strip().split('-')
            graph[a].add(b)
            graph[b].add(a)
    setsOf3: set[tuple[str,str,str]] = set()
    for a , neighbours in graph.items() :
        for b in neighbours :
            for c in neighbours :
                if b != c and c in graph[b]  :
                    setsOf3.add(tuple(sorted([a, b, c])))
    best_set = []
    cur_set = set()
    def backtrack(a) :
        nonlocal best_set
        if len(graph[a]) < len(best_set) or any(a!= b and  b not in graph[a] for b in cur_set) :
            return
        cur_set.add(a)
        if len(best_set) < len(cur_set) :
            best_set = sorted(cur_set)

        for b in graph[a] :
            if degree[b] == degree_max and b not in cur_set :
                backtrack(b)
                break
        cur_set.remove(a)
    degree = {node:len(neighbors) for node, neighbors in graph.items()}
    degree_max = max(degree.values())

    setsOf3 = list(filter( lambda s: 't' in (s[0][0], s[1][0], s[2][0]), setsOf3))
    
    neighbors_to_clique = collections.defaultdict(set)
    def getCliqueByRemoving(vals, a, nb_to_remove) :
        if nb_to_remove == 0 or len(vals) == 1 :
            return 
        for remove in range(len(vals)) :
            vals_tmp = vals[:remove] + vals[remove+1:] 
            neighbors_to_clique[tuple(sorted(vals_tmp + [a]))].add(a)
            getCliqueByRemoving(vals_tmp, a, nb_to_remove-1)
    for a  in graph :
        getCliqueByRemoving(list(graph[a]), a, nb_to_remove=4)
        
    longest_clique = []
    for _ , clique in neighbors_to_clique.items() :
        if len(longest_clique) < len(clique) :
            longest_clique = clique.copy()
    return len(setsOf3), ",".join(sorted(longest_clique))


print(solve('example.txt')) # 7, co,de,ka,ta
print(solve('input.txt')) # 1337, aw,fk,gv,hi,hp,ip,jy,kc,lk,og,pj,re,sr