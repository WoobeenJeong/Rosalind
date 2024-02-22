### motif finding : Exact matching

### dna = AAA-GGA-AAA
### mofif =   GGA      = substring s[j:k] = s[4:6]      

####################################

def motif_find(dna, motif):
    result = []
    for i in range(len(dna)):
        if dna[i:i+len(motif)] == motif:
            result.append(i+1)
    return result

#####################################
### 엄청 긴 서열에서 효율적으로 찾아내기 위해
### KMP 알고리즘을 사용할 수도 있음
### KMP = Knuth-Morris-Pratt algorithm

def kmp_search(dna, motif):
    result = []
    n = len(dna)
    m = len(motif)
    pi = [0] * m
    j = 0

    for i in range(1, m):
        while j > 0 and motif[i] != motif[j]:
            j = pi[j-1]
        if motif[i] == motif[j]:
            j += 1
            pi[i] = j

    j = 0
    for i in range(n):
        while j > 0 and dna[i] != motif[j]:
            j = pi[j-1]
        if dna[i] == motif[j]:
            if j == m - 1:
                result.append(i - m + 2)
                j = pi[j] 
            else:
                j += 1

    return result

#####################################

with open('bioinfo2/rosalind_subs.txt', 'r') as f:
    dna = f.readline().strip()
    motif = f.readline().strip()
    
# result = motif_find(dna, motif)
result02 = kmp_search(dna, motif)

for each in result02:
    print(each, end=' ')
