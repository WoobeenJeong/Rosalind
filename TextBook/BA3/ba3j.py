### (k,d)mer paired 정보를 기반으로 string으로 reconstruct
### 두 kmer를 가지고 있지만, 두 kmer사이에 d만큼의 거리(unknown 서열) pair로부터
### 한마디로 gapped kmer pair -> string
### (k,d)-mer 에서 k는 kmer, d는 gap을 의미, 인덱싱

### 이것도 어떻게 하면 최적화되어 빠르게 여러 개의 kmer를 처리할 수 있을까가 관건
### logic : k-1 DeBruijn graph를 만들어서 Eulerian path를 찾고, 그걸로 reconstruct

#############################################

def kmius1_DeBruijn(pattern_dict):
    graph = {}
    for pre, post in pattern_dict:
        prefix = (pre[:-1], post[:-1])
        suffix = (pre[1:], post[1:])
        
        if prefix not in graph:
            graph[prefix] = []
        graph[prefix].append(suffix)

    # for key, value in graph.items():
    #     print(f"{key}:{value}", sep='\n')
    # print(graph)
    return graph

#############################################
### 모든 원소가 graph에 존재하는지 확인

def check_patterns_in_graph(pattern_dict, graph):
    for pre, post in pattern_dict:
        prefix = (pre[:-1], post[:-1])
        suffix = (pre[1:], post[1:])
        
        if prefix not in graph or suffix not in graph[prefix]:
            return False

    return True

#############################################
### 이게 오류가, start_node를 찾는 과정에서, in_degree가 out_degree보다 큰 노드를 찾아야 하는데
### 단순히 (짧은 서열로 봐서) value에만 있고 key에는 없는 노드로 설정해버림
### 이 경우의 가정은 결국 out_degree 제일 작은 서열로 하겠단 것이고 이는 논리적으로 맞지 않음

# def find_start(graph):
#     start_node = []
    
#     for key,value in graph.items():
#         if key not in graph.values():
#             start_node.append(value[0])
#             print(start_node[0])
#             break
                
#     return start_node[0]

