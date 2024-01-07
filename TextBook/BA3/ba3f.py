### find eulerian path in a graph
### 먼저 graph를 dictionary로 만드는데, 이때 value는 list형식으로 여러개 가능
### 주어진 pseudo code 참조 할 것

def eulerian(graph_dict):
    cycle = []
    visited_value = {}
    copied = {key: list(value) for key, value in graph_dict.items()}  # 복사본 생성 (굳이 필요없지만, eulerian02와 비교 위해)

    while copied:
        current = next(iter(copied))
        cycle.append(current)
        visited_value[current] = True

        while copied[current]:
            next_node = copied[current].pop()
            if not copied[current]:
                del copied[current]
            if next_node in copied:
                current = next_node
                cycle.append(current)
                visited_value[current] = True
            else:
                break
            
    return cycle

#############################################
### 위 코드는 순환하는 그래프를 만들지 못함

def unvisit(node, visited, graph):
    return [neighbor for neighbor in graph.get(node, []) if not visited[node][neighbor]]

def eulerian02(graph):
    visited = {node: {neighbor: False for neighbor in graph[node]} for node in graph}
    cycle = [next(iter(graph.keys()))]

    while any(False in node.values() for node in visited.values()):
        current = cycle[-1]
        new = unvisit(current, visited, graph)

        if new:
            neighbor = new[0]
            visited[current][neighbor] = True
            cycle.append(neighbor)
        else:
            for node in reversed(cycle):
                if any(not visited[node][neighbor] for neighbor in graph[node]):
                    index = cycle.index(node)
                    new_start = node
                    break
            else:
                # cycle 안에 node가 없는 경우 예외 처리
                raise ValueError("Invalid Eulerian path")

            result = []
            current = new_start
            while True:
                new = unvisit(current, visited, graph)
                if new:
                    neighbor = new[0]
                    visited[current][neighbor] = True
                    current = neighbor
                    result.append(current)
                else:
                    break

            cycle[index:index + 1] = result

    # 추가된 부분: 모든 노드 방문 여부 확인
    if any(False in node.values() for node in visited.values()):
        raise ValueError("Invalid Eulerian path")

    return cycle

#############################################
### random start로, 정확한 cycle을 찾도록 수정
### 대신, 검산 및 결과 비교를 위해 seed 설정

import random

def eulerian03(graph):
    def explore(v, cycle):
        while graph[v]:
            u = graph[v].pop()
            explore(u, cycle)
        cycle.append(v)

    random.seed(0)
    start_node = random.choice(list(graph.keys()))
    # start_node = 0
    eulerian_cycle = [start_node]

    while any(graph.values()):
        for i, node in enumerate(eulerian_cycle):
            if graph[node]:
                new_start = eulerian_cycle[i]
                new_cycle = []
                explore(new_start, new_cycle)

                eulerian_cycle = eulerian_cycle[:i] + new_cycle + eulerian_cycle[i + 1:]

    ### cycle이 "누적 되므로" 역순으로 출력
    return eulerian_cycle[::-1]

#############################################

with open('bioinfo2/rosalind_ba3f.txt', 'r') as f:
    graph_dict = {}
    
    for line in f:
        line = line.strip().split(' -> ')
        key = int(line[0])
        values = [int(x) for x in line[1].split(',')]
        graph_dict[key] = values

# print(graph_dict)

#############################################
### 결과 비교

result = eulerian(graph_dict)
result02 = eulerian02(graph_dict)
result03 = eulerian03(graph_dict)
# print(result, len(result))
# print(result02, len(result02))
# print(result03, len(result03))
# print(len(graph_dict))            ### 검산용

#############################################
### 출력 형식

print("->".join(map(str, result03)))

#############################################
### 밑의 사념 정리 : order does not matter

### 결과는 동일한데, Extra dataset까지, 문제는 순서가 왜 다를까?
### 우리는 0부터 항상 시작하는데 rosalind에서는 0이 아닌 수로 시작하는데...
### form a cycle Cycle by randomly walking in Graph (don't visit the same edge twice!) 이 pseudo code를 간과했다.
### 해당 내용으로 보자면 초기 cycle의 randomization으로 start를 결정해야 한다.
