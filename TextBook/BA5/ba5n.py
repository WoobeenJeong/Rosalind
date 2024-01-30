### topological ordering으로 root를 가져오기
### 이번엔 일단, path정보를 불러와서 path에 대한 정보를 before -> after로 root형태로 [ ] tuple 저장

import numpy as np

with open("bioinfo2/rosalind_ba5n.txt", "r") as file:
    path = file.readlines()

root = []
for each in path:
    separate = each.strip().split("->")
    before = int(separate[0])
    after_list = list(map(int, separate[1].split(',')))
    for after in after_list:
        root.append((before, after))
    
# print(root)

def topo_order(root):

    nodes = max(max(edge[0], edge[1]) for edge in root) + 1         # 1. adjancent matrix
    matrix = np.zeros((nodes, nodes))
    
    for edge in root:
        start, end = edge
        matrix[start][end] = 1
    # print(matrix)
    
    indegree = np.zeros(nodes)                                      # indegree = edge받는 end node의 연결 갯수
    memory = []                                                      # memory = 임시저장
    result = []                                                     # result = 결과값
    
    for edge in root:                                               # 2. 모든 node에 대해, end node가 될 때, edge의 연결 개수 저장 
        start, end = edge
        indegree[end] += 1
    # print(indegree)
    
    for i in range(nodes):                                          # 3. indegree가 0인 node를 memory에 저장 (=시작점 찾기)
        if indegree[i] == 0:
            memory.append(i)
    # print(memory)
        
    while memory:
        node = memory.pop(0)                                         # 4. memory에서 node를 하나씩 빼서 T에 저장 (즉, 연결 개수 작은 순서로 T에 저장)
        result.append(node)
            
        for i in range(nodes):
            if matrix[node][i] != 0:
                indegree[i] -= 1                                       # 연결개수가 언젠가는 0이 되고 -> memory에 저장, 그걸 맨 위의 while문에서 result에 저장 반복
                
                if indegree[i] == 0:
                    memory.append(i)                    
        # print(result)
    
    if any(0 in pair for pair in root):
        final = result
    else:
        final = []                                                 # result에서 0번째 node (사실상 존재X) 제외 (만약 0이라는 node가 없으면)
        for x in result:
            if x != 0:
                final.append(x)
    
    return final

answer = ', '.join(map(str, topo_order(root)))                      # 그냥 print(topo_order(root))하면 list로 출력
print(answer)                                                       # 이렇게 해야 [ , , ]이 아닌, , , 로 출력
