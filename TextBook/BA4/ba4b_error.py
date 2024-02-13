### 이번엔 5'->3', 3'->5' ORF 6개에서 각각 동일한 translation 보이는 서열 찾기
### dna target ptn seq 주어짐
### codon table은 ba4a에서 가져옴

base = ['A','C','G','T']
codon = [a+b+c for a in base for b in base for c in base]
aminoacid = 'KNKNTTTTRSRSIIMIQHQHPPPPRRRRLLLLEDEDAAAAGGGGVVVV*Y*YSSSS*CWCLFLF'
codon_table = dict(zip(codon, aminoacid))

def translation(dna):
    if len(dna) % 3 == 0:
        margin = 0
        pass
    elif len(dna) % 3 == 1:
        dna = dna[:-1]
        margin = 1
    else:
        dna = dna[:-2]
        margin = 2
        
    rna = ''.join([codon_table[dna[i:i+3]] for i in range(0, len(dna), 3)])
    return rna, margin
    
#####################################################

def orfs(dna, substring):
    dict = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
    target = []
    
    f_minus = dna           # forward strand
    f_zero = dna[1:-2]
    f_plus = dna[2:-1]
    
    r_minus = ''.join([dict[base] for base in dna[::-1]])   # reverse strand
    r_zero = r_minus[1:-2]
    r_plus = r_minus[2:-1]
    # print((f_minus, r_minus))

    for seq, revseq in zip([f_minus, f_zero, f_plus], [r_minus, r_zero, r_plus]):
        ptn,_ = translation(seq)
        revptn, margin = translation(revseq)
        # print((ptn, seq), (revptn, revseq))
        pos = [i for i in range(len(ptn)) if ptn.startswith(substring, i)]
        target += [seq[3 * p: 3 * p + len(substring) * 3] for p in pos]
        
        revpos = [i for i in range(len(revptn)) if revptn.startswith(substring, i)]
        revpos = [len(revptn) - (p + len(substring)) for p in revpos]
        print(pos, revpos)
        
        if revseq == r_minus:
            target += [seq[3 * p + margin : 3 * p + len(substring) * 3 + margin] for p in revpos]
        elif revseq == r_zero:
            target += [seq[3 * p + 1 + margin : 3 * p + len(substring) * 3 + 1 + margin] for p in revpos]
        elif revseq == r_plus:
            target += [seq[3 * p + 2 + margin : 3 * p + len(substring) * 3 + 2 + margin] for p in revpos]
    
    return target

#####################################################

with open('bioinfo2/rosalind_ba4b.txt') as file:
    dna = file.readline().strip()
    substring = file.readline().strip()

result = orfs(dna, substring)
for i in result:
    print(i, sep='\n')

