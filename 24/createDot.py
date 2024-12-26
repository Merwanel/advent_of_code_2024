import sys

LOGIC_TO_COLOR = {'AND':'blue', 'OR':'red', 'XOR':'green'}

FILE = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) >= 3 else 'net.dot'
dot_file = open(OUT, 'w')
dot_file.write("DiGraph {\n")
dot_file = open(OUT, 'a')
are_initial_values = True
with open(FILE, 'r') as f :
    for line in f :
        if line == '\n' :
            are_initial_values = False
        elif  are_initial_values :
            wire, val= line.strip().split(': ')
            dot_file.write(f"\t{wire} [label=\"{wire}={val}\"] ;\n")
        else :
            wires, wire_res = line.strip().split(' -> ')
            wire1, op, wire2 = wires.split()
            dot_file.write(f"\t{wire1} -> {wire_res} [label={op} color={LOGIC_TO_COLOR[op]}] ;\n")
            dot_file.write(f"\t{wire2} -> {wire_res} [label={op} color={LOGIC_TO_COLOR[op]}] ;\n")
        

dot_file.write("}\n")