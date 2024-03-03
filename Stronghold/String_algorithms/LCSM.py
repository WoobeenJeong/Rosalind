### find the longest shared motif
### 가장 길게 공통된 서열을 찾는 문제
### 최적 알고리즘은 suffix tree를 이용하는 것이지만, 
### 이 문제에서는 간단한 방법으로 풀 수 있다.

### 가장 짧은 서열을 기준으로, 모든 부분 서열을 찾아서
### 다른 서열에도 존재하는지 확인하는 방법을 사용한다.

def common_substr(dnaset):
    substr = ''

    # min_length = float('inf')
    # for string in dnaset:
    #     if len(string) < min_length:
    #         min_length = len(string)
    #         minimal = string    
    
    minimal = min(dnaset, key=len)         ### 위 코드를 한 줄로

    for i in range(len(minimal)):
        for j in range(len(minimal)-i+1):   
            candidate = minimal[i:i+j]
            # print(candidate)

            if j > len(substr):
                is_common = all(candidate in string for string in dnaset)
                if is_common:
                    substr = candidate

    return substr

#####################################

dnaset = []
with open('bioinfo2/rosalind_lcsm.txt', 'r') as file:
    strings = file.read().split('>')[1:]
    trimmed = lambda x: x.split('\n', 1)[1].replace('\n', '')
    dnaset = list(map(trimmed, strings))
    
# print(dnaset)

print(common_substr(dnaset)) 
