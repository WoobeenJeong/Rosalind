### 이 경우는 밀려나고 안밀려나고를 고려해서 가장 최적을 구해야 하므로,
### DP를 통해서 최적 경로를 찾아야 함을 알 수 있음
## Edit dist.

import numpy as np

def editmatrix(ref,alt):
    matrix = np.zeros((len(ref)+1,len(alt)+1))
    
    for i in range(len(ref)+1):
        matrix[i,0] = i
    for j in range(len(alt)+1):
        matrix[0,j] = j
    
    # print(matrix)
    
    for i in range(1,len(ref)+1):
        for j in range(1,len(alt)+1):
            if ref[i-1] == alt[j-1]:
                matrix[i,j] = matrix[i-1,j-1]
            else:
                matrix[i,j] = min(matrix[i-1,j]+1,matrix[i,j-1]+1,matrix[i-1,j-1]+1)

    # print(matrix)

    return matrix

with open ("bioinfo2/rosalind_ba5g.txt", "r") as myfile:
    line=myfile.readlines()
    
    ref = line[0].strip()
    alt = line[1].strip()
    
    # print(ref,alt)
    
result = editmatrix(ref,alt)
edit_dist = result[len(ref),len(alt)]
print(int(edit_dist))
