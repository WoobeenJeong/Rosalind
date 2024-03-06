
### LRS = longest repeated substring

### 유사 Suffix array를 만든 효과 -> suffixes를 정렬하면, 인접한 suffixes는 prefix가 겹치는 것을 활용
### 즉 Suffix 조합 다 찾아보지 않겠다는 의미
### 원리가 제대로 보고싶다면, print 찍은것

### 이건 그냥 두 suffix중에서 일치하는 최대 앞부분 반환하는 도구

def max_prefix(suf1, suf2):
    common_prefix = ''
    for i in range(min(len(suf1), len(suf2))):
        if suf1[i] == suf2[i]:
            common_prefix += suf1[i]
        else:
            break
    return common_prefix

### 34번째가 핵심인게, i와 i-1 혹은 i+1을 비교해서 바로 옆의 suffix랑 최대로 겹치는 서열이 뭔지 보는거임

def LRS(string):
    suffixes = []
    longest = ''
    
    for i in range(len(string)):
        suffixes.append(string[i:])
    suffixes.sort()
    # print(suffixes)           # 데이터 크면 출력 오류나니까, 이 print는 sample만
    # print(len(suffixes))
    
    for i in range(len(string)-1):
        candidate = max_prefix(suffixes[i],suffixes[i-1])
        # print(f'{i}: {candidate}')                            # 이 print도 마찬가지로 sample에서만 확인
        if len(candidate) > len(longest) and candidate in string:
            longest = candidate
            # print(longest)
        
    return longest

with open ('bioinfo2/rosalind_ba9d.txt','r') as f:
    string = f.readline().strip() 
    # print(string) 
    # print(len(string))

print(LRS(string))
