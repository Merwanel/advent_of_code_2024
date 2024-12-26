import collections
import sys
sys.setrecursionlimit(100_000)


def solve(file : str) -> tuple[int, int] :
    values : dict[str, bool] = {}
    zwires = []
    xwires = []
    ywires = []
    operations_waiting : list[tuple[str,str,str,str]] = []
    operations_ready : list[tuple[str,str,str,str]] = []
    deg_in = collections.defaultdict(int)
    wire_before = collections.defaultdict(list)
    are_initial_values = True
    with open(file, 'r') as f :
        for line in f :
            if line == '\n' :
                are_initial_values = False
            elif  are_initial_values :
                wire, val= line.strip().split(': ')
                values[wire] = val == '1'
                if wire[0] == 'z' :
                    zwires.append(wire)
                if wire[0] == 'x' :
                    xwires.append(wire)
                if wire[0] == 'y' :
                    ywires.append(wire)
            else :
                wires, wire_res = line.strip().split(' -> ')
                if wire_res[0] == 'z' :
                    zwires.append(wire_res)
                wire1, op, wire2 = wires.split()
                if wire1 in values and wire2 in values :
                    operations_ready.append((wire1, op, wire2, wire_res))
                else :
                    operations_waiting.append((wire1, op, wire2, wire_res))
                wire_before[wire1].append(wire_res)
                wire_before[wire2].append(wire_res)
                deg_in[wire_res] += 2
                
    zwires = sorted(set(zwires))
    xwires = sorted(set(xwires))
    ywires = sorted(set(ywires))
    while operations_ready or operations_waiting :
        while operations_ready :
            res = True
            wire1, op, wire2, wire_res = operations_ready.pop()
            if op == 'AND' :
                res = values[wire1] and values[wire2]
            if op == 'OR' :
                res = values[wire1] or values[wire2]
            if op == 'XOR' :
                res = values[wire1] ^ values[wire2]
            values[wire_res] = res
            deg_in[wire_res] -= 2
        for i in range(len(operations_waiting)-1, -1, -1):
            if deg_in[operations_waiting[i][0]] == deg_in[operations_waiting[i][2]] == 0 :
                operations_ready.append(operations_waiting.pop(i))
            
            
    def get_value(wires) :
        res = 0
        for bit, z in enumerate(wires) :
            if values[z] :
                res |= (1 << bit)
        return res
    
    z_val = get_value(zwires)
    x_val = get_value(xwires)
    y_val = get_value(ywires)
    z_val_expected = x_val + y_val
    diffs = []
    for i , (a,b) in enumerate(zip(reversed(bin(z_val)), reversed(bin(z_val_expected)))) :
        if a != b :
            diffs.append(i)
    return (z_val, z_val_expected), diffs

########################
# part 1
########################
print(solve('example_small.txt')) # 4
print(solve('example.txt')) # 2024
print(solve('input.txt')) # 59619940979346


########################
# part 2 by hand with graphviz
########################

# python3 createDot.py input.txt net1.dot
# fdp -Tsvg net1.dot > output1.svg
    # => there is a repeated pattern, some are weird
    # swap: z31 mfm
    

print(solve('input_modif1.txt')) # ((59617793495698, 59342915586642), [6, 7, 11, 12, 38, 39, 40, 41])
#  python3 createDot.py input_modif1.txt net2.dot
#  fdp -Tsvg net2.dot > output2.svg
    # swap: z06 fkp



print(solve('input_modif2.txt')) # ((59617793495634, 59342915586642), [11, 12, 38, 39, 40, 41])
#  python3 createDot.py input_modif2.txt net3.dot
#  dot -Tsvg net3.dot > output3.svg
    # swap: z11 ngr
    
print(solve('input_modif3.txt')) # ((59617793493586, 59342915586642), [38, 39, 40, 41])
#  python3 createDot.py input_modif3.txt net4.dot
#  dot -Tsvg net4.dot > output4.svg
    # swap: krj bpt
    
print(solve('input_modif4.txt')) # ((59342915586642, 59342915586642), [])

# answer => bpt,fkp,krj,mfm,ngr,z06,z11,z31