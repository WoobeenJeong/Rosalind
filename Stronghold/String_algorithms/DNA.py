### dictionary로 A,T,G,C count

seq = open("bioinfo2/rosalind_dna.txt",'r').read()
count = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    
for base in seq:
    if base in count:
        count[base] += 1

result = " ".join([f"{count}" for base, count in sorted(count.items())])

print(result)
