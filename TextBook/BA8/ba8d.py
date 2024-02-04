### Soft k-means
### random하게 초기값을 고르지만, 대신 초기값에 민감
### 떄문에, rosalind 문제에서는 초기값을 random으로 구현하는 것보다,
### 그냥 처음에 제시한 이들을 초기값으로 진행하면 답에 더 쉽게 근접
### EM algorithm based, converge

import numpy as np

def euclidean_distance(p1, p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))

def Estep(pairs, centers, beta):
    k, n = len(centers), len(pairs)
    hidden_matrix = np.zeros((k, n))

    for i in range(k):
        for j in range(n):
            distance = euclidean_distance(pairs[j], centers[i])
            hidden_matrix[i][j] = np.exp(-beta * distance)          # beta = stiffness

    hidden_matrix /= np.sum(hidden_matrix, axis=0)                  # Normalize 해줘야 함 까먹었음...

    return hidden_matrix

def Mstep(pairs, hidden_matrix):
    k, n = hidden_matrix.shape
    responsibilities = []                                           # responsibilities = parameters = new_centers

    for i in range(k):
        sum_hidden_matrix = np.sum(hidden_matrix[i])
        # center = np.sum(pairs[j] * (hidden_matrix[i][j] / sum_hidden_matrix) for j in range(n))  # Warning 발생 지점
        # DeprecationWarning: Calling np.sum(generator) is deprecated, and in the future will give a different result. Use np.sum(np.fromiter(generator)) or the python sum builtin instead.
        center = np.dot(pairs.T, hidden_matrix[i] / sum_hidden_matrix)
        responsibilities.append(center)

    return responsibilities

def soft_k_means(pairs, k, beta, steps=100):
    # random = np.random.choice(len(pairs), k, replace=False)   # 이 코드는 어느정도 random으로 해도 돌아가네, 값 정렬만 해주면 됨
    # centers = [pairs[i] for i in random]
    centers = pairs[:k]                                  # 랜덤보다는 맨앞 k개의 center설정

    for _ in range(steps):
        hidden_matrix = Estep(pairs, centers, beta)
        responsibilities = Mstep(pairs, hidden_matrix)
        centers = responsibilities

    return centers

with open('bioinfo2/rosalind_ba8d.txt', 'r') as f:
    k, m = map(int, f.readline().split())
    beta = float(f.readline())
    pairs = [list(map(float, line.split())) for line in f]

pairs = np.array(pairs)

result = soft_k_means(pairs, k, beta)
        
for each in result:
    print(" ".join(map(lambda x: "{:.3f}".format(x), each)))
    
# for center in result:
#     print(" ".join(format(coord, ".3f") for coord in center))
