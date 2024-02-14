### reverse complement dna
### 5'->3' into 3'->5'

def complement(dna):
    dna = dna.replace('A', 't').replace('C', 'g').replace('G', 'C').replace('T', 'A').replace('t', 'T').replace('g', 'G')
    return dna[::-1]


with open ('REVC.txt', 'r') as file:
    dna = file.readline().strip()

print(complement(dna))
