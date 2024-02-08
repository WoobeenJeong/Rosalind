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
        contigs.append("->".join(map(str, path)))

    return contigs

#############################################

graph = {}

with open("bioinfo2/sample.txt") as f:
    adj_list = f.read().splitlines()
    for i in range(len(adj_list)):
        adj_list[i] = adj_list[i].split(" -> ")
        graph[int(adj_list[i][0])] = list(map(int, adj_list[i][1].split(",")))
        
# print(adj_list)
print(graph)
print(inoutdegree(graph))

result = max_nonbranch_path(graph)
for i in result:
    print(i, sep="\n")
