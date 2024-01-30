### Tree를 그렸을때, 아무리 많아도 결국
### 자식 node (최하단 node) 에 대한 n x n matrix 만들어야 한다
### So, 자식 node는 어떻게? = 관계도 그림 그려보기 = 유사 한붓그리기 문제 
### 즉 edge가 1개인 node = leaf node = 자식 node
### 정확히 하자면, 주어진 input에서는 in,out으로 2개의 edge (거의 모든 것들이 2개일 것임 = 2개 이하로 안전빵 하자)

### 다행히 input이 a->b와 b->a가 같은 symmetric한 경우임

import numpy as np

def find_leaf(node_set, num_leaves):
    num_start = max([int(start) for start, _, _ in node_set]) + 1
    num_end = max([int(end) for _, end, _ in node_set]) + 1
    matrix = np.zeros((num_start, num_end))
    
    for node in node_set:
        start, end, edge = node
        matrix[int(start)][int(end)] = edge
        matrix[int(end)][int(start)] = edge
    # print(matrix)
    
    # leaf_nodes = [n for n in range(num_start) if sum(matrix[n, :] != 0) <= 1 and sum(matrix[:, n] != 0) <= 2]
    leaf_nodes = []                                     # 이 부분을 짧게 넘기고 싶으면, 위 코드를 쓰면 됨
    for n in range(num_start):
        row_non_zero = sum(matrix[n, :] != 0)
        col_non_zero = sum(matrix[:, n] != 0)
        if row_non_zero + col_non_zero <= 2:
            leaf_nodes.append(n)    
    # print(leaf_nodes)
    
    if len(leaf_nodes) == num_leaves:
        return leaf_nodes, matrix     
    else:
        print("Error: The number of leaf_nodes is not equal to num_leaves.")


def dfs(node, matrix, distances, visited):                          # 이걸 dfs 알고리즘 = 깊이 우선 탐색 이라고 함
    visited[node] = True                                            # 해당 node에 방문했음을 저장
    # print(visited)
    for i in range(len(matrix)):
        if matrix[node][i] > 0 and not visited[i]:
            distances[i] = distances[node] + matrix[node][i]
            dfs(i, matrix, distances, visited)                      # 재귀함수로 구현 (가장 나의 weak point)

def short_matrix(node_set, num_leaves):
    leaf_nodes, matrix = find_leaf(node_set, num_leaves)
    new_matrix = np.zeros((num_leaves, num_leaves))
    
    for i in range(num_leaves):
        visited = [False] * len(matrix)
        distances = [0] * len(matrix)
        dfs(leaf_nodes[i], matrix, distances, visited)
        new_matrix[i] = distances[:num_leaves]
    
    return new_matrix


with open("bioinfo2/rosalind_ba7a.txt", "r") as file:
    num_leaves = int(file.readline().strip())
    edges = [line.strip() for line in file]
    
    node_set = []
    for edge in edges:
        start, rest = edge.split("->")
        end, edge = map(int, rest.split(":"))
        node_set.append((start, end, edge))

result = short_matrix(node_set, num_leaves)

for row in result:
    dist = [int(value) for value in row]
    print(" ".join(map(str, dist)))

#############################################################

### 처음에는 다음과같이 reduced matrix를 만들려고 했는데, [i][k] + [k][k] + [k][j]에서 [0][4] [4][5] [5][2] 형태로 [0][2]가 계산되지 않음. [k][k] = [4][5] 계산이 인됨
### so, 거쳐간 node를 기록해야함
### 그래서, for k ~ 대신 while k == j: new_matrix[i][j] += matrix[i][k]로 바꾸니까, 에러문구 없이 무한루프 발생

# def dist_matrix(node_set, num_leaves):
#     leaf_nodes, matrix = find_leaf(node_set, num_leaves)
    
#     new_matrix = np.zeros((num_leaves, num_leaves))
    
#     for i in range(num_leaves):
#         for j in range(num_leaves):
#             if i != j:
#                 for k in range(len(matrix)):
#                     new_matrix[i][j] += matrix[i][k] + matrix[k][k]+ matrix[k][j]
            
#     return new_matrix
    
