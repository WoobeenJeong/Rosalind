
### (L,t)-clump in string
### L = length of loci we are looking for
### t = times of occurence

def forming_clump(string, k, L, t):
    clumps = []
    for i in range(len(string)-L+1):
        window = string[i:i+L]
        for j in range(len(window)-k+1):
            kmer = window[j:j+k]
            if window.count(kmer) >= t:
                if kmer not in clumps:
                    clumps.append(kmer)            
                    
    # return set(clumps)
    return clumps

with open ("bioinfo2/rosalind_ba1e.txt", "r") as file: 
    lines = file.readlines()
    string = lines[0].strip()
    k, L, t = lines[1].strip().split(" ")

# print(string, k, L, t)
    
clump = forming_clump(string, int(k), int(L), int(t))

print(" ".join(clump))
