### Eulerian cycle에서는 순환하기 때문에 DBG의 a -> b, c 로 이루어진 구성에서
### b를 가져오는 애는 a다 라는 것을 연결해서 그럼 a는 누가 가져오지 하는 형식으로 순환고리 생성가능
### = 해당 과정을 DFS, 깊이 우선 탐색, "Depth First Search"
### 순환하므로, random start 가능
### Eulerian path에서는 위 형식은 같지만, 시작점과 끝점이 다르다, 즉 정해질 수 있다.

### 즉 끝점은 어떻게 찾을지를 추가만 하면 된다. (거슬러 올라가므로)

def find_end(graph):
    in_degree = {}
    out_degree = {}
    for i, node_set in graph.items():
        out_degree[i] = out_degree.get(i, 0) + len(node_set)
        for node in node_set:
            in_degree[node] = in_degree.get(node, 0) + 1

    for i in set(in_degree.keys()) | set(out_degree.keys()):        ### 해당 node에서 나가는 edge가 들어오는 edge보다 많으면 종료지점이므로
        if in_degree.get(i, 0) < out_degree.get(i, 0):
            end_node = i
            break

    if not end_node:                                               ### 만약 발견 안되면 그냥 아무거나
        end_node = next(iter(out_degree.keys()))
    return end_node

### 기존과 유사하지만, 이번엔 DAG이므로 visited_edges가 모두 끝나면 종료
### 지난번 ba3f의 Eulerian은 cycle이므로 while문으로 모두 방문

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

    end_node = find_end(graph)          ### 끝점 찾기

    dfs(end_node)                       

    path = reversed(path)
    return path

#############################################

with open('bioinfo2/rosalind_ba3g.txt', 'r') as f:
    graph_dict = {}
    
    for line in f:
        line = line.strip().split(' -> ')
        key = int(line[0])
        values = [int(x) for x in line[1].split(',')]
        graph_dict[key] = values

# print(graph_dict)

#############################################

result = eulerian(graph_dict)
print("->".join(map(str, result)))
