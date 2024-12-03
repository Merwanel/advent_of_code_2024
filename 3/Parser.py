from io import TextIOWrapper

class Parser :
    def __init__(self, is_part1:bool, f: TextIOWrapper):
        self.i = 0
        self.f = f
        self.ans = 0
        self.last_was_do = True
        self.is_part1 = is_part1
        
    def parseIt(self) -> int :
        for line in self.f:
            self.i = 0
            self.parseLine(line)
        return self.ans
    
    def parseLine(self, line: str) -> int :
        while self.i < len(line) :
            if ( self.is_part1 or self.last_was_do ) and line[self.i] == "m" and line[self.i:self.i+4] == "mul(" :
                self.mul(line)
            elif line[self.i] == "d" :
                if line[self.i:self.i+7] == "don't()" :
                    self.last_was_do = False
                    self.i += 7
                elif line[self.i:self.i+4] == "do()" :
                    self.last_was_do = True
                    self.i += 4
                else :
                    self.i += 1
            else :
                self.i += 1
                
    def getInt(self, line: str) -> int :
        n = 0
        line[self.i].isdigit
        while self.i < len(line) and line[self.i].isdigit() :
            n *= 10
            n += int(line[self.i])
            self.i += 1
        
        return n
    
    def match(self, line: str, f: callable) :
        return self.i < len(line) and f(line[self.i])
    
    def mul(self, line: str) :
        self.i += 4  # consume mult(
        if not self.match(line, lambda c : c.isdigit()) :
            return
        a = self.getInt(line)
        if not self.match(line, lambda c : c == ',') :
            return
        self.i += 1
        if not self.match(line, lambda c : c.isdigit()) :
            return
        b = self.getInt(line)
        if not self.match(line, lambda c : c == ')') :
            return
        self.i += 1
        self.ans += a * b