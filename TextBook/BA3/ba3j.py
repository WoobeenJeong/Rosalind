### (k,d)mer paired 정보를 기반으로 string으로 reconstruct
### 두 kmer를 가지고 있지만, 두 kmer사이에 d만큼의 거리(unknown 서열) pair로부터
### 한마디로 gapped kmer pair -> string
### (k,d)-mer 에서 k는 kmer, d는 gap을 의미, 인덱싱

### 이것도 어떻게 하면 최적화되어 빠르게 여러 개의 kmer를 처리할 수 있을까가 관건

### 내가 생각한 logic : DeBruijn graph를 만들어서 Eulerian path를 찾고, 그걸로 reconstruct

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

    return graph

def find_start(graph):
    for key, value in graph.items():
        if key not in graph.values():
            start_node = value
            print(start_node)
            break
                
    return start_node[0]

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

with open('bioinfo2/sample.txt') as file:
    kmer, gap = map(int, file.readline().split())
    pattern_dict = [(line.strip().split('|')[0], line.strip().split('|')[1]) for line in file]

# print(pattern_dict)

DBG = (kmius1_DeBruijn(pattern_dict))

print(eulerian_path(DBG, find_start(DBG)))

GAAAGGTACAAATACTGGCGACCTCGCTGTTCGACACTTCATCACTGCTCCGGGGCGCTCAGGAGGGACGGTTCCCTGTACCATTGGAAGTCAATAGTCTAAGGTACAAAGAGAAGACCCGACCCGACAGAGGGGGTTCTGCGCCGGGTTTCGAGCTTGTAACCCCCCAGAGAATTAGATCCACCGTCTGTGTGGACAAAGTAGTAAAGCTAGCATACCAAATTGAAATTCGGAGTTTGACTACCAGATCCACGCATACGCTGCACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTAGAAATTCAGAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGGGGGTAATTCGTAGTTAGGTACAGAAAACTCCCGGACAGAACCGCATATAACCGATGAAGCAAGGGTTCTTCATTTAATACGACCCTAACCGGTATTGCTGCTAGCTTGATTTTCCTAGCAATCTAAACTCTATGTATGAGGCCACTCGGACGCCCGCTAGTGCCGGCAGCTAGCTACTGCCCTTCACCAGGAGCACGCACTATGCCTATCGGGCAATGCTGATCATACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGATCCCTCTGCAGAAAGCGGTGGCGGCGGGTCTAAGCAAGTCCAACGCAATACCAGGAAATCACCGTATCGTTAGCGACCAGTAGGTGATGGTTTGTAAGTTCGGACTACAGGCGGATGTGTCCCCGCCAGTTAAAAGTCGACTTTCTGTTACAACTGCTCCCTACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTCTAATGATCCCCACAGATCGTGTTTCAACGTTGAAGTCTGAATGGGTTCGTGAATATAGCCATCCAACGTGGACAATAAGATGAGCTTTATAGTTTCCGATCCTCATGGCGATCGAATAAGATCTATCCGCTTGTGTGTGTACGAGTCGCCGACTAACCGGTCTTGGGATATATACGTCACAGATTAAGTACTCGTCACGAGCTTGAATGGGAAGATAAGTAGACTCTTGTCGGGCACACACAGAGACTCCGACGCATCGAGATCGCAAACACTGCCTCCAGCCGGGGGATGCTAATCGTCGCGGTCGGTCCGAGCTTTATTCTACATCGTGGTGTTTCCGACCGAGCCATAAGAACAGTGTCCAAGTCACAAGAGGAGCACGCGGTGGAGGTCGTTCGCTATACAATATATTTGCAACTGTGTCTGGCATCACGCGCATTTCTCACACTTCCAAACGTGCTGCATTCTAAATGATTTCATGAATAGATTGTCTACTAGTTCACCCAAGGTATTACAGCACTGGTCATGTGCCGCTCTGGCACGGCTAGTATCAGGGCCGACTGTGTCCTAGGCGGCTGTTTTCGGGAGCCCAAGGGAAGCAATCAATGCGTTGACTGACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGATGACCCTAGGGCGGGCTGTTTGAGTGGGCTATCGGCGACCATTTCGCCCCGCAAGCCCCCGTCACGATACCGAGACCCTGAAGCTCATAAACGCCTATCTTTGTTGCATGAACAACGGGAGTAAGCGAGGCCAGGCCATACGGTTTCGGAGCCGCAGAATAGCCTTTACACGACCTCTACACAACCCAAAGTGAATATCCACGGGGTATTGTTTGTGCTGCTACCATGCGCAGTCAACATCGCCCACCGGCGATGTGTTTCAGATCTGCAGGCCCATCAACCGTTGTGACACCACCCCGGCTTTCAGAAGCAGTATGTCGGACACATTGACCTGTAGCGTTAGTTCTGTACAAGGGACCCTGCTCACTCGAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTTGGGAATCTAATGCGGTCTGCCATGGGACCCCTAACAACAAGGGACGCCTCCACCTGTCTAGGAGGAAAGACTTTACACACATCTTCTAGTTTCGAGAAGCACCGTAGCCAGTGGACCCTGAGTGGTTACAAACAAATCGCAGTTTAGCGCTTACCGACAAAGGCGGGAGCTTCGTTCACATTAGGATTGAAAGAACTTAAGAGTCTGTAGGCTCGGAGGTCTCTATATATACCATCTAGTCGTCCGGGGCATGATTAACTAAGAGTTGATCTGAGTCGGAACATAATGCCTGATCTGACCCCAATTCACTACGGTCGCACGTTCCGGGAACACCTACCGATCAGTCCGGAACTGTGACCTAAGAAGTCTCAAGCCTTTACGTCAATGTTCCCGGTGAAGGACTGTGTAACGGTCGCCTTCGCGCCCCCCCATAGGCCGGTCCTTCTCGTTGCAGGATAGCTAAGTCCCATATAGAGTTGTTGGTGTACCATTACGCTGATTTTACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTGGTGTGTTCAACTCAGCATACCCGGTTAGTCTGGAGCACTCCCCGTGCCTACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTGCCGAAATCCTTGTCAAGTAGTGGCATCTACTGCCGCGGGGCAGGACTGATGCTGACCCAAGACCACGCTCCTATCAGCCGGTGGCGCATCAGGGTGGGCTATAAGTTATATTCCTACTGTACGGCTGAAGTCAGCTGTAGTCAGGGAGCGGTTCCTGAGCCGGCTGATTCCGCTCGTAATGCGCTATGTAGAAGCATAGTTAGCCTCGCGCTCGTGTGTGGGCAGTCGTATAAGTAGTTTAGCTCCCGATGCGAAGGAGTTGCAAGTACCTACAAACTCGTAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGTCCGGTTCATATTAACCATGCACCAAGGTTTGACTAAATCAACTCGTGGGAATCCGACGTGACAAAATCCCCAGATATGCCGGGGGTGCACGTGAATACGTCGTAAGTTGAGCGTCCTATGACGGGAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGCCAAAGTAATACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGAATCCTTGACTGGCCTGCCGAGTGTTATCTCGCTGCTATCCCCCCCCAAGGTAGAAATGGAAGTGGGATCCAGCGCACCAAGGCACTTCACACAGGCATTACCCCAGCACCACGAATTAGCTTGCAGCTAAAGACAGGGTATTTTACGGAGTATATGATCTCTGTGAGGTACCGTATTCACACATCGTGGGATGTCTGCCATGAGCTTTTCCATTAGTATCCGGCGAGTTTTGATCCAAGTTACCAAACAAGGTTGTCCTCCAGGTCCTACGTGCTGAACGGCCAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGCCGGATCGGCCCTGACTCAAGTAAGGTCTGGTTGCTTGTCACTACATAAAGCCACGGAAGGGTGCGCGGCCCCAAAGCTGCGTCCGGATTCGACTCCCGTTTGCCTGGCTTCTCGACGAATCTAACGTTCTCATTAACCGAAAACCCTGAGCGGCTTAACCTCATTCGTCCCAGAATCAAACCCATCGTGTATCACCGTTGGCCCAGCAGGGAAGACAAGACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTGTGGCTCCCCAACCGAAGAATAAGATCCCTTCGCCGCCACAGAAGCAACACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGATTTAAAGTCTACCGTGGGGAGCCGGACGAGAACAAGACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGTAGGCGGCTACCTTCTGCCCATATCTCGGAATCCTTAGGGTCTTTAGCTGCTGGCAACACGGGGATGCCTTAGTCGCGGGGGAGCCGTTAGATCGGTTTCAGACTTGCCGACACCGTTCACCGTGGCCGGCCAACCGGCCGGTTCTGTGCTCCACTGAGTTTAGATAGGAATCCATACCTATAGTTTTACGTACACCAACTGGTTAACAAGCCGTCTCCGCGATGACAAACGGTGGGGGCACGAGCTCGAGGTAAGAGGTTGCGATCCGATTACAATGTATGACTACTTATAATGGTCTTACCTTAAATAGGGAACGGGTTTACAGATTACATGTCGGCGAAGACGTTACTGTATTTCGGCCAATGAGCAAATTCCCACCAGGCTCGCTCGGCTTAAATAGAATAGTCAGATTGGCTCTGAATGCTTTGGGCGTGCATTGAGAGCAGCCATATGTAATATTAAATGGCAGTACAAATCATACAGTTCAGAACTGCCGACAGCGCAGGAGTTTAAGGGTATCGAATATTGCGCTATCCGTGAGTGCTCTTAGCGATGGGGGGGCGGACCCTAAGTCTGACCCCCTCTCCTACCTTCTACGGATTACTATTATTGGCACTTGATGAGTAATCATTTCTAGCAAGAGTCTTATAAGGTAAACAATAACTTAGTAAGTGAGTCATGTAGTGTGCTTCCAGGACGAGTCGGCAAACTCTGTAGTCTTATGCTCATGTCTGACCTGCTGTGCCCAAAATTCTCTTCGTAAGGAGGGCTTTATAATGTTATGGGCACGACTTCGCATTGGGTCCACGCCCCAGGACTTCAGCATGTTATTTTGGGTTGCAGGATTTAAGAGAGCCTCATGCGTTGATAAGCCAAAGTGGGGGTATGGTGGGACCTCTCACCATGAGAGTTAAGTTAACTCACCGTGGCTCAAAAAAAGCTGGTTAGAATCTGCGAGTAATACGAGCGGGAAAATCTGGAATAACAGAAGCGACACCCTGACCTACAGTCGTTCAGTACTAGGTTACAAGTGAACCACTCGCGGATATAGTCAGGCGGGGATGTCCCGCGCGTTGATTAGACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGCGAGTTAATTGAAGTTTGCCTAGACACCGCTGAGGCTGGTTCGACATACCCTTAGGGAGGCCAAGCTATATAAAACCAAGATCATTGACCCCCTACGTGATACGTGATTTCAAACTTTACAATCATTAGGGTCGCCAGTGGAGAATCTATAGAATCTTTTCTACAGGCTACAGAGAAGCATTTTTCACAGGACCGCGTGGCGCAAACAATCCGATGGGGACCATCTGTGAACTCCCATACGTGACTATTCTGTGTCACATGAGGGGAGCTAGGGGGATTGAGTGCTCATGTCGGTTGGAGACCATTTTGAGTGCACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGCGAAGCATACTTACCTTGATCAACGCAGTGATTATTCATCTGAAGA
GAAAGGTACAAATACTGGCGACCTCGCTGTTCGACACTTCATCACTGCTCCGGGGCGCTCAGGAGGGACGGTTCCCTGTACCATTGGAAGTCAATAGTCTAAGGTACAAAGAGAAGACCCGACCCGACAGAGGGGGTTCTGCGCCGGGTTTCGAGCTTGTAACCCCCCAGAGAATTAGATCCACCGTCTGTGTGGACAAAGTAGTAAAGCTAGCATACCAAATTGAAATTCGGAGTTTGACTACCAGATCCACGCATACGCTGCACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTAGAAATTCAGAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGGGGGTAATTCGTAGTTAGGTACAGAAAACTCCCGGACAGAACCGCATATAACCGATGAAGCAAGGGTTCTTCATTTAATACGACCCTAACCGGTATTGCTGCTAGCTTGATTTTCCTAGCAATCTAAACTCTATGTATGAGGCCACTCGGACGCCCGCTAGTGCCGGCAGCTAGCTACTGCCCTTCACCAGGAGCACGCACTATGCCTATCGGGCAATGCTGATCATACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGATCCCTCTGCAGAAAGCGGTGGCGGCGGGTCTAAGCAAGTCCAACGCAATACCAGGAAATCACCGTATCGTTAGCGACCAGTAGGTGATGGTTTGTAAGTTCGGACTACAGGCGGATGTGTCCCCGCCAGTTAAAAGTCGACTTTCTGTTACAACTGCTCCCTACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTCTAATGATCCCCACAGATCGTGTTTCAACGTTGAAGTCTGAATGGGTTCGTGAATATAGCCATCCAACGTGGACAATAAGATGAGCTTTATAGTTTCCGATCCTCATGGCGATCGAATAAGATCTATCCGCTTGTGTGTGTACGAGTCGCCGACTAACCGGTCTTGGGATATATACGTCACAGATTAAGTACTCGTCACGAGCTTGAATGGGAAGATAAGTAGACTCTTGTCGGGCACACACAGAGACTCCGACGCATCGAGATCGCAAACACTGCCTCCAGCCGGGGGATGCTAATCGTCGCGGTCGGTCCGAGCTTTATTCTACATCGTGGTGTTTCCGACCGAGCCATAAGAACAGTGTCCAAGTCACAAGAGGAGCACGCGGTGGAGGTCGTTCGCTATACAATATATTTGCAACTGTGTCTGGCATCACGCGCATTTCTCACACTTCCAAACGTGCTGCATTCTAAATGATTTCATGAATAGATTGTCTACTAGTTCACCCAAGGTATTACAGCACTGGTCATGTGCCGCTCTGGCACGGCTAGTATCAGGGCCGACTGTGTCCTAGGCGGCTGTTTTCGGGAGCCCAAGGGAAGCAATCAATGCGTTGACTGACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGATGACCCTAGGGCGGGCTGTTTGAGTGGGCTATCGGCGACCATTTCGCCCCGCAAGCCCCCGTCACGATACCGAGACCCTGAAGCTCATAAACGCCTATCTTTGTTGCATGAACAACGGGAGTAAGCGAGGCCAGGCCATACGGTTTCGGAGCCGCAGAATAGCCTTTACACGACCTCTACACAACCCAAAGTGAATATCCACGGGGTATTGTTTGTGCTGCTACCATGCGCAGTCAACATCGCCCACCGGCGATGTGTTTCAGATCTGCAGGCCCATCAACCGTTGTGACACCACCCCGGCTTTCAGAAGCAGTATGTCGGACACATTGACCTGTAGCGTTAGTTCTGTACAAGGGACCCTGCTCACTCGAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTTGGGAATCTAATGCGGTCTGCCATGGGACCCCTAACAACAAGGGACGCCTCCACCTGTCTAGGAGGAAAGACTTTACACACATCTTCTAGTTTCGAGAAGCACCGTAGCCAGTGGACCCTGAGTGGTTACAAACAAATCGCAGTTTAGCGCTTACCGACAAAGGCGGGAGCTTCGTTCACATTAGGATTGAAAGAACTTAAGAGTCTGTAGGCTCGGAGGTCTCTATATATACCATCTAGTCGTCCGGGGCATGATTAACTAAGAGTTGATCTGAGTCGGAACATAATGCCTGATCTGACCCCAATTCACTACGGTCGCACGTTCCGGGAACACCTACCGATCAGTCCGGAACTGTGACCTAAGAAGTCTCAAGCCTTTACGTCAATGTTCCCGGTGAAGGACTGTGTAACGGTCGCCTTCGCGCCCCCCCATAGGCCGGTCCTTCTCGTTGCAGGATAGCTAAGTCCCATATAGAGTTGTTGGTGTACCATTACGCTGATTTTACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTGGTGTGTTCAACTCAGCATACCCGGTTAGTCTGGAGCACTCCCCGTGCCTACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTGCCGAAATCCTTGTCAAGTAGTGGCATCTACTGCCGCGGGGCAGGACTGATGCTGACCCAAGACCACGCTCCTATCAGCCGGTGGCGCATCAGGGTGGGCTATAAGTTATATTCCTACTGTACGGCTGAAGTCAGCTGTAGTCAGGGAGCGGTTCCTGAGCCGGCTGATTCCGCTCGTAATGCGCTATGTAGAAGCATAGTTAGCCTCGCGCTCGTGTGTGGGCAGTCGTATAAGTAGTTTAGCTCCCGATGCGAAGGAGTTGCAAGTACCTACAAACTCGTAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGTCCGGTTCATATTAACCATGCACCAAGGTTTGACTAAATCAACTCGTGGGAATCCGACGTGACAAAATCCCCAGATATGCCGGGGGTGCACGTGAATACGTCGTAAGTTGAGCGTCCTATGACGGGAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGCCAAAGTAATACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGAATCCTTGACTGGCCTGCCGAGTGTTATCTCGCTGCTATCCCCCCCCAAGGTAGAAATGGAAGTGGGATCCAGCGCACCAAGGCACTTCACACAGGCATTACCCCAGCACCACGAATTAGCTTGCAGCTAAAGACAGGGTATTTTACGGAGTATATGATCTCTGTGAGGTACCGTATTCACACATCGTGGGATGTCTGCCATGAGCTTTTCCATTAGTATCCGGCGAGTTTTGATCCAAGTTACCAAACAAGGTTGTCCTCCAGGTCCTACGTGCTGAACGGCCAACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGCCGGATCGGCCCTGACTCAAGTAAGGTCTGGTTGCTTGTCACTACATAAAGCCACGGAAGGGTGCGCGGCCCCAAAGCTGCGTCCGGATTCGACTCCCGTTTGCCTGGCTTCTCGACGAATCTAACGTTCTCATTAACCGAAAACCCTGAGCGGCTTAACCTCATTCGTCCCAGAATCAAACCCATCGTGTATCACCGTTGGCCCAGCAGGGAAGACAAGACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGTGTGGCTCCCCAACCGAAGAATAAGATCCCTTCGCCGCCACAGAAGCAACACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGATTTAAAGTCTACCGTGGGGAGCCGGACGAGAACAAGACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGTAGGCGGCTACCTTCTGCCCATATCTCGGAATCCTTAGGGTCTTTAGCTGCTGGCAACACGGGGATGCCTTAGTCGCGGGGGAGCCGTTAGATCGGTTTCAGACTTGCCGACACCGTTCACCGTGGCCGGCCAACCGGCCGGTTCTGTGCTCCACTGAGTTTAGATAGGAATCCATACCTATAGTTTTACGTACACCAACTGGTTAACAAGCCGTCTCCGCGATGACAAACGGTGGGGGCACGAGCTCGAGGTAAGAGGTTGCGATCCGATTACAATGTATGACTACTTATAATGGTCTTACCTTAAATAGGGAACGGGTTTACAGATTACATGTCGGCGAAGACGTTACTGTATTTCGGCCAATGAGCAAATTCCCACCAGGCTCGCTCGGCTTAAATAGAATAGTCAGATTGGCTCTGAATGCTTTGGGCGTGCATTGAGAGCAGCCATATGTAATATTAAATGGCAGTACAAATCATACAGTTCAGAACTGCCGACAGCGCAGGAGTTTAAGGGTATCGAATATTGCGCTATCCGTGAGTGCTCTTAGCGATGGGGGGGCGGACCCTAAGTCTGACCCCCTCTCCTACCTTCTACGGATTACTATTATTGGCACTTGATGAGTAATCATTTCTAGCAAGAGTCTTATAAGGTAAACAATAACTTAGTAAGTGAGTCATGTAGTGTGCTTCCAGGACGAGTCGGCAAACTCTGTAGTCTTATGCTCATGTCTGACCTGCTGTGCCCAAAATTCTCTTCGTAAGGAGGGCTTTATAATGTTATGGGCACGACTTCGCATTGGGTCCACGCCCCAGGACTTCAGCATGTTATTTTGGGTTGCAGGATTTAAGAGAGCCTCATGCGTTGATAAGCCAAAGTGGGGGTATGGTGGGACCTCTCACCATGAGAGTTAAGTTAACTCACCGTGGCTCAAAAAAAGCTGGTTAGAATCTGCGAGTAATACGAGCGGGAAAATCTGGAATAACAGAAGCGACACCCTGACCTACAGTCGTTCAGTACTAGGTTACAAGTGAACCACTCGCGGATATAGTCAGGCGGGGATGTCCCGCGCGTTGATTAGACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGCGAGTTAATTGAAGTTTGCCTAGACACCGCTGAGGCTGGTTCGACATACCCTTAGGGAGGCCAAGCTATATAAAACCAAGATCATTGACCCCCTACGTGATACGTGATTTCAAACTTTACAATCATTAGGGTCGCCAGTGGAGAATCTATAGAATCTTTTCTACAGGCTACAGAGAAGCATTTTTCACAGGACCGCGTGGCGCAAACAATCCGATGGGGACCATCTGTGAACTCCCATACGTGACTATTCTGTGTCACATGAGGGGAGCTAGGGGGATTGAGTGCTCATGTCGGTTGGAGACCATTTTGAGTGCACAAGGGACCCTGCTCACTCGATTGGGAATCTAATGCGGTCTGCCATGGGGCGAAGCATACTTACCTTGATCAACGCAGTGATTATTCATCTGAAGA

GGATTGGGATAATACTGCGAACATATTGGAAAATTAACTGATTTATCTTCTGATCGATTCCCACACTCCACGAATTGGGGTGCCATGCTCCCATAGTAGGCCCTAGAGATGCCGATCATTCCGCAGGTGTGCCTAAGTGGACAGTCACTTGGCACTTAGGCCAATAAGTACAACAAAGGGATCAGTGGGCAAATTATCAGCGTACAATTCCCAGATATATAGGCGGCGAGAAAAGCTTCAAAAGACTTAATTTACTAGCCTCCTACAAACTCTAGATGAGGATTGGCTCTTGATGCTAGCGTTTTCATTTTCCATTACAAGACATTAGGCTGATAATTGCAGAGATTGGCGGCGTAGACTGACAGTCGCGATCAATCTGCGTGTTA
