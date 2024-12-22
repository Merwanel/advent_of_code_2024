import collections

cache = {}
def solve(file : str, it=2) -> int :
    secret_numbers : list[str] = []
    with open(file, 'r') as f :
        for line in f :
            secret_numbers.append(int(line.strip()))

    # To mix a value into the secret number, calculate the bitwise XOR of the given value and the secret number.
    # Then, the secret number becomes the result of that operation. (If the secret number is 42 and you were to mix 
    # 15 into the secret number, the secret number would become 37.)
    def mix(val, secret) :
        return val ^ secret

    # To prune the secret number, calculate the value of the secret number modulo 16777216. Then, the secret number 
    # becomes the result of that operation. (If the secret number is 100000000 and you were to prune the secret number,
    # the secret number would become 16113920.)
    def prune(secret) :
        return secret % 16777216
    
    def helper(secret) :
        # Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret number. Finally, prune the secret number.
        secret = mix(secret * 64, secret) 
        secret = prune(secret)
        # Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer. Then, mix this result into the secret number. Finally, prune the secret number.
        secret = mix(secret // 32 , secret) 
        secret = prune(secret)
        # Calculate the result of multiplying the secret number by 2048. Then, mix this result into the secret number. Finally, prune the secret number.
        secret = mix(secret * 2048, secret) 
        secret = prune(secret)
        return secret
    def get_price(secret) :
        return secret % 10
    
    bananas = collections.defaultdict(int)
    def get_ith(secret:int, it=2000) :
        if it < 5 :
            for _ in range(it) :
                secret=helper(secret)
            return secret
        prev_price = get_price(secret)
        prev4 = []
        for _ in range(4) :
            secret=helper(secret)
            prev4.append(get_price(secret) - prev_price)
            prev_price = get_price(secret)
        
        bananas_tmp = collections.defaultdict(int)
        bananas_tmp[tuple(prev4)] = get_price(secret)
        for _ in range(it-4) :
            secret=helper(secret)
            prev4.pop(0)
            prev4.append(get_price(secret) - prev_price)
            prev_price = get_price(secret)
            if tuple(prev4) not in bananas_tmp :
                bananas_tmp[tuple(prev4)] = get_price(secret)            
            
        # update bananas :        
        for changes4, cpt in bananas_tmp.items() :
            bananas[changes4] += cpt
        return secret
    s1= 0
    for initial in secret_numbers :
        s1 += get_ith(initial, it=it)
    return s1 , max(bananas.values()) if bananas else 0


print(solve('example_small.txt', it=1)) # 15887950
print(solve('example_small.txt', it=2)) # 16495136
print(solve('example_small.txt', it=3)) # 527345
print(solve('example_small.txt', it=4)) # 704524
print(solve('example_small.txt', it=5)) # 1553684
print(solve('example_small.txt', it=6)) # 12683156
print(solve('example_small.txt', it=7)) # 11100544
print(solve('example_small.txt', it=8)) # 12249484
print(solve('example_small.txt', it=9)) # 7753432, 6
print(solve('example_small.txt', it=10)) # 5908254, 6
print(solve('example.txt', it=2000)) # 37327623  24
print(solve('example2.txt', it=2000)) # 37990510  23
print(solve('input.txt', it=2000)) # 12979353889, 1449