### 이 코드를 썻을때, 결과는 나오지만 뒤쪽에 잘림
### 결과 서열: GAAAGGTACAAATACTGGCGACCTCGCTGTTCGACACTTCATCACTGCTCCGGGGCGCTCAGGAGGGACGGTTCCCTGTACCATTGGAAGTCAATAGTCTAAGGTACAAAGAGAAGACCCGACCCGACAGAGGGGGTTCTGCGCCGGGTTTCGAGCTTGTAACCCCCCAGAGAATTAGATCCACCGTCTGTGTGGACAAAGTAGTAAAGCTAGCATACCAAATTGAAATTCGGAGTTTGACTACCAGATCCACGCATACGCTGCACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTAGAAATTCAGAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGGGGGTAATTCGTAGTTAGGTACAGAAAACTCCCGGACAGAACCGCATATAACCGATGAAGCAAGGGTTCTTCATTTAATACGACCCTAACCGGTATTGCTGCTAGCTTGATTTTCCTAGCAATCTAAACTCTATGTATGAGGCCACTCGGACGCCCGCTAGTGCCGGCAGCTAGCTACTGCCCTTCACCAGGAGCACGCACTATGCCTATCGGGCAATGCTGATCATACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGATCCCTCTGCAGAAAGCGGTGGCGGCGGGTCTAAGCAAGTCCAACGCAATACCAGGAAATCACCGTATCGTTAGCGACCAGTAGGTGATGGTTTGTAAGTTCGGACTACAGGCGGATGTGTCCCCGCCAGTTAAAAGTCGACTTTCTGTTACAACTGCTCCCTACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTCTAATGATCCCCACAGATCGTGTTTCAACGTTGAAGTCTGAATGGGTTCGTGAATATAGCCATCCAACGTGGACAATAAGATGAGCTTTATAGTTTCCGATCCTCATGGCGATCGAATAAGATCTATCCGCTTGTGTGTGTACGAGTCGCCGACTAACCGGTCTTGGGATATATACGTCACAGATTAAGTACTCGTCACGAGCTTGAATGGGAAGATAAGTAGACTCTTGTCGGGCACACACAGAGACTCCGACGCATCGAGATCGCAAACACTGCCTCCAGCCGGGGGATGCTAATCGTCGCGGTCGGTCCGAGCTTTATTCTACATCGTGGTGTTTCCGACCGAGCCATAAGAACAGTGTCCAAGTCACAAGAGGAGCACGCGGTGGAGGTCGTTCGCTATACAATATATTTGCAACTGTGTCTGGCATCACGCGCATTTCTCACACTTCCAAACGTGCTGCATTCTAAATGATTTCATGAATAGATTGTCTACTAGTTCACCCAAGGTATTACAGCACTGGTCATGTGCCGCTCTGGCACGGCTAGTATCAGGGCCGACTGTGTCCTAGGCGGCTGTTTTCGGGAGCCCAAGGGAAGCAATCAATGCGTTGACTGACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGATGACCCTAGGGCGGGCTGTTTGAGTGGGCTATCGGCGACCATTTCGCCCCGCAAGCCCCCGTCACGATACCGAGACCCTGAAGCTCATAAACGCCTATCTTTGTTGCATGAACAACGGGAGTAAGCGAGGCCAGGCCATACGGTTTCGGAGCCGCAGAATAGCCTTTACACGACCTCTACACAACCCAAAGTGAATATCCACGGGGTATTGTTTGTGCTGCTACCATGCGCAGTCAACATCGCCCACCGGCGATGTGTTTCAGATCTGCAGGCCCATCAACCGTTGTGACACCACCCCGGCTTTCAGAAGCAGTATGTCGGACACATTGACCTGTAGCGTTAGTTCTGTACAAGGGACCCTGCTCACTCGAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTTGGGAATCTAATGCGGTCTGCCATGGGACCCCTAACAACAAGGGACGCCTCCACCTGTCTAGGAGGAAAGACTTTACACACATCTTCTAGTTTCGAGAAGCACCGTAGCCAGTGGACCCTGAGTGGTTACAAACAAATCGCAGTTTAGCGCTTACCGACAAAGGCGGGAGCTTCGTTCACATTAGGATTGAAAGAACTTAAGAGTCTGTAGGCTCGGAGGTCTCTATATATACCATCTAGTCGTCCGGGGCATGATTAACTAAGAGTTGATCTGAGTCGGAACATAATGCCTGATCTGACCCCAATTCACTACGGTCGCACGTTCCGGGAACACCTACCGATCAGTCCGGAACTGTGACCTAAGAAGTCTCAAGCCTTTACGTCAATGTTCCCGGTGAAGGACTGTGTAACGGTCGCCTTCGCGCCCCCCCATAGGCCGGTCCTTCTCGTTGCAGGATAGCTAAGTCCCATATAGAGTTGTTGGTGTACCATTACGCTGATTTTACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTGGTGTGTTCAACTCAGCATACCCGGTTAGTCTGGAGCACTCCCCGTGCCTACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTGCCGAAATCCTTGTCAAGTAGTGGCATCTACTGCCGCGGGGCAGGACTGATGCTGACCCAAGACCACGCTCCTATCAGCCGGTGGCGCATCAGGGTGGGCTATAAGTTATATTCCTACTGTACGGCTGAAGTCAGCTGTAGTCAGGGAGCGGTTCCTGAGCCGGCTGATTCCGCTCGTAATGCGCTATGTAGAAGCATAGTTAGCCTCGCGCTCGTGTGTGGGCAGTCGTATAAGTAGTTTAGCTCCCGATGCGAAGGAGTTGCAAGTACCTACAAACTCGTAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGTCCGGTTCATATTAACCATGCACCAAGGTTTGACTAAATCAACTCGTGGGAATCCGACGTGACAAAATCCCCAGATATGCCGGGGGTGCACGTGAATACGTCGTAAGTTGAGCGTCCTATGACGGGAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGCCAAAGTAATACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGAATCCTTGACTGGCCTGCCGAGTGTTATCTCGCTGCTATCCCCCCCCAAGGTAGAAATGGAAGTGGGATCCAGCGCACCAAGGCACTTCACACAGGCATTACCCCAGCACCACGAATTAGCTTGCAGCTAAAGACAGGGTATTTTACGGAGTATATGATCTCTGTGAGGTACCGTATTCACACATCGTGGGATGTCTGCCATGAGCTTTTCCATTAGTATCCGGCGAGTTTTGATCCAAGTTACCAAACAAGGTTGTCCTCCAGGTCCTACGTGCTGAACGGCCAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGCCGGATCGGCCCTGACTCAAGTAAGGTCTGGTTGCTTGTCACTACATAAAGCCACGGAAGGGTGCGCGGCCCCAAAGCTGCGTCCGGATTCGACTCCCGTTTGCCTGGCTTCTCGACGAATCTAACGTTCTCATTAACCGAAAACCCTGAGCGGCTTAACCTCATTCGTCCCAGAATCAAACCCATCGTGTATCACCGTTGGCCCAGCAGGGAAGACAAGACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTGTGGCTCCCCAACCGAAGAATAAGATCCCTTCGCCGCCACAGAAGCAACACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGATTTAAAGTCTACCGTGGGGAGCCGGACGAGAACAAGACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGTAGGCGGCTACCTTCTGCCCATATCTCGGAATCCTTAGGGTCTTTAGCTGCTGGCAACACGGGGATGCCTTAGTCGCGGGGGAGCCGTTAGATCGGTTTCAGACTTGCCGACACCGTTCACCGTGGCCGGCCAACCGGCCGGTTCTGTGCTCCACTGAGTTTAGATAGGAATCCATACCTATAGTTTTACGTACACCAACTGGTTAACAAGCCGTCTCCGCGATGACAAACGGTGGGGGCACGAGCTCGAGGTAAGAGGTTGCGATCCGATTACAATGTATGACTACTTATAATGGTCTTACCTTAAATAGGGAACGGGTTTACAGATTACATGTCGGCGAAGACGTTACTGTATTTCGGCCAATGAGCAAATTCCCACCAGGCTCGCTCGGCTTAAATAGAATAGTCAGATTGGCTCTGAATGCTTTGGGCGTGCATTGAGAGCAGCCATATGTAATATTAAATGGCAGTACAAATCATACAGTTCAGAACTGCCGACAGCGCAGGAGTTTAAGGGTATCGAATATTGCGCTATCCGTGAGTGCTCTTAGCGATGGGGGGGCGGACCCTAAGTCTGACCCCCTCTCCTACCTTCTACGGATTACTATTATTGGCACTTGATGAGTAATCATTTCTAGCAAGAGTCTTATAAGGTAAACAATAACTTAGTAAGTGAGTCATGTAGTGTGCTTCCAGGACGAGTCGGCAAACTCTGTAGTCTTATGCTCATGTCTGACCTGCTGTGCCCAAAATTCTCTTCGTAAGGAGGGCTTTATAATGTTATGGGCACGACTTCGCATTGGGTCCACGCCCCAGGACTTCAGCATGTTATTTTGGGTTGCAGGATTTAAGAGAGCCTCATGCGTTGATAAGCCAAAGTGGGGGTATGGTGGGACCTCTCACCATGAGAGTTAAGTTAACTCACCGTGGCTCAAAAAAAGCTGGTTAGAATCTGCGAGTAATACGAGCGGGAAAATCTGGAATAACAGAAGCGACACCCTGACCTACAGTCGTTCAGTACTAGGTTACAAGTGAACCACTCGCGGATATAGTCAGGCGGGGATGTCCCGCGCGTTGATTAGACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGCGAGTTAATTGAAGTTTGCCTAGACACCGCTGAGGCTGGTTCGACATACCCTTAGGGAGGCCAAGCTATATAAAACCAAGATCATTGACCCCCTACGTGATACGTGATTTCAAACTTTACAATCATTAGGGTCGCCAGTGGAGAATCTATAGAATCTTTTCTACAGGCTACAGAGAAGCATTTTTCACAGGACCGCGTGGCGCAAACAATCCGATGGGGACCATCTGTGAACTCCCATACGTGACTATTCTGTGTCACATGAGGGGAGCTAGGGGGATTGAGTGCTCATGTCGGTTGGAGACCATTTTGAGTGCACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGCGAAGCATACTTACCTTGATCAACGCAGTGATTATTCATCTGAAGA
### 원하는 결과: GAAAGGTACAAATACTGGCGACCTCGCTGTTCGACACTTCATCACTGCTCCGGGGCGCTCAGGAGGGACGGTTCCCTGTACCATTGGAAGTCAATAGTCTAAGGTACAAAGAGAAGACCCGACCCGACAGAGGGGGTTCTGCGCCGGGTTTCGAGCTTGTAACCCCCCAGAGAATTAGATCCACCGTCTGTGTGGACAAAGTAGTAAAGCTAGCATACCAAATTGAAATTCGGAGTTTGACTACCAGATCCACGCATACGCTGCACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTAGAAATTCAGAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGGGGGTAATTCGTAGTTAGGTACAGAAAACTCCCGGACAGAACCGCATATAACCGATGAAGCAAGGGTTCTTCATTTAATACGACCCTAACCGGTATTGCTGCTAGCTTGATTTTCCTAGCAATCTAAACTCTATGTATGAGGCCACTCGGACGCCCGCTAGTGCCGGCAGCTAGCTACTGCCCTTCACCAGGAGCACGCACTATGCCTATCGGGCAATGCTGATCATACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGATCCCTCTGCAGAAAGCGGTGGCGGCGGGTCTAAGCAAGTCCAACGCAATACCAGGAAATCACCGTATCGTTAGCGACCAGTAGGTGATGGTTTGTAAGTTCGGACTACAGGCGGATGTGTCCCCGCCAGTTAAAAGTCGACTTTCTGTTACAACTGCTCCCTACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTCTAATGATCCCCACAGATCGTGTTTCAACGTTGAAGTCTGAATGGGTTCGTGAATATAGCCATCCAACGTGGACAATAAGATGAGCTTTATAGTTTCCGATCCTCATGGCGATCGAATAAGATCTATCCGCTTGTGTGTGTACGAGTCGCCGACTAACCGGTCTTGGGATATATACGTCACAGATTAAGTACTCGTCACGAGCTTGAATGGGAAGATAAGTAGACTCTTGTCGGGCACACACAGAGACTCCGACGCATCGAGATCGCAAACACTGCCTCCAGCCGGGGGATGCTAATCGTCGCGGTCGGTCCGAGCTTTATTCTACATCGTGGTGTTTCCGACCGAGCCATAAGAACAGTGTCCAAGTCACAAGAGGAGCACGCGGTGGAGGTCGTTCGCTATACAATATATTTGCAACTGTGTCTGGCATCACGCGCATTTCTCACACTTCCAAACGTGCTGCATTCTAAATGATTTCATGAATAGATTGTCTACTAGTTCACCCAAGGTATTACAGCACTGGTCATGTGCCGCTCTGGCACGGCTAGTATCAGGGCCGACTGTGTCCTAGGCGGCTGTTTTCGGGAGCCCAAGGGAAGCAATCAATGCGTTGACTGACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGATGACCCTAGGGCGGGCTGTTTGAGTGGGCTATCGGCGACCATTTCGCCCCGCAAGCCCCCGTCACGATACCGAGACCCTGAAGCTCATAAACGCCTATCTTTGTTGCATGAACAACGGGAGTAAGCGAGGCCAGGCCATACGGTTTCGGAGCCGCAGAATAGCCTTTACACGACCTCTACACAACCCAAAGTGAATATCCACGGGGTATTGTTTGTGCTGCTACCATGCGCAGTCAACATCGCCCACCGGCGATGTGTTTCAGATCTGCAGGCCCATCAACCGTTGTGACACCACCCCGGCTTTCAGAAGCAGTATGTCGGACACATTGACCTGTAGCGTTAGTTCTGTACAAGGGACCCTGCTCACTCGAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTTGGGAATCTAATGCGGTCTGCCATGGGACCCCTAACAACAAGGGACGCCTCCACCTGTCTAGGAGGAAAGACTTTACACACATCTTCTAGTTTCGAGAAGCACCGTAGCCAGTGGACCCTGAGTGGTTACAAACAAATCGCAGTTTAGCGCTTACCGACAAAGGCGGGAGCTTCGTTCACATTAGGATTGAAAGAACTTAAGAGTCTGTAGGCTCGGAGGTCTCTATATATACCATCTAGTCGTCCGGGGCATGATTAACTAAGAGTTGATCTGAGTCGGAACATAATGCCTGATCTGACCCCAATTCACTACGGTCGCACGTTCCGGGAACACCTACCGATCAGTCCGGAACTGTGACCTAAGAAGTCTCAAGCCTTTACGTCAATGTTCCCGGTGAAGGACTGTGTAACGGTCGCCTTCGCGCCCCCCCATAGGCCGGTCCTTCTCGTTGCAGGATAGCTAAGTCCCATATAGAGTTGTTGGTGTACCATTACGCTGATTTTACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTGGTGTGTTCAACTCAGCATACCCGGTTAGTCTGGAGCACTCCCCGTGCCTACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTGCCGAAATCCTTGTCAAGTAGTGGCATCTACTGCCGCGGGGCAGGACTGATGCTGACCCAAGACCACGCTCCTATCAGCCGGTGGCGCATCAGGGTGGGCTATAAGTTATATTCCTACTGTACGGCTGAAGTCAGCTGTAGTCAGGGAGCGGTTCCTGAGCCGGCTGATTCCGCTCGTAATGCGCTATGTAGAAGCATAGTTAGCCTCGCGCTCGTGTGTGGGCAGTCGTATAAGTAGTTTAGCTCCCGATGCGAAGGAGTTGCAAGTACCTACAAACTCGTAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGTCCGGTTCATATTAACCATGCACCAAGGTTTGACTAAATCAACTCGTGGGAATCCGACGTGACAAAATCCCCAGATATGCCGGGGGTGCACGTGAATACGTCGTAAGTTGAGCGTCCTATGACGGGAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGCCAAAGTAATACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGAATCCTTGACTGGCCTGCCGAGTGTTATCTCGCTGCTATCCCCCCCCAAGGTAGAAATGGAAGTGGGATCCAGCGCACCAAGGCACTTCACACAGGCATTACCCCAGCACCACGAATTAGCTTGCAGCTAAAGACAGGGTATTTTACGGAGTATATGATCTCTGTGAGGTACCGTATTCACACATCGTGGGATGTCTGCCATGAGCTTTTCCATTAGTATCCGGCGAGTTTTGATCCAAGTTACCAAACAAGGTTGTCCTCCAGGTCCTACGTGCTGAACGGCCAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGCCGGATCGGCCCTGACTCAAGTAAGGTCTGGTTGCTTGTCACTACATAAAGCCACGGAAGGGTGCGCGGCCCCAAAGCTGCGTCCGGATTCGACTCCCGTTTGCCTGGCTTCTCGACGAATCTAACGTTCTCATTAACCGAAAACCCTGAGCGGCTTAACCTCATTCGTCCCAGAATCAAACCCATCGTGTATCACCGTTGGCCCAGCAGGGAAGACAAGACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTGTGGCTCCCCAACCGAAGAATAAGATCCCTTCGCCGCCACAGAAGCAACACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGATTTAAAGTCTACCGTGGGGAGCCGGACGAGAACAAGACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGTAGGCGGCTACCTTCTGCCCATATCTCGGAATCCTTAGGGTCTTTAGCTGCTGGCAACACGGGGATGCCTTAGTCGCGGGGGAGCCGTTAGATCGGTTTCAGACTTGCCGACACCGTTCACCGTGGCCGGCCAACCGGCCGGTTCTGTGCTCCACTGAGTTTAGATAGGAATCCATACCTATAGTTTTACGTACACCAACTGGTTAACAAGCCGTCTCCGCGATGACAAACGGTGGGGGCACGAGCTCGAGGTAAGAGGTTGCGATCCGATTACAATGTATGACTACTTATAATGGTCTTACCTTAAATAGGGAACGGGTTTACAGATTACATGTCGGCGAAGACGTTACTGTATTTCGGCCAATGAGCAAATTCCCACCAGGCTCGCTCGGCTTAAATAGAATAGTCAGATTGGCTCTGAATGCTTTGGGCGTGCATTGAGAGCAGCCATATGTAATATTAAATGGCAGTACAAATCATACAGTTCAGAACTGCCGACAGCGCAGGAGTTTAAGGGTATCGAATATTGCGCTATCCGTGAGTGCTCTTAGCGATGGGGGGGCGGACCCTAAGTCTGACCCCCTCTCCTACCTTCTACGGATTACTATTATTGGCACTTGATGAGTAATCATTTCTAGCAAGAGTCTTATAAGGTAAACAATAACTTAGTAAGTGAGTCATGTAGTGTGCTTCCAGGACGAGTCGGCAAACTCTGTAGTCTTATGCTCATGTCTGACCTGCTGTGCCCAAAATTCTCTTCGTAAGGAGGGCTTTATAATGTTATGGGCACGACTTCGCATTGGGTCCACGCCCCAGGACTTCAGCATGTTATTTTGGGTTGCAGGATTTAAGAGAGCCTCATGCGTTGATAAGCCAAAGTGGGGGTATGGTGGGACCTCTCACCATGAGAGTTAAGTTAACTCACCGTGGCTCAAAAAAAGCTGGTTAGAATCTGCGAGTAATACGAGCGGGAAAATCTGGAATAACAGAAGCGACACCCTGACCTACAGTCGTTCAGTACTAGGTTACAAGTGAACCACTCGCGGATATAGTCAGGCGGGGATGTCCCGCGCGTTGATTAGACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGCGAGTTAATTGAAGTTTGCCTAGACACCGCTGAGGCTGGTTCGACATACCCTTAGGGAGGCCAAGCTATATAAAACCAAGATCATTGACCCCCTACGTGATACGTGATTTCAAACTTTACAATCATTAGGGTCGCCAGTGGAGAATCTATAGAATCTTTTCTACAGGCTACAGAGAAGCATTTTTCACAGGACCGCGTGGCGCAAACAATCCGATGGGGACCATCTGTGAACTCCCATACGTGACTATTCTGTGTCACATGAGGGGAGCTAGGGGGATTGAGTGCTCATGTCGGTTGGAGACCATTTTGAGTGCACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGCGAAGCATACTTACCTTGATCAACGCAGTGATTATTCATCTGAAGAGGATTGGGATAATACTGCGAACATATTGGAAAATTAACTGATTTATCTTCTGATCGATTCCCACACTCCACGAATTGGGGTGCCATGCTCCCATAGTAGGCCCTAGAGATGCCGATCATTCCGCAGGTGTGCCTAAGTGGACAGTCACTTGGCACTTAGGCCAATAAGTACAACAAAGGGATCAGTGGGCAAATTATCAGCGTACAATTCCCAGATATATAGGCGGCGAGAAAAGCTTCAAAAGACTTAATTTACTAGCCTCCTACAAACTCTAGATGAGGATTGGCTCTTGATGCTAGCGTTTTCATTTTCCATTACAAGACATTAGGCTGATAATTGCAGAGATTGGCGGCGTAGACTGACAGTCGCGATCAATCTGCGTGTTA

