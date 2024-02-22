def hamming(string01, string02):
    if len(string01) != len(string02):
        print("Error:Using Edit distance")
    return sum(s1 != s2 for s1, s2 in zip(string01, string02))

with open ('bioinfo2/rosalind_hamm.txt', 'r') as f:
    string01 = f.readline().strip()
    string02 = f.readline().strip()
    
result = hamming(string01, string02)
print(result)
