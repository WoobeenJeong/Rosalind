### kmer patterns into original string
### 맨 하단 코드를 잘못 만들고
### +1 sliding window가정 + ordered가정으로 구현

def slide_1_merge(strings):
    final = strings[0]
    
    for i in range(1,len(strings)):
        if strings[i-1].endswith(strings[i][:-1]):
            final += strings[i][-1]
        else:
            break

    return final

with open("bioinfo2/rosalind_ba3b.txt","r") as f:
    strings = [line.strip() for line in f]

result = slide_1_merge(strings)

# print(len(strings[0])+len(strings)-1)       ## 검산용
# print(len(result))

print(result)

#############################################
### 잘못 만든 코드

### 일단 핵심은 가장 많은 overlap을 가지는 두 패턴 찾기
### 구현은 dictionary로 {패턴,겹치는 패턴:겹침끝 위치}
### 예시에서는 -1 sliding window가 주어졌지만, 좀 더 범용적이게
### endswith, startswith모두 시작, 끝을 보장하지 않는다 -> 가정 필요

### Assumetion 01: kmer의 길이가 다를 수 있다
### Assumetion 02: 적어도 1개의 겹치는 부분이 있다
### Assumetion 03: 겹치는 부분이 여러개일 경우, 가장 긴 부분을 선택한다 (종료 조건)

### 이게 없으면 이제 DAG문제가 되어버림

def find_overlap(strings):
    overlaps = []

    for start in strings:
        max_match = 0
        max_match_end = ""
        
        for end in strings:
            if end != start:
                
                for i in range(len(end)):
                    if end.startswith(start[i:]):
                        current_match = len(start[i:])
                        if current_match > max_match:
                            max_match = current_match
                            max_match_end = end
                        break
        overlaps.append((start, max_match_end, max_match))


    noloop = min(each[2] for each in overlaps)
    howmany = 0
    
    for each in overlaps:
        if each[2] == noloop:
            howmany += 1
            if howmany > 1:
                return "Tail cannot determine(Multiple overlaps)"
            else:
                overlaps.remove(each)
    
    # print(overlaps)
    return overlaps

def assemble(strings):
    overlaps = find_overlap(strings)
    starts = [each[0] for each in overlaps]
    ends = [each[1] for each in overlaps]
    total = starts + ends
    only = []
    final = ""

    for value in total:
        if total.count(value) == 1:
            only.append(value)

    for each in overlaps:
        if each[0] in only:
            final = each[0]

    for prev in overlaps:
        for post in overlaps:
            if prev[1] == post[1]:
                final += post[1][post[2]:]
    
    return final

#############################################
