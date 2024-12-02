from typing import List


def is_safe(report: List[int], tolerance: int) -> bool :
    nb_inc = int(report[0] < report[1] ) + int(report[1] < report[2] ) + int(report[2] < report[3] )
    is_increasing = nb_inc >= 2
    for i in range(len(report)-1) :
        if (report[i] < report[i+1]) != is_increasing or not (1 <= abs(report[i] - report[i+1]) <= 3) :
            
            if tolerance > 0 :
                removed_ith = report[:i] + report[i+1:]
                removed_iplus1th = report[:i+1] + report[i+2:]
                return is_safe(removed_ith, tolerance=0) or is_safe(removed_iplus1th, tolerance=0)
            
            return False
    return True

def solve(file: str, tolerance: int) -> int :
    ans = 0
    with open(file, 'r') as f :
        for line in f :
            report = [ int(level) for level in line.split()]
            ans += is_safe(report, tolerance)
    return ans
            
    

print(solve('example.txt', tolerance=0))         
print(solve('input.txt', tolerance=0))     
print(solve('example.txt', tolerance=1))         
print(solve('input.txt', tolerance=1))        