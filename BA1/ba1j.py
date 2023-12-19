
### find most freq kmer with mismatch and reverse
### ba1c.py + ba1i.py
### shortest version code

def reverse_complement(string):
    seq_dict = {"A":"T","T":"A","G":"C","C":"G"}
    return "".join([seq_dict[nt] for nt in string[::-1]])

def hamming(string01, string02):
    if len(string01) != len(string02):
        print("Error:Using Edit distance")
    return sum(s1 != s2 for s1, s2 in zip(string01, string02))

def most_freq(string, k, d):
    
    reverse = reverse_complement(string)
    
    ### all possible patterns
    pattern_dict = {}
    nt = ["A","C","G","T"]
    patterns = [''.join(nt[(i//(4**j))%4] for j in range(k)) for i in range(4**k)]
    pattern_dict = {pattern: 0 for pattern in patterns}
    
    ### count patterns occurances with mismatch on forward and reverse
    for pattern in pattern_dict.keys():
        pattern_dict[pattern] = sum(1 for i in range(len(string) - k + 1) if hamming(pattern, string[i:i + k]) <= d)
        pattern_dict[pattern] += sum(1 for i in range(len(reverse) - k + 1) if hamming(pattern, reverse[i:i + k]) <= d)

    ### find patterns with maximum occurance (두개 이상일 수도 있음)
    max_count = max(pattern_dict.values())
    max_pattern = [k for k,v in pattern_dict.items() if v == max_count]

    return max_pattern

with open("bioinfo2/rosalind_ba1j.txt","r") as f:
    string = f.readline().strip()
    k,d = f.readline().strip().split(" ")
    k,d = int(k),int(d)
    
# print(string,k,d)

result = most_freq(string,k,d)
print(" ".join(result))