#############################################

def find_start(graph):
    in_degrees = {}
    out_degrees = {}
    elements = set()
        
    for key, value in graph.items():
        elements.add(key)
        elements.update(value)
    # print(elements)
    
    in_degrees = {element: 0 for element in elements}
    out_degrees = {element: 0 for element in elements}
    
    for key, value in graph.items():
        for element in elements:    
            if element == key:
                out_degrees[element] += 1
            if element == value[0]:
                in_degrees[element] += 1

    # for node, in_degree in in_degrees.items():
    #     out_degree = out_degrees[node]
    #     print(f"Node: {node}, In-Degree: {in_degree}, Out-Degree: {out_degree}")
    
    for element in elements:
        if in_degrees[element] > out_degrees[element]:
            start_node = element

    # print(start_node)
    return start_node

#############################################

def eulerian_path(graph, start_node):
    stack = []
    stack.append(start_node)

    while stack:
        current_node = stack[-1]
        
        for key, value in graph.items():
            if current_node in value:
                stack.append(key)
                break
        else:
            break
    # print(stack)
    
    pattern01 = stack[0][0][::-1]
    pattern02 = stack[0][1][::-1]

    for node in stack[1:]:
        pattern01 += node[0][0]
        pattern02 += node[1][0]

    pattern01 = pattern01[::-1]
    pattern02 = pattern02[::-1]
    
    #########################################
    
    overlap_length = 0
    
    for i in range(1, min(len(pattern01), len(pattern02))):
        if pattern01[-i:] == pattern02[:i]:
            overlap_length = i
    path = pattern01 + pattern02[overlap_length:]
    
    return path

#################################################

with open('bioinfo2/rosalind_ba3j.txt') as file:
    kmer, gap = map(int, file.readline().split())
    pattern_dict = [(line.strip().split('|')[0], line.strip().split('|')[1]) for line in file]

# print(pattern_dict)

DBG = (kmius1_DeBruijn(pattern_dict))

### 검산용
# print(check_patterns_in_graph(pattern_dict, DBG))

print(eulerian_path(DBG, find_start(DBG)))
