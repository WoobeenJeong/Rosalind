### ba4a.py 와 동일

base = ['A','C','G','U']
codon = [a+b+c for a in base for b in base for c in base]
aminoacid = 'KNKNTTTTRSRSIIMIQHQHPPPPRRRRLLLLEDEDAAAAGGGGVVVV*Y*YSSSS*CWCLFLF'
codon_table = dict(zip(codon, aminoacid))

#####################################################

def translation(rna):
    ptn = ''.join([codon_table[rna[i:i+3]] for i in range(0, len(rna), 3)])
    if ptn[-1] == '*':
        ptn = ptn[:-1]
    else:
        "no stop codon found in the end of the sequence."
    return ptn

#####################################################

with open('bioinfo2/rosalind_prot.txt') as file:
    rna = file.read().strip()

result = translation(rna)

print(result)
