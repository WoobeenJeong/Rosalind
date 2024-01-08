import random

def eulerian(graph):
    def dfs(node, cycle):
        while graph[node]:
            new_node = graph[node].pop()
            dfs(new_node, cycle)
        cycle.append(node)

    start_node = random.choice(list(graph.keys()))

    eulerian_cycle = [start_node]

    while any(graph.values()):
        for i, node in enumerate(eulerian_cycle):
            if graph[node]:
                new_start = eulerian_cycle[i]
                new_cycle = []
                dfs(new_start, new_cycle)
                eulerian_cycle = eulerian_cycle[:i] + new_cycle + eulerian_cycle[i + 1:]

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

result = eulerian(graph_dict)
print("->".join(map(str, result)))
