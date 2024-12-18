from typing import Literal

class Computer() :
    def __init__(self, A: int, B: int, C: int, instructions: list[int], part2:bool=False):
        self.A = A
        self.B = B
        self.C = C
        self.instructions = instructions
        self.instruction_pointer = 0
        self.output: list[str] = []
        self.part2 = part2
        
    def combo(self, operand: int) -> int :
        if 0 <= operand <= 3 :
            return operand
        if operand == 4 :
            return self.A
        if operand == 5 :
            return self.B
        if operand == 6 :
            return self.C
        raise Exception('invalid operand ', operand, 'at instruction ', self.instruction_pointer-2 )
    
    def run(self, print_register:bool=False) -> str :
        while self.instruction_pointer < len(self.instructions) :
            opcode, operand = self.instructions[self.instruction_pointer], self.instructions[self.instruction_pointer+1]
            
            if opcode == 0 :
                self.adv(operand)
            if opcode == 1 :
                self.bxl(operand)
            if opcode == 2 :
                self.bst(operand)
            if opcode == 3 :
                self.jnz(operand)
            if opcode == 4 :
                self.bxc()
            if opcode == 5 :
                self.output.append(self.out(operand))
                if self.part2 and self.output[-1] != str(self.instructions[len(self.output)-1]):
                    break
            if opcode == 6 :
                self.bdv(operand)
            if opcode == 7 :
                self.cdv(operand)
        if print_register :
            print(f"A={self.A}, B={self.B}, C={self.C}")
        return ",".join(self.output)
    

    def adv(self, operand: int) -> None :
        self.instruction_pointer += 2
        self.A = self.A // (2 ** self.combo(operand))
        
    def bxl(self, operand: int) -> None :
        self.instruction_pointer += 2
        self.B = self.B ^ operand

    def bst(self, operand: int) -> None :
        self.instruction_pointer += 2
        self.B = self.combo(operand) % 8

    def jnz(self, operand: int) -> None :
        if self.A == 0 :
            self.instruction_pointer += 2
        else :
            self.instruction_pointer = operand
                
    def bxc(self) -> None :
        self.instruction_pointer += 2
        self.B = self.B ^ self.C
    
    def out(self, operand: int) -> str :
        self.instruction_pointer += 2
        return str(self.combo(operand) % 8)
    
    def bdv(self, operand: int) -> None :
        self.instruction_pointer += 2
        self.B = self.A // (2 ** self.combo(operand))
        
    def cdv(self, operand: int) -> None :
        self.instruction_pointer += 2
        self.C = self.A // (2 ** self.combo(operand))
    

def solve(file : str, print_register:bool=False) -> tuple[int, int] :
    program : list[str] = []
    with open(file, 'r') as f :
        for line in f :
            program.append(line.strip())
    A = int(program[0].split()[-1])
    B = int(program[1].split()[-1])
    C = int(program[2].split()[-1])
    
    instructions = [int(n) for n in program[4].split()[-1].split(',')]

    return  Computer(A,B,C, instructions).run(print_register)

########################################################
################    Part 1   ###########################
########################################################
print(Computer(0,0,9, [2,6]).run(print_register=True)) # B == 1
print(Computer(0,29,0, [1,7]).run(print_register=True)) # B == 26
print(Computer(0,2024,43690, [4,0]).run(print_register=True)) # B == 44354
print(solve('example1.txt')) # 0,1,2
print(solve('example2.txt', print_register=True)) # 4,2,5,6,7,7,7,7,3,1,0    A == 0 
print(solve('example3.txt')) # 4,6,3,5,6,3,5,2,1,0
print(solve('input.txt')) # 5,0,3,5,7,6,1,5,4
print(Computer(117440,0,0, [0,3,5,4,3,0]).run()) # 0,3,5,4,3,0
print(Computer(164516454365621,0,0, [2,4,1,1,7,5,1,5,0,3,4,4,5,5,3,0]).run()) # 
print(Computer(164534248369853,0,0, [2,4,1,1,7,5,1,5,0,3,4,4,5,5,3,0]).run()) #  


########################################################
################    Part 2   ###########################
########################################################

# 2,4,1,1,7,5,1,5,0,3,4,4,5,5,3,0
# what the program does :
    # 2,4 bst(4) B = A % 8
    # 1,1 bxl(1) B = B ^ 1
    # 7,5 cdv(5) C = A // (2 ** B)
    # 1,5 bxl(5) B = B ^ 5
    # 0,3 adv(3) A = A // (2 ** 3)
    # 4,4 bxc(4) B = B ^ C
    # 5,5 out(5) B % 8
    # 3,0 jnz(0) go back to instruction 0

    # B = (A % 8) ^ 1
    # C = A // (2 ** B)
    # A = A // (2 ** 3)
    # B = ((B ^ 5) ^ C) % 8 -> out
    # go back

    # in particular :
    # 2,4 bst(4) B = A % 8
    # 0,3 adv(3) A = A // (2 ** 3)
    # => for the 1st out , the first 3 bits counts the most
    # => for the 2nd out , 3 following bits  counts the most
    # => that until getting all the program back

print()
print()
instructions = [2,4,1,1,7,5,1,5,0,3,4,4,5,5,3,0]
instructions_str = list(map(str,instructions)) 

best = 0
for k in range(1_000_000) :
    A = k
    A = k * 8 ** 5 + 0o74665
    A = k * 8 ** 5 + 0o474665
    A = k * 8 ** 8 + 0o64474665
    A = k * 8 ** 13 + 0o2017064474665
    
    computer = Computer(A,0,0, instructions, part2=True)
    computer.run()
    
    if computer.output == instructions_str :
        print('hit', A)  # => 164516454365621
        break
    
    if best < len(computer.output) :
        best = len(computer.output) 
        print(oct(A), A, ",".join(computer.output), best)