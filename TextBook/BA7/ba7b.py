### leaf tree를 그렸을 때, limb length를 구하는 문제
### limb length의 정의 = leaf node에서 leaf node로 가는 internal node까지의 거리
### 즉, ba7a에서는 여러 path중에서 가장 deep하게 들어 갈 수 있는 dfs문제라면
### 유사하지만, 깊게 = 여러 node 거쳐서 (맨하탄 아님!) 가 아닌, 단순 이전까지 거리 구하기

### input으로 ba7a의 결과를 받아옴;; -> 이게 확장된 목적인 듯 (역으로 구하고자 하는 것이 목적. unrooted tree에서 distance matrix로)

import numpy as np

def limb(matrix, row_j):
    n = len(matrix)
    limb_length = float('inf')
    for i in range(n):
        for j in range(n):
            if i == row_j or j == row_j:
                continue
            else:
                limb_length = min(limb_length, (matrix[i][row_j] + matrix[row_j][j] - matrix[i][j]) // 2)
    return limb_length


with open('bioinfo2/rosalind_ba7b.txt', 'r') as file:
    data = file.readlines()
    limb_count = int(data[0].strip())
    row_j = int(data[1].strip())
    matrix_data = [list(map(int, line.split())) for line in data[2:]]

matrix = np.array(matrix_data, dtype=int)

# print(limb_count, row_j, matrix)

print(limb(matrix, row_j))
