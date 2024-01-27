

###############################################################################################
### 이번엔 단순하게가 아니라 Middle egde와 Middle node를 통해 align하기


import numpy as np

def linear_space_alignment(vstr, wstr, sigma):
    n = len(vstr)
    m = len(wstr)

    upper = np.zeros(m + 1, dtype=int)
    lower = np.zeros(m + 1, dtype=int)
    middle_edge = np.empty((n, m), dtype=str)

    for j in range(1, m + 1):
        upper[j] = upper[j - 1] - sigma
        # print(upper)

    for i in range(1, n + 1):
        lower[0] = upper[0] - sigma
        # print(lower)

        for j in range(1, m + 1):
            match = upper[j - 1] + BLOSUM62[vstr[i - 1]][wstr[j - 1]]
            delete = upper[j] - sigma
            insert = lower[j - 1] - sigma

            upper[j - 1] = max(match, delete, insert)

            lower[j] = max(match, upper[j] - sigma, lower[j - 1] - sigma)

            if upper[j - 1] >= delete and upper[j - 1] >= insert:
                middle_edge[i - 1, j - 1] = 'D'
            elif delete >= insert:
                middle_edge[i - 1, j - 1] = 'U'
            else:
                middle_edge[i - 1, j - 1] = 'L'

        upper, lower = lower, upper

    # print(f"{upper}\n{lower}\n{middle_edge}")
    
    i, j = n - 1, m - 1
    v_match, w_match = [], []

    while i >= 0 or j >= 0:
        if i >= 0 and j >= 0:
            if middle_edge[i, j] == 'D':
                v_match.append(vstr[i])
                w_match.append(wstr[j])
                i -= 1
                j -= 1
            elif middle_edge[i, j] == 'U':
                v_match.append(vstr[i])
                w_match.append('-')
                i -= 1
            else:
                v_match.append('-')
                w_match.append(wstr[j])
                j -= 1
        elif i >= 0:
            v_match.append(vstr[i])
            w_match.append('-')
            i -= 1
        else:
            v_match.append('-')
            w_match.append(wstr[j])
            j -= 1

    return upper[m], ''.join(v_match[::-1]), ''.join(w_match[::-1])

with open ("bioinfo2/rosalind_ba5l.txt", "r") as f:
    seqs = f.readlines()
    vstr = seqs[0].strip()
    wstr = seqs[1].strip()

with open ("bioinfo2/BLOSUM62.txt", "r") as f:
    BLOSUM62 = f.readlines()
    BLOSUM62 = [line.strip().split() for line in BLOSUM62]
    BLOSUM62 = {line[0]:{BLOSUM62[0][i]:int(line[i+1]) for i in range(len(BLOSUM62[0]))} for line in BLOSUM62[1:]}

# print(vstr, wstr)
# print(BLOSUM62)

score, v_match, w_match = linear_space_alignment(vstr, wstr, sigma=5)
print(score)
print(v_match)
print(w_match)
