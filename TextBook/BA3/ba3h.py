### 이제까지 패턴 -> DBG 그리고 DBG -> DAG 를 구현
### 여기서는 패턴 -> DBG -> DAG 구현
### ba3e.py -> ba3g.py 

def overlap(patterns):
    
    overlap_dict = {}
    max_overlap = 0
    
    for prefix in patterns:
        for suffix in patterns:
            if prefix != suffix:
                overlap_length = count_overlap(prefix, suffix)
                if overlap_length >= max_overlap:
                    max_overlap = overlap_length
                    overlap_dict[prefix] = [suffix]

    return overlap_dict

#######################
### 이부분 나중에 다시 쓰려고 일부러 refactoring

def count_overlap(prefix, suffix):
    overlap_length = 0
    for i in range(1, min(len(prefix), len(suffix))):
        if prefix.endswith(suffix[:i]):
            overlap_length = i
    return overlap_length

#######################
### Eulerian Path (ba3g.py 그대로 가져와서 다듬기 추가)

def find_end(graph):
    in_degree = {}
    out_degree = {}
    for i, node_set in graph.items():
        out_degree[i] = out_degree.get(i, 0) + len(node_set)
        for node in node_set:
            in_degree[node] = in_degree.get(node, 0) + 1
    
    for i in set(in_degree.keys()) | set(out_degree.keys()):
        if in_degree.get(i, 0) < out_degree.get(i, 0):              ### 시작점 찾는것임
            start_node = i
            break

    if not start_node:
        start_node = next(iter(out_degree.keys()))
    return start_node

### RecursionError: maximum recursion depth exceeded while calling a Python object
### 너무 많은 재귀호출이 일어나서 생기는 에러

def eulerian(graph):
    path = []
    visited_edges = set()
    
    def dfs(i):
        if i in graph:
            for node in graph[i]:
                if (i, node) not in visited_edges:
                    visited_edges.add((i, node))
                    dfs(node)
        path.append(i)

    start_node = find_end(graph)          ### 시작점 찾기

    dfs(start_node)                       ### 시작점부터 dfs로 이어나가기

    path = path[::-1]
    return path

#######################
### 재귀호출 수정 -> stack으로 바꾸기

def eulerian02(graph):
    path = []
    visited_edges = set()
    stack = []

    def dfs_stack(start):
        stack.append(start)
        
        while stack:
            current_node = stack[-1]

            if current_node in graph:
                neighbors = graph[current_node]

                next_node = None
                for neighbor in neighbors:
                    edge = (current_node, neighbor)
                    if edge not in visited_edges:
                        visited_edges.add(edge)
                        next_node = neighbor
                        stack.append(next_node)
                        break

                if next_node:
                    continue

            path.append(stack.pop())

    start_node = find_end(graph)
    dfs_stack(start_node)

    path = path[::-1]
    return path

#######################

def into_string(path):
    result_sentence = path[0]

    for i in range(1, len(path)):
        current_word = path[i]
        previous_word = path[i - 1]
        overlap = count_overlap(previous_word, current_word)
        result_sentence += current_word[overlap:]
    
    return result_sentence

#######################
### input

with open ('bioinfo2/rosalind_ba3h.txt', 'r') as f:
    k = f.readline().strip()
    patterns = f.read().splitlines()
    
#######################
### 과정 엿보기

DBG = overlap(patterns)
path = eulerian02(DBG)
result = into_string(path)

# print(k, patterns)
# print(overlap(patterns))
# print(find_end(DBG))
# print(eulerian02(DBG))

print(result)
