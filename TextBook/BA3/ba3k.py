### Contigue generation
### 이전 debruijn graph에서 contigue를 생성하는 과정

from collections import defaultdict

#############################################
### 잘못된 de Bruijn graph 만들기 (ba3j 함수 응용)

# def DeBruijn(pattern_dict):
#     graph = {}
#     for i in pattern_dict:
#         for j in pattern_dict:
#             if i != j and i[1:] == j[:-1]:
#                 if i not in graph:
#                     graph[i] = []
#                 if j not in graph[i]:
#                     graph[i].append(j)
#     return graph

#############################################
### k-1 mer로 de Bruijn graph 만들기

def kmius1_DeBruijn(pattern_dict):
    graph = defaultdict(list)
    for patterns in pattern_dict:
        graph[patterns[:-1]].append(patterns[1:])
    return graph

#############################################
### 만든 graph에서 indegree, outdegree 찾기 (ba3g find_end 함수 활용)

def inoutdegree(graph):
    in_degree = {}
    out_degree = {}

    for i, node_set in graph.items():
        out_degree[i] = out_degree.get(i, 0) + len(node_set)
        for node in node_set:
            in_degree[node] = in_degree.get(node, 0) + 1

    for key in in_degree.keys():
        if key not in out_degree:
            out_degree[key] = 0
    for key in out_degree.keys():
        if key not in in_degree:
            in_degree[key] = 0
    # print(in_degree, out_degree)
        
    return in_degree, out_degree

#############################################

def max_nonbranch_path(graph):
    indeg, outdeg = inoutdegree(graph)
    fractions = []
    contigs = []
    
    for innode, incount in indeg.items():
        for outnode, outcount in outdeg.items():
            if innode == outnode:
                if not (incount == 1 and outcount == 1) and outcount > 0:
                    for current in graph[innode]:
                        path = [innode, current]
                        while indeg[current] == 1 and outdeg[current] == 1:
                            path += graph[current]
                            current = graph[current][0]
                        fractions += [path]

    memory = sum(fractions, [])
    # print(memory)

    for innode, incount in indeg.items():
        for outnode, outcount in outdeg.items():
            if innode == outnode:
                if (incount == 1 and outcount == 1) and innode not in memory:
                    memory.append(innode)
                    linknode = [innode]
                    while linknode:
                        current = linknode.pop(0)
                        path = [current]
                        while indeg[current] == 1 and outdeg[current] == 1 and graph[current][0] in linknode:
                            path += graph[current]
                            current = graph[current][0]
                            linknode.remove(current)
                        fractions += [path + [path[0]]]

    for path in fractions:
        fullpath = path[0] + "".join(x[-1] for x in path[1:])
        contigs.append(fullpath)
        # print(contigs)

    return contigs

#############################################

patterns = []

with open('bioinfo2/rosalind_ba3k.txt', 'r') as f:
    for line in f.readlines():
        patterns.extend(line.strip().split(' '))
        
    # patterns = [line.strip() for line in f.readlines()]
    
# print(patterns)
# print(kmius1_DeBruijn(patterns))

graph = kmius1_DeBruijn(patterns)
result = max_nonbranch_path(graph)

for i in reversed(result):              ### result의 원소를 역순으로 출력 (그냥 출력해도 상관 없음)
    print(i, end=' ')
