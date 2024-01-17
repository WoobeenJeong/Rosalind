### 이번엔 Overlap하는 서열을 DP로 확인하기
### 이 경우 이전과 다르게 global alignment를 수정해서 
### suffix - prefix 형태의 overlapping seq를 가장 길고, 점수 높은 서열로 가져 올 것임

import numpy as np

def scorematrix(ref, alt):
    score = np.zeros((len(ref) + 1, len(alt) + 1), dtype=int)

    for i in range(1, len(ref) + 1):
        for j in range(1, len(alt) + 1):
            match = score[i - 1][j - 1] + (1 if ref[i - 1] == alt[j - 1] else -2)
            delete = score[i - 1][j] - 2
            insert = score[i][j - 1] - 2
            score[i][j] = max(match, delete, insert, 0)

    return score

print(scorematrix(ref, alt))
    
def start(ref, alt):
    i, j = len(alt), len(ref)
    score = scorematrix(ref, alt)
    
    max_score = []
    max_pos_candidate = []
    max_sum = []
    real_max_pos = []
    
    max_score.append(max(score[len(ref)]))
    for j in range(len(alt) + 1):
        if score[len(ref)][j] == max(score[len(ref)]):
            max_pos_candidate.append((len(ref), j))

    # print(max_score, max_pos_candidate)
    
    for i, j in max_pos_candidate:
        current = score[i][j]
        x, y = i, j

        while x > 0 and y > 0:
            if max(score[x-1][y-1], score[x-1][y], score[x][y-1]) == score[x-1][y-1]:
                current += score[x-1][y-1]
                x -= 1
                y -= 1
            elif max(score[x-1][y-1], score[x-1][y]-2, score[x][y-1]-2) == score[x-1][y]:
                current += score[x-1][y]
                x -= 1
            elif max(score[x-1][y-1], score[x-1][y]-2, score[x][y-1]-2) == score[x][y-1]:
                current += score[x][y-1]
                y -= 1
            else:
                break

        max_sum.append(current)

    real_max_pos = max_pos_candidate[max_sum.index(max(max_sum))]
    max_score = max(score[len(ref)])
    
    return max_score, real_max_pos

print(start(ref,alt))

def traceback(ref,alt):
    i, j = start(ref,alt)[1]
    max_score = start(ref,alt)[0]
    score = scorematrix(ref, alt)
    refseq = []
    altseq = []
    
    while i > 0 and j > 0:
        if score[i][j] == 0:
            break
        if score[i][j] == score[i-1][j-1] + (1 if ref[i-1] == alt[j-1] else -2):
            refseq.append(ref[i-1])
            altseq.append(alt[j-1])
            i -= 1
            j -= 1
        elif score[i][j] == score[i-1][j] - 2:
            refseq.append(ref[i-1])
            altseq.append('-')
            i -= 1
        elif score[i][j] == score[i][j-1] - 2:
            refseq.append('-')
            altseq.append(alt[j-1])
            j -= 1
        else:
            break

    return f"{max_score}\n{''.join(refseq[::-1])}\n{''.join(altseq[::-1])}"

###########################################################

with open ("bioinfo2/rosalind_ba5i.txt","r") as file:
    line = file.readlines()
    ref = line[0].strip()
    alt = line[1].strip()

print(traceback(ref,alt))
