### kmers patterns into k-1 mers DeBruijn graph
### k-1 prefix suffix 통해서 원래 서열 (circuit 혹은 path) 찾기
### 주어진 pseudo code
### DeBruijn(Patterns)
###     kmer pattern사이의 prefix, suffix를 edge로 활용 = CompositionalGraph(kmers)라는 함수로 구현
###     동일 label을 갖는 노드를 이어붙여, DeBruijn graph 생성

### 여기서 CompositionalGraph(kmers) == overlaps(kmers, window) (ba3c.py)와 동일
### overlaps를 통해 gluing까지 된 상태임 (dictionary 형태로 찾아갈 수 있음) 

def overlaps(kmers, window):
    
    overlap_dict = {}
    
    for prefix in kmers:
        for suffix in kmers:
            if prefix != suffix and prefix[window:] == suffix[:-window]:
                if prefix not in overlap_dict:
                    overlap_dict[prefix] = [suffix]
                else:
                    overlap_dict[prefix].append(suffix)
    # print(overlap_dict)  
    
    return overlap_dict

### 이제 이 딕셔너리에서 어떻게 k-1 mers DeBruijn graph를 만들 것인가?
### 답은 간단한게, 동일한 label을 갖는 노드를 이어붙이면 됨
### 영어로 말이 어렵게 되있지만, 쉽게하자면 key값을 suffix와 prefix로 나눈 새로운 딕셔너리 생성

def DeBruijn_from_overlaps(patterns,windows):
    
    CompositionGraph_dict = overlaps(patterns, windows)
    count_dict = {}
    debruijn_dict = {}
    
    for prefix, suffix in CompositionGraph_dict.items():
        unique_suffix = set(suffix)
        if len(suffix) != len(unique_suffix):
            count = len(suffix)/len(unique_suffix)
        else:
            count = 1
        count_dict[prefix] = count
    
    # print(count_dict)
    
    for key, value in count_dict.items():
        prefix = key[:len(key)-window]
        suffix = key[-(len(key)-window):]
        new_key = {prefix : [suffix]*int(value)}
        
        debruijn_dict.update({k: debruijn_dict.get(k, []) + v for k, v in new_key.items()})
    
    return debruijn_dict 

### 위 과정을 더 쉽게 하자면 다음과 같이 할 수 있음
### 놀랍게도 결과는 동일하지만, 원리를 이해하자.

def DeBruijn(patterns, window):
    
    pattern_count_dict = {}
    debruijn_dict = {}
    
    for each in patterns:
        if each not in pattern_count_dict:
            pattern_count_dict[each] = 1
        else:
            pattern_count_dict[each] += 1
            
    # print(pattern_count_dict)
    
    for key, value in pattern_count_dict.items():
        prefix = key[:len(key)-window]
        suffix = key[-(len(key)-window):]
        new_key = {prefix : [suffix]*int(value)}
        
        debruijn_dict.update({k: debruijn_dict.get(k, []) + v for k, v in new_key.items()})
    
    return debruijn_dict


with open ('bioinfo2/rosalind_ba3e.txt', 'r') as f:
    # patterns = f.readlines()
    # patterns = [x.strip() for x in patterns]
    patterns = f.read().splitlines()
    window = 1
    
# print(patterns, window)

### 1번 결과 (원리 이해용)
# print(DeBruijn_from_overlaps(patterns, window))
### 2번 결과 (더 쉬운 방법)
# print(DeBruijn(patterns, window))

### 결과값 정렬
result = DeBruijn(patterns, window)
key_sort = sorted(result.keys())
result = {key: result[key] for key in key_sort}

#####################
### printing format

print('\n'.join([prefix + ' -> ' + ','.join(suffix) for prefix, suffix in result.items()]))

#####################
