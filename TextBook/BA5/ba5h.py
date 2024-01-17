### local align에서 global 맛 내기
### 일단 문제 의도는, 긴 서열 v와 짧은서열 w가 있는데
### global로 하면 v의 길이에 w를 맞추기만 해서 문제고
### local로 하면 v를 w에 맞춤과 동시에 w도 v에 맞춰버림

### 즉, local인데 v에 "일방적"으로 w를 맞추고자 함 -> semi-global 유사
### == global로 하되, 시작지점은 local처럼 찾기
### mismatch, indel penatly는 +1, match는 -1 (만들어진 매트릭스 잘 보기!)

import numpy as np

def scorematrix(ref,alt):
    score = np.zeros((len(alt)+1,len(ref)+1),dtype=int)
    # for i in range(1,len(alt)+1):
    #     score[i][0] = score[i-1][0] - 1
        
    for i in range(1,len(alt)+1):
        for j in range(1,len(ref)+1):
            score[i][j] = max(score[i-1][j-1] + (1 if alt[i-1] == ref[j-1] else - 1),
                            score[i-1][j] - 1,
                            score[i][j-1] - 1)
    return score
  
# print(scorematrix(ref,alt))

def start(ref, alt):
    i, j = len(alt), len(ref)
    score = scorematrix(ref, alt)
    
    max_score = []
    max_pos_candidate = []
    max_sum = []
    real_max_pos = []
    
    max_score.append(max(score[len(alt)]))
    for j in range(len(ref) + 1):
        if score[len(alt)][j] == max(score[len(alt)]):
            max_pos_candidate.append((len(alt), j))

    # print(max_score, max_pos_candidate)
    
    for i, j in max_pos_candidate:
        current = score[i][j]
        x, y = i, j

        while x > 0 and y > 0:
            if max(score[x-1][y-1], score[x-1][y], score[x][y-1]) == score[x-1][y-1]:
                current += score[x-1][y-1]
                x -= 1
                y -= 1
            elif max(score[x-1][y-1], score[x-1][y], score[x][y-1]) == score[x-1][y]:
                current += score[x-1][y]
                x -= 1
            elif max(score[x-1][y-1], score[x-1][y], score[x][y-1]) == score[x][y-1]:
                current += score[x][y-1]
                y -= 1
            else:
                break

        max_sum.append(current)

    real_max_pos = max_pos_candidate[max_sum.index(max(max_sum))]
    max_score = max(score[len(alt)])
    
    return max_score,real_max_pos

# print(start(ref,alt))

def traceback(ref, alt):
    max_score, real_max_pos = start(ref, alt)
    i, j = real_max_pos
    score= scorematrix(ref,alt)
    altseq = []
    refseq = []

    while i > 0 and j > 0:
        if score[i][j] == score[i - 1][j - 1] + (1 if alt[i-1] == ref[j-1] else - 1):
            altseq.append(alt[i - 1])
            refseq.append(ref[j - 1])
            i -= 1
            j -= 1
        elif score[i][j] == score[i - 1][j] - 1:
            altseq.append(alt[i - 1])
            refseq.append('-')
            i -= 1
        elif score[i][j] == score[i][j - 1] - 1:
            altseq.append('-')
            refseq.append(ref[j - 1])
            j -= 1

    return f"{max_score}\n{''.join(refseq[::-1])}\n{''.join(altseq[::-1])}"

with open ("bioinfo2/rosalind_ba5h.txt","r") as file:
    line = file.readlines()
    ref = line[0].strip()
    alt = line[1].strip()
    
# print(f"{ref,alt,len(ref),len(alt)}")
print(traceback(ref, alt))
