### global alignment + BLSUM62
### needleman-wunsch algorithm

### Code 시작 전에, 문제에서 주어진 BLOSUM62 정보를 가져와야 하므로 txt 파일로 저장해 불러온다.

with open('bioinfo2/BLOSUM62.txt', 'r') as file:
    lines = file.readlines()
    blosum62 = []
    aa = lines[0].strip().split()[0:]                       # aa에는 아미노산 index로 matrix값 추적
    for line in lines[1:]:
        row = [int(x) for x in line.strip().split()[1:]]
        blosum62.append(row)
        
indel = -5                                                  # indel penalaty도 설정해야함        

# penalty = blosum62[aa.index('A')][aa.index('A')]          # 확인차 penalty를 A-A로 설정 4가 나와야 함
# print(aa, blosum62,len(aa),len(blosum62),penalty)         # aa리스트와 blosum62리스트의 길이도 동일한지 체크

def scorematrix(aa,blosum62,indel,ref,alt):
    score = [[0 for i in range(len(ref)+1)] for j in range(len(alt)+1)]         # ref+1 , alt+1 크기로 작성
     
    for i in range(1,len(alt)+1):                                               # 두 for문을 1부터 시작하니, 당연히 (0,0)은 0으로 채워자고, 1부터 서열 시작
        score[i][0] = score[i-1][0] + indel                                     # 1칸 떨어질 때마다 indel로 -5씩 추가
    for j in range(1,len(ref)+1):
        score[0][j] = score[0][j-1] + indel
    
    for i in range(1,len(alt)+1):                                                # aa.index활용해서(순서주의) max값 구하고, 일치는 대각선, indel은 위,옆 구분 주의
        for j in range(1,len(ref)+1):
            score[i][j] = max(score[i-1][j-1] + blosum62[aa.index(alt[i-1])][aa.index(ref[j-1])],
                              score[i-1][j] + indel,
                              score[i][j-1] + indel)
    return score

# print(scorematrix(aa,blosum62,indel,ref,alt))

def traceback(aa, blosum62, indel, ref, alt):
    score = scorematrix(aa, blosum62, indel, ref, alt)
    i, j = len(alt), len(ref)
    max_score = score[i][j]
    refseq = []
    altseq = []

    while i > 0 or j > 0:
        if i > 0 and j > 0 and score[i][j] == score[i - 1][j - 1] + blosum62[aa.index(alt[i - 1])][aa.index(ref[j - 1])]:
            refseq.append(ref[j - 1])
            altseq.append(alt[i - 1])
            i -= 1
            j -= 1
        else:
            if i > 0 and score[i][j] == score[i - 1][j] + indel:
                altseq.append(alt[i - 1])
                refseq.append('-')
                i -= 1
            elif j > 0 and score[i][j] == score[i][j - 1] + indel:
                altseq.append('-')
                refseq.append(ref[j - 1])
                j -= 1
            else:
                print('error')
                break

    return f"{max_score}\n{''.join(refseq[::-1])}\n{''.join(altseq[::-1])}"

########################################################

with open('bioinfo2/rosalind_ba5e.txt', 'r') as file:
    lines = file.readlines()
    ref = lines[0].strip().split()[0]
    alt = lines[1].strip().split()[0]

# print(ref, alt, len(ref), len(alt))                         # ref alt 길이 확인해서, score matrix 만들때, +1 크기로 만들어야, (0,0)으로 시작하고 시작하는 위치에 대한 penalty=-5씩 추가

result = traceback(aa,blosum62,indel,ref,alt)
print(result)

###############################################


# def traceback(aa, blosum62, indel, ref, alt):                                   # 이 traceback의 문제점은, maximum을 구할때, 전체 기준이 아니라, 한번 이동 기준만 고려
#     score = scorematrix(aa, blosum62, indel, ref, alt)
#     i, j = len(alt), len(ref)
#     max_score = score[i][j]
#     refseq = []
#     altseq = []

#     refseq.extend(ref[-1])                                                      # 처음에 시작 값을 넣어줘야 함 (score matrix의 맨 마지막 값)
#     altseq.extend(alt[-1])

#     # print(score)
    
#     while i > 0 and j > 0:
    
#         # print(f"i:{i}, j:{j}")
        
#         maximum = max(score[i-1][j-1], score[i-1][j], score[i][j-1])
        
#         # print(f"{score[i-1][j-1], score[i-1][j], score[i][j-1],maximum}")   
        
#         if maximum == score[i-1][j-1]:                                         # maximum이 대각원소이면, 둘다 -1하고
#             i -= 1
#             j -= 1
#             refseq.append(ref[j-1])                                            # 해당 aa를 저장
#             altseq.append(alt[i-1])

#         elif maximum == score[i-1][j]:
#             i -= 1
#             altseq.append(alt[i-1])
#             refseq.append('-')                                                 # =위로 이동한 경우 = ref에 insertion 발생

#         elif maximum == score[i][j-1]:
#             j -= 1
#             altseq.append('-')                                                 # =옆으로 이동한 경우 = alt에 deletion 발생
#             refseq.append(ref[j-1])

#         else:
#             print('error')                                                     # 만약 코드에 문제 있으면 error
#             break

#         # print(f"i:{i}, j:{j}, refseq:{refseq}, altseq:{altseq}")             # 이 각주 해제하면 순서대로 어떻게 들어갔는지 확인 가능
        
#     return f"{max_score}\n{''.join(refseq[-2::-1])}\n{''.join(altseq[-2::-1])}"     # -2::-1로 하면, 마지막 1개를 제외하고, 역순으로 출력
