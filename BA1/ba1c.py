
### making reverse complement of a DNA sequence

def reverse_complement(seq):
    seq = seq[::-1]
    seq = seq.replace('A','t')
    seq = seq.replace('T','a')
    seq = seq.replace('C','g')
    seq = seq.replace('G','c')
    seq = seq.upper()
    return seq

with open ('bioinfo2/rosalind_ba1c.txt','r') as input:
    seq = input.read().replace('\n','')
    
print(reverse_complement(seq))
