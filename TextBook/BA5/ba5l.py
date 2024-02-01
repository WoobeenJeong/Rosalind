### 이번엔 middle edge 찾기를 반복해서 divide and conquer
### 전체 local alignment를 찾기
### 기존 ba5k 활용

import time
import numpy as np

with open('bioinfo2/BLOSUM62.txt', 'r') as file:
    lines = file.readlines()
    blosum62 = []
    aa = lines[0].strip().split()[0:]
    for line in lines[1:]:
        row = [int(x) for x in line.strip().split()[1:]]
        blosum62.append(row)
    
def scoring(ref, alt, indel):
    before = np.zeros((len(ref) + 1), dtype=np.int64)
    after = np.arange(0, -indel * (len(ref) + 1), -indel, dtype=np.int64)
    backtrack = np.zeros((len(ref) + 1), dtype=np.int8)

    for i, inext in enumerate(alt, 1):                                          
        before, after = after, before
        after[0] = -indel * i
        for j, jnext in enumerate(ref, 1):
            match = before[j - 1] + blosum62[aa.index(jnext)][aa.index(inext)]
            insertion = after[j - 1] - indel
            deletion = before[j] - indel
            after[j] = max(match, insertion, deletion)

            if after[j] == match:
                backtrack[j] = 2
            elif after[j] == insertion:
                backtrack[j] = 1
            else:
                backtrack[j] = 0

    return after, backtrack

def middle_edge(ref, alt, indel):
    midpoint = len(alt) // 2
    
    source2m, _ = scoring(ref, alt[:midpoint], indel)
    m2sink, traceback = scoring(ref[::-1], alt[midpoint:][::-1], indel)
    total = source2m + m2sink[::-1]

    i = np.argmax(total)
    j = midpoint
    
    addscore = traceback[::-1][i]
    
    if addscore == 0:
        k = i
        l = j + 1
    elif addscore == 1:
        k = i + 1
        l = j
    elif addscore == 2:
        k = i + 1
        l = j + 1

    return (i, j), (k, l)

############################################################################

def alignment(top, bottom, left, right, ref, alt, indel):
    if left == right:
        return [(i, left) for i in range(top, bottom + 1)]
    if top == bottom:
        return [(top, j) for j in range(left, right + 1)]

    partial_ref = ref[top:bottom]
    partial_alt = alt[left:right]
    (mi, mj), (mk, ml) = middle_edge(partial_ref, partial_alt, indel)
    mi += top; mk += top
    mj += left; ml += left
    # print(partial_ref, partial_alt, mi, mj, mk, ml)
    
    source2mid = alignment(top, mi, left, mj, ref, alt, indel)
    mid2sink = alignment(mk, bottom, ml, right, ref, alt,indel)
    # print(source2mid, mid2sink)
    
    return source2mid + mid2sink

def traceback(ref, alt, path, indel):
    alignref = []
    alignalt = []
    score = 0
    for (i, j), (k, l) in zip(path, path[1:]):
        alignref.append(ref[i] if i < k else '-')
        alignalt.append(alt[j] if j < l else '-')
        if i < k and j < l:
            score += + blosum62[aa.index(ref[i])][aa.index(alt[j])]
        else:
            score -= indel

    return score, ''.join(alignref), ''.join(alignalt)

############################################################################
### 문제는 서열이 매우 길어서 오래 걸림

with open('bioinfo2/rosalind_ba5l.txt', 'r') as file:
    lines = file.readlines()
    ref = lines[0].strip().split()[0]
    alt = lines[1].strip().split()[0]
    
    indel = 5

start_time = time.time()

path = alignment(0, len(ref), 0, len(alt), ref, alt, 5)
score, alignref, alignalt = traceback(ref, alt, path, indel)

end_time = time.time()
elapsed_time = (end_time - start_time)/60

print(score, alignref, alignalt, sep='\n')
print(f"Elapsed Time: {round(elapsed_time,3)} min")

### Elapsed Time: 5.797 min
