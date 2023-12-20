
### most frequent k-mer in a string

def findpattern(string,kmer):
    
    pattern_dict = {}       # for making dictionary that can check the repeated patterns
    
    for i in range(len(string)-kmer+1):
        pattern = string[i:i+kmer]
        if pattern in pattern_dict:
            pattern_dict[pattern] += 1
        else:
            pattern_dict[pattern] = 1
    
    maximum = max(pattern_dict.values())
    target = [pattern for pattern, count in pattern_dict.items() if count == maximum]
    return target

with open("bioinfo2/rosalind_ba1b.txt", "r") as file:
    string = file.readline().strip()
    kmer = int(file.readline().strip())
    
result = findpattern(string,kmer)
print(" ".join(sorted(result)))