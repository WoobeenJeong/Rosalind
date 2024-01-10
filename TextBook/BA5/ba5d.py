### 매우 기본적인 DP 시작 문제
### DP의 주목적인 Longest Path, 즉 DP matrix 작성시 가장 weight가 높은 path를 가는 방법
### pathfind 함수가 이전의 dfs와 유사한 구조임을 확인 가능
### 게다가 마지막을 pop으로 빼서 cycle이 아닌 DAG를 구성하는 것 까지

import numpy as np

def adjacent_matrix(root):  
    num_nodes = max(max(edge[0], edge[1]) for edge in root) + 1
    matrix = np.zeros((num_nodes, num_nodes))

    for edge in root:
        start, end, weight = edge
        matrix[start][end] = weight
    # print(matrix)    
  
    return matrix

# def trial_1(start, end, root):                # 이렇게 하면, 최단거리가 아닌, 첫 경로를 출력함
#     matrix = adjacent_matrix(root)            # 아이디어 : 아 여기서 maximum을 구하면 되겠네
#     count = 0
#     path = []
#     point = start

#     while point != end:
#         for i in range(len(root)):
#             if matrix[point][i] != 0:
#                 path.append(point)
#                 count += matrix[point][i]
#                 point = i
#                 break

#     path.append(end)
#     return f"{count}\n{path}"

def max_weight_path(start, end, root):
    matrix = adjacent_matrix(root)
    max_weight = -float('inf')
    path = []

    def pathfind(node, current, sum_edge_weight):           # max값 찾으려면 따로 pathfind 함수 만들기
        if node == end:
            nonlocal max_weight                             # nonlocal : 바깥쪽 변수 사용 -> 변수 지정을 -inf로 계속 불러오는 것을 방지
            if sum_edge_weight > max_weight:                # weight부분이 헷갈려서 sum_edge_weight와 max_weight로 변수명 설정
                max_weight = sum_edge_weight
                path.clear()                                # path를 초기화해줘야한다   
            if sum_edge_weight == max_weight:
                path.append(list(current))                  # append로 list형태로 누적
            return

        for i in range(len(matrix)):
            if matrix[node][i] != 0 and i not in current:                   # i not in current : cycle 방지 (동영상에서도 봤지만, 무한루프 방지)
                current.append(i)
                pathfind(i, current, sum_edge_weight + matrix[node][i])  
                current.pop()                                               # pop으로 빼줘야한다. (이거 안하면, cycle이 생김)

    pathfind(start, [start], 0)

    max_weight = int(max_weight)
    direction = '->'.join(map(str, path[0]))                # 꼭 [0] 지정해야한다 
    return f"{max_weight}\n{direction}"

#######################################################

with open("bioinfo2/rosalind_ba5d.txt", "r") as file:
    start = int(file.readline().strip())
    end = int(file.readline().strip())
    others = [line.strip() for line in file]
    
    root = []
    for each in others:
        separate = each.split("->")
        before = int(separate[0])
        after, weight = map(int, separate[1].split(":"))

        root.append((before, after, weight))

# print(root)

result = max_weight_path(start, end, root)
print(result)
