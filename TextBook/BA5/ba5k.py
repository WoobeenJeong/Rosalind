### middle edge in linear space
### space efficient alignment
### Divide and Conquer로 풀기 위한 준비!

### 핵심 포인트 : middle edge까지 source ~ middle 합과 middle ~ sink 합이 동일
### 때문에 한 column씩 계산 가능 (i,middle) -> i path중 최대 점수로 선택 가능

### 즉, 반반으로 쪼개서 한 column씩 모든 path에 대해 계산한 값을 구하겠다는 의미
## 대신 경로합이 middle path가 되는 i번째 에서는 같으니까 그냥 더해주면 됨 (구별도 쉽고, 계산도 쉬움)

import numpy as np

with open('bioinfo2/BLOSUM62.txt', 'r') as file:
    lines = file.readlines()
    blosum62 = []
    aa = lines[0].strip().split()[0:]
    for line in lines[1:]:
        row = [int(x) for x in line.strip().split()[1:]]
        blosum62.append(row)
    
def scoring(aa, blosum62, ref, alt, indel):
    before = np.zeros((len(ref) + 1), dtype=np.int64)                           # 이전, 이후 두 column의 값을 저장
    after = np.arange(0, -indel * (len(ref) + 1), -indel, dtype=np.int64)
    backtrack = np.zeros((len(ref) + 1), dtype=np.int8)                         # backtrack으로 어디서 왔는지 기록(0:source, 1:middle, 2:sink)
    # print(before, after, backtrack)
    
    for i, inext in enumerate(alt, 1):                                          
        before, after = after, before                                           # 이전, 이후 column을 바꿔가며 계산
        after[0] = -indel * i                                                   # 바뀐 이후 column의 첫번째 값은 -indel * i (penalty위치 변경)
        # print(before, after, backtrack)
        
        for j, jnext in enumerate(ref, 1):
            match = before[j - 1] + blosum62[aa.index(jnext)][aa.index(inext)]
            insertion = after[j - 1] - indel
            deletion = before[j] - indel
            after[j] = max(match, insertion, deletion)

            if after[j] == match:
                backtrack[j] = 2
            elif after[j] == insertion:
                backtrack[j] = 1
            else:
                backtrack[j] = 0

    # print(before, after, backtrack)  
    return after, backtrack                              # sink에서 source로 가는 path의 최대값 절반과, 그 path를 구성하는 방향을 return

def middle_edge(ref, alt,aa, blosum62, indel):
    midpoint = len(alt) // 2
    
    source2m, _ = scoring(aa, blosum62, ref, alt[:midpoint], indel)                         # source -> middle 절반값
    m2sink, traceback = scoring(aa, blosum62, ref[::-1], alt[midpoint:][::-1], indel)       # middle -> sink 절반값, traceback
    total = source2m + m2sink[::-1]                                                         # source -> middle -> sink 절반값

    i = np.argmax(total)                                                                # source -> middle -> sink 절반값 중 최대값 index
    j = midpoint
    
    addscore = traceback[::-1][i]
    # print(addscore)
    
    if addscore == 0:
        k = i
        l = j + 1
    elif addscore == 1:
        k = i + 1
        l = j
    elif addscore == 2:
        k = i + 1
        l = j + 1

    return (i, j), (k, l)

############################################################################

with open('bioinfo2/rosalind_ba5k.txt', 'r') as file:
    lines = file.readlines()
    ref = lines[0].strip().split()[0]
    alt = lines[1].strip().split()[0]

result = middle_edge(ref, alt, aa, blosum62, 5)
print(f'({result[0][0]},{result[0][1]}) ({result[1][0]},{result[1][1]})')
