
### ba5e 활용

import numpy as np

with open('bioinfo2/BLOSUM62.txt', 'r') as file:
    lines = file.readlines()
    blosum62 = []
    aa = lines[0].strip().split()[0:]
    for line in lines[1:]:
        row = [int(x) for x in line.strip().split()[1:]]
        blosum62.append(row)

with open('bioinfo2/sample.txt', 'r') as file:
    lines = file.readlines()
    ref = lines[0].strip().split()[0]
    alt = lines[1].strip().split()[0]
    
def middle(aa, blosum62, ref, alt):
    indel = -5
    matrix = np.zeros((len(alt) + 1, len(ref) + 1))
    max_score = 0
    max_i, max_j = 0, 0
    for i in range(1, len(alt) + 1):
        for j in range(1, len(ref) + 1):
            matrix[i][j] = max(0,
                matrix[i - 1][j - 1] + blosum62[aa.index(alt[i - 1])][aa.index(ref[j - 1])],
                matrix[i - 1][j] + indel,
                matrix[i][j - 1] + indel
            )

    # print(len(alt), len(ref))
    # print(matrix)

    mid_i = len(alt) // 2 
    mid_matrix = np.array(matrix)[:, :len(ref) // 2 ]

    # print(mid_matrix)
    
    for i in range(len(alt) + 1):
        for j in range(mid_i + 1):
            if mid_matrix[i][j] > max_score:
                max_score = mid_matrix[i][j]
                max_i, max_j = i + 1, j + 1

                after_i, after_j = max_i + 1, max_j + 1

    # print(mid_matrix[max_i-2:max_i+2][max_j-2:max_j+2])
    
    return f"{max_j, max_i} {after_j, after_i}"

print(middle(aa, blosum62, ref, alt))

# print(len(ref), len(alt))
