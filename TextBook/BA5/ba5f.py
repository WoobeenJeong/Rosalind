## 이번엔 PAM250을 사용해서, local alignment / 기존 ba5e.py (BLOSUM62 / global alignment) 활용

with open('bioinfo2/rosalind_ba5f.txt', 'r') as file:
    lines = file.readlines()
    ref = lines[0].strip()
    alt = lines[1].strip()

def scorematrix(aa, pam250, indel, ref, alt):
    score = [[0 for _ in range(len(ref) + 1)] for _ in range(len(alt) + 1)]
    max_score = 0
    max_i, max_j = 0, 0                                                 # 이 값을 가져오는 이유는, 나중에 traceback에서 거꾸로 올라가는 end서열을 위해

    for i in range(1, len(alt) + 1):
        for j in range(1, len(ref) + 1):
            score[i][j] = max(
                score[i - 1][j - 1] + pam250[aa.index(alt[i - 1])][aa.index(ref[j - 1])],
                score[i - 1][j] + indel,
                score[i][j - 1] + indel,
                0                                                       # local align의 핵심! 좀 더 compact하게 점화식 썼는데, 결국 penalty부여해서 0이하는 align안하고 무시
            )
            if score[i][j] > max_score:
                max_score = score[i][j]
                max_i, max_j = i, j

    # print(f"score:{score}, max_score:{max_score}")                     # 이건 좀 조심히 풀어야 하는게, score matrix가 어마무시하게 크므로, 작은 sample에서만 확인 용으로
    # print(f"score:{len(score)},{len(score[0])}, max_score:{max_score}")

    return score, max_score, max_i, max_j

def traceback(aa, pam250, indel, ref, alt):
    score_matrix, max_score, end_i, end_j = scorematrix(aa, pam250, indel, ref, alt)
    altseq = []
    refseq = []

    i, j = end_i, end_j                                                    # traceback의 종착지, 서열의 start점을 위해
    while i > 0 and j > 0 and score_matrix[i][j] > 0:
        if score_matrix[i][j] == score_matrix[i - 1][j - 1] + pam250[aa.index(alt[i - 1])][aa.index(ref[j - 1])]:
            i -= 1
            j -= 1
        elif score_matrix[i][j] == score_matrix[i - 1][j] + indel:
            i -= 1
        elif score_matrix[i][j] == score_matrix[i][j - 1] + indel:
            j -= 1
        else:
            break
    
    start_i, start_j = i, j             # 위 while문을 바탕으로 거슬러올라간 start점을 저장
    i, j = end_i, end_j                 # end점을 다시 불러와서 while문으로 이번엔 서열을 저장해야 함
    
    # print(f"start_i:{start_i}, start_j:{start_j}, end_i:{end_i}, end_j:{end_j}")
    
    while i > start_i and j > start_j:
        if score_matrix[i][j] == score_matrix[i - 1][j - 1] + pam250[aa.index(alt[i - 1])][aa.index(ref[j - 1])]:
            altseq.append(alt[i - 1])
            refseq.append(ref[j - 1])
            i -= 1
            j -= 1
        elif score_matrix[i][j] == score_matrix[i - 1][j] + indel:
            altseq.append(alt[i - 1])
            refseq.append('-')
            i -= 1
        elif score_matrix[i][j] == score_matrix[i][j - 1] + indel:
            altseq.append('-')
            refseq.append(ref[j - 1])
            j -= 1

    return f"{max_score}\n{''.join(refseq[::-1])}\n{''.join(altseq[::-1])}"

########################################################

with open('bioinfo2/PAM250.txt', 'r') as file:
    lines = file.readlines()
    pam250 = []
    aa = lines[0].strip().split()[0:]                       # aa에는 아미노산 index로 matrix값 추적
    for line in lines[1:]:
        row = [int(x) for x in line.strip().split()[1:]]
        pam250.append(row)
        
indel = -5                                                  # indel penalaty도 설정해야함       

# penalty = pam250[aa.index('A')][aa.index('A')]          # 확인차 penalty를 A-A == 2 
# print(aa, pam250,len(aa),len(pam250),penalty)         # aa리스트와 pam250 matrix 길이 동일

########################################################

result = traceback(aa, pam250, indel, ref, alt)
print(result)
