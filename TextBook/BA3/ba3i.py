### input으로 주어진 kmer길이에 해당하는 binary 문자열을 만들어
### Eulerian path로 묶어주기
### Recursion에러가 나타나서, Stack을 이용하여 DFS를 구현
### time으로 실행 시간 측정

#############################################

import time
import random

def binary_strings(kmer):
    binary_list = []
    for i in range(2 ** kmer):
        binary = bin(i)[2:]
        binary = '0' * (kmer - len(binary)) + binary
        binary_list.append(binary)
    return binary_list

#############################################
### 위를 더 간단하게 코딩

def binary_strings(kmer):
    return [format(i, f'0{kmer}b') for i in range(2 ** kmer)]

#############################################
### 이전에 쓴 함수인용

def count_overlap(prefix, suffix):
    overlap_length = 0
    for i in range(1, min(len(prefix), len(suffix))):
        if prefix.endswith(suffix[:i]):
            overlap_length = i
    return overlap_length

def overlap(patterns):

    overlap_dict = {}
    max_overlap = 0
    
    for prefix in patterns:
        overlap_dict[prefix] = []
        for suffix in patterns:
            if prefix != suffix:
                overlap_length = count_overlap(prefix, suffix)
                if overlap_length >= max_overlap:
                    max_overlap = overlap_length
                    overlap_dict[prefix].append(suffix)

    return overlap_dict

#################################################

def eulerian(graph):
    path = []
    visited = set()

    stack = [random.choice(list(graph.keys()))]

    while stack:
        current_node = stack[-1]

        if current_node in graph and graph[current_node]:
            next_node = graph[current_node].pop()
            edge = (current_node, next_node)

            # print(edge, current_node)

            if edge not in visited:
                visited.add(edge)
                visited.add(current_node)

                if next_node not in visited:
                    visited.add(next_node)
                    stack.append(next_node)
            else:
                path.append(stack.pop())
        else:
            path.append(stack.pop())

    path = path[::-1]

    if path and path[0] == path[-1]:
        path.pop()

    return path

#############################################
### 아래 코드로 하면 kmer=10부터 RecursionError 발생

# def eulerian(graph):
#     path = []
#     visited_edges = set()
#     visited_nodes = set()  # 방문한 노드를 기록하기 위한 세트
    
#     def dfs(i):
#         if i in graph:
#             for node in graph[i]:
#                 edge = (i, node)
#                 if edge not in visited_edges:
#                     visited_edges.add(edge)
#                     if node not in visited_nodes:  # 이미 방문한 노드인지 확인
#                         visited_nodes.add(node)
#                         dfs(node)
#         path.append(i)

#     random.seed(0)
#     start_node = random.choice(list(graph.keys()))

#     dfs(start_node)

#     path = path[::-1]
#     if path and path[0] == path[-1]:
#         path.pop()

#     return path

#############################################

def merge(path):
    sequence = path[0]

    for node in path[1:]:
        overlap = len(node) - 1

        while sequence.endswith(node[:overlap]) is False:
            overlap -= 1

        sequence += node[overlap:]

    return sequence

#############################################

with open('bioinfo2/rosalind_ba3i.txt') as f:
    kmer = int(f.readline().strip())

start_time = time.time()

strings = binary_strings(kmer)
path = eulerian(overlap(strings))
result = merge(path)

end_time = time.time()
elapsed_time = end_time - start_time

# print(binary_strings(kmer))
# print(overlap(strings))
# print(path)
# print(result)
print(result[:-(kmer-1)])        # 마지막 반복 (kmer-1)개는 cycle이라 지워야 함 -> 아님 코드상에서 마지막은 연결 안하도록 바꾸기

#############################################

### Kmer  4 : 0.001 seconds
### Kmer  9 : 1.669 seconds
### Kmer 10 : 5.309 seconds
### Kmer 12 : 110.002 seconds (1.83 min)
### 문제된 점은 13 이상으로 가면 5분 이상 코드가 돌아가는 문제가 존재 

print(f"Elapsed Time: {round(elapsed_time,3)} seconds")
