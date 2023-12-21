### kmer with lexicographic order (lexical order)

def kmer(k, string):
    kmers = []
    for i in range(len(string)-k+1):
        kmers.append(string[i:i+k])
    return sorted(kmers)

with open("bioinfo2/rosalind_ba3a.txt","r") as f:
    k = int(f.readline().strip())
    string = f.readline().strip()
    
# print(k, string)

result = kmer(k, string)
print("\n".join(result))
