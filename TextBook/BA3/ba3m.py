### 이전 ba3k 에서 maximal_non_branching_paths 구한 것의 일부분
### 여기서는 adjaceny list가 인풋

#############################################
### ba3k의 indegree, outdegree 구하는 함수

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
        
    return in_degree, out_degree

#############################################
### cycle을 처리하려면 (7,6),(6,7) 에서  
### 7 -> 6 -> 7 과 6 -> 7 -> 6 둘 다 가능하기 때문에 중복을 제거 필요

def remove_edge(graph, source, sink):
    graph[source].remove(sink)
    if not graph[source]:
        del graph[source]
    return graph

#############################################

def max_nonbranch_path(graph):
    paths = []
    indeg, outdeg = inoutdegree(graph)

    for nth_graph_element in list(indeg):
        if [indeg[nth_graph_element], outdeg[nth_graph_element]] != [1, 1]:
            if outdeg[nth_graph_element] > 0:
                while nth_graph_element in graph:
                    source = graph[nth_graph_element][0]
                    non_branching_path = [nth_graph_element, source]
                    graph = remove_edge(graph, nth_graph_element, source)
                    while [indeg[source], outdeg[source]] == [1, 1]:
                        sink = graph[source][0]
                        non_branching_path.append(sink)
                        graph = remove_edge(graph, source, sink)
                        source = sink
                    paths.append(non_branching_path)

    while graph:
        start_node = list(graph)[0]
        current_node = graph[start_node][0]
        graph = remove_edge(graph, start_node, current_node)
        cycle = [start_node, current_node]
        while current_node != start_node:
            target_node = graph[current_node][0]
            cycle.append(target_node)
            graph = remove_edge(graph, current_node, target_node)
            current_node = target_node
        paths.append(cycle)
    
    tuple_paths = [tuple(path) for path in paths]                           ### tuple로 변환 후 중복 제거
    unique_tuple_paths = list(set(tuple_paths))                             ### loop를 처리하는 과정에서 (A->B)와 (B->A)의 경우 (A,B),(A,B)로 중복
    unique_paths = [list(tup_path) for tup_path in unique_tuple_paths]
    
    return unique_paths

#############################################

graph = {}

with open("bioinfo2/rosalind_ba3m.txt") as f:
    adj_list = f.read().splitlines()
    for i in range(len(adj_list)):
        adj_list[i] = adj_list[i].split(" -> ")
        graph[int(adj_list[i][0])] = list(map(int, adj_list[i][1].split(",")))
        
# print(adj_list)
# print(graph)
# print(inoutdegree(graph))

result = max_nonbranch_path(graph)
for i in result:
    print("->".join(map(str, i)))
    # print(i)                      ### 출력형식 맞추기 전, list가 제대로 작성되었는지 확인용
