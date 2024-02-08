### Gapped (k,d)mer Genome Path 
### kmer read 두개가 d만큼 차이를 두고 paired-end 되었을 때, genome 찾기
### 시퀀싱을 하면 read의 형태가 [kmer1-----kmer2] 꼴로 나옴
### paired end read의 필요성은 genome이 길고, 짧은 read로 중복없이 맵핑
### 반복서열(repetitive seq), 중복서열(duplicated seq), 융합(gene fusion), 새로운 전사물(novel transcript)용이

### 사실 ba3j로 풀 수 있음
### 단, 이번에는 (a1|b1), ... , (an|bn) 이고 Suffix(ai|bi) = Prefix(ai+1|bi+1)

#############################################
### (k-1) DBG 그리면, 순차적으로 연결됨을 확인

def kmius1_DeBruijn(pattern_dict):
    graph = {}
    for pre, post in pattern_dict:
        prefix = (pre[:-1], post[:-1])
        suffix = (pre[1:], post[1:])
        
        if prefix not in graph:
            graph[prefix] = []
        graph[prefix].append(suffix)

    return graph

#############################################

def graph2path(graph,kmer,gap):
    
    pattern01 = next(iter(graph.keys()))[0]
    pattern02 = next(iter(graph.keys()))[1]
    
    for key, value in graph.items():
        if key[0] == pattern01[-(kmer-1):]:
            pattern01 += value[0][0][-1]
        if key[1] == pattern02[-(kmer-1):]:
            pattern02 += value[0][1][-1]
        
    overlap_length = 0
    
    for i in range(1, min(len(pattern01), len(pattern02))):
        if pattern01[-i:] == pattern02[:i]:
            overlap_length = i
    path = pattern01 + pattern02[overlap_length:]
    
    return path

##############################################

with open('bioinfo2/rosalind_ba3l.txt') as file:
    kmer, gap = map(int, file.readline().split())
    pattern_dict = [(line.strip().split('|')[0], line.strip().split('|')[1]) for line in file]
    
graph = kmius1_DeBruijn(pattern_dict)
path = graph2path(graph, kmer, gap)
# print(graph)
print(path)
