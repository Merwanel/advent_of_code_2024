from typing import List

def solve(file : str) -> tuple[int,int] :
    compressed = ''
    with open(file, 'r') as f :
        for line in f :
            compressed = [int(n) for n in line.strip()]
            
    decompressed :  list[int|str] = []
    cur_id = 0
    for i in range(0, len(compressed) , 2) :
        decompressed.extend([cur_id] * compressed[i])
        if i+1 < len(compressed) :
            decompressed.extend(['.'] * compressed[i+1])
        
        cur_id += 1
    def compact_and_checksum1(decompressed: list[int|str]) -> int :
        left = 0
        right = len(decompressed) - 1
        while left < right :
            while left < right and decompressed[left] != '.' :
                left += 1
            while left < right and decompressed[right] == '.' :
                right -= 1
            decompressed[left], decompressed[right] = decompressed[right], decompressed[left]
        checksum = sum(i * decompressed[i]  for i in range(right))
        return checksum
    def compact_and_checksum2(decompressed: list[int|str], cur_id: int) -> int :
        end_block = len(decompressed) - 1
        start_block = end_block + 1
        while end_block >= 0 and cur_id >= 0  :
            end_block = start_block - 1
            while end_block >= 0 and decompressed[end_block] != cur_id:
                end_block -= 1
            start_block = end_block
            while start_block > 0 and decompressed[start_block-1] == cur_id :
                start_block -= 1
            block_size = end_block - start_block + 1
            start_free, end_free = 0, -1
            while start_free < start_block and end_free - start_free + 1 < block_size  :
                start_free = end_free + 1
                while start_free < start_block and decompressed[start_free] != '.' :
                    start_free += 1
                end_free = start_free
                while end_free +1 < start_block and decompressed[end_free+1] == '.' :
                    end_free += 1
            if start_free < start_block  and  end_free - start_free + 1 >= block_size  :
                decompressed[start_free:start_free + block_size] = [cur_id] * block_size
                decompressed[start_block:end_block+1] = ['.'] * block_size
            cur_id -= 1
        checksum = sum(i * decompressed[i] if decompressed[i] != '.' else 0 for i in range(len(decompressed)))
        return checksum
    return compact_and_checksum1(decompressed.copy()), compact_and_checksum2(decompressed.copy(), cur_id - 1)



print(solve('example.txt')) # 1928, 2858
print(solve('input.txt')) # 6367087064415, 6390781891880