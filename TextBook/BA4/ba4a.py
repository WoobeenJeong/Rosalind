### RNA into A.A. sequence
### 3 bp 단위로 쪼개서 codon table에서 바꾸기
### codon table도 정리하면 좋을 것임

#####################################################
### 효과적으로 codon table을 만들기

base = ['A','C','G','U']
codon = [a+b+c for a in base for b in base for c in base]
aminoacid = 'KNKNTTTTRSRSIIMIQHQHPPPPRRRRLLLLEDEDAAAAGGGGVVVV*Y*YSSSS*CWCLFLF'
codon_table = dict(zip(codon, aminoacid))
# print(codon_table)

#####################################################
### shorter version

def short_translation(rna):
    ptn = ''.join([codon_table[rna[i:i+3]] for i in range(0, len(rna), 3)])
    if ptn[-1] == '*':
        ptn = ptn[:-1]
    else:
        "no stop codon found in the end of the sequence."
    return ptn

#####################################################

def translation(rna):
    ptn = ''
    i=0
    codon = rna[i:i+3]
    
    while codon:
        ptn += codon_table[codon]
        i += 3
        codon = rna[i:i+3]
        if i == len(rna):
            break
    
    if ptn[-1] == '*':
        ptn = ptn[:-1]
    else:
        "no stop codon found in the end of the sequence."
        
    return ptn

#####################################################

with open('bioinfo2/rosalind_ba4a.txt') as file:
    rna = file.read().strip()


short_result = short_translation(rna)
result = translation(rna)

# print(short_result)
print(result)
