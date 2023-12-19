
### frequency array
### 이전에 ba1i ~ ba1j 에서 쓴 pattern dict랑 동일

def kmer_freq(string,k):
    
    nt = ["A","C","G","T"]
    patterns = [''.join(nt[(i//(4**j))%4] for j in range(k)) for i in range(4**k)]
    pattern_dict = {pattern: 0 for pattern in patterns}
    
    ### alphabetically ordered patterns
    pattern_dict = dict(sorted(pattern_dict.items()))
    
    ### count
    for i in range(len(string) - k + 1):
        pattern_dict[string[i:i + k]] += 1
    
    return pattern_dict


with open("bioinfo2/rosalind_ba1k.txt","r") as f:
    
    string = f.readline().strip()
    k = int(f.readline().strip())
    
# print(string,k)

result = kmer_freq(string,k)
# print(*result.values())
print(*result.values(),sep=" ")

##################################################
output_file_path = "ba1k_output.txt"

with open(output_file_path, "w") as output_file:
    output_file.write(" ".join(map(str, result.values())))
print(f"Results saved to {output_file_path}")