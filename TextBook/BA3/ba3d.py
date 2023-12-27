### making de Bruijn graph from as (k-1)mer

### 지난번 ba3a.py, ba3c.py 응용
### sliding window는 이전처럼 = 1
### NP complete 문제니까, 당연히 Brute Force로, |Text| - k + 1

def kmer_lexical(k, string):
    kmers = []
    for i in range(len(string)-k+1):
        kmers.append(string[i:i+k])
    return sorted(kmers)

def DeBruijn_k(string,kmer):
    
    kmer_list = kmer_lexical(kmer, string)
    kmer_dict = {}

    # print(kmer_list)
    
    for kmer in kmer_list:
        if kmer[:-1] not in kmer_dict:
            kmer_dict[kmer[:-1]] = [kmer[1:]]
    ###     prefix를 key로       =  suffix를 value로          
        else:
            kmer_dict[kmer[:-1]].append(kmer[1:])
            
    return kmer_dict
    

with open ('bioinfo2/rosalind_ba3d.txt', 'r') as f:
    kmer = int(f.readline().strip())
    string = f.readline().strip()
    
result = DeBruijn_k(string, kmer)

#####################
### printing format

print('\n'.join([prefix + ' -> ' + ','.join(suffix) for prefix, suffix in result.items()]))

#####################
