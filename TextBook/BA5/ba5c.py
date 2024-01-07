### Longest Common Subsequence without Gap
### Input : Two amino acid strings.
### Output : A longest common subsequence in both strings.
### 즉, 두 서열에서 공통으로 나타나는 가장 긴 서열을 찾는 문제 (gap은 지워서 찾는 형식)

#############################################
### 잘못 만든 함수 gap 이해에 문제

def ident_allowgap(ref,alt):                                    # 만들다 보니, 숫자 세는걸 만들어 버림

    ident_count = 0
    
    for i in range(len(ref)):
        for j in range(len(alt)):                               # ref, alt 둘 다 고려할 거구
            if ref[i] == alt[j]:        
                ident_count += 1
            elif ref[i] != alt[j]:                              # 다른 경우에는
                for k in range(abs((len(ref)-len(alt)))+1):     # gap허용 개수
                    if ref[i] == alt[j+k]:                      # alt에 갭 허용해 +1
                        ident_count += 1
                    elif ref[i+k] == alt[j]:                    # ref에 갭 허용해 +1
                        ident_count += 1
                    else:                                       # 둘 다 아니면 지나감
                        break
    return ident_count


import numpy as np

#############################################

def ident_allowgap2(ref, alt):
    
    n, m = len(ref), len(alt)
    F = np.zeros((n+1, m+1), dtype=int)                 # int로 안해주면, max에서 오류남

    for i in range(1, n+1):                             # 1부터 시작해야, 0번째 행과 열에 0이 들어감 (서열보다 1개 더 많게 시작)
        for j in range(1, m+1):
            
            if ref[i-1] == alt[j-1]:                    # 서열 같으면, 이전 대각선 원소+1을 넣기
                F[i][j] = F[i-1][j-1]+1
            else:                                       # 다르면, 이전 (윗,옆)원소 중 큰값 넣기 
                F[i][j] = max(F[i-1][j], F[i][j-1])

    # print(F)                                          # 알던 dynamic programming은 아님 (local,global 둘다X)
    
    total = F[n][m]                                     # 가장 긴 공통 서열 길이 (같은 값을 가지면 +1씩 누적되었기 때문)
    # print(total)
    string = [''] * total
    i, j = n, m
    
    while i > 0 and j > 0:                              # traceback과정으로 가장 긴 공통 서열
        if ref[i-1] == alt[j-1]:
            string[total-1] = ref[i-1]                  # 같으면, string에 넣고
            i -= 1                                      # i,j 모두 1칸씩 줄여 대각 이동, string길이도 -1
            j -= 1
            total -= 1
        elif F[i-1][j] > F[i][j-1]:                     # 위 if에 반하여, 값이 다르고, 위쪽갚이 왼쪽값보다 크면
            i -= 1                                      # 위로 이동
        else:                                           
            j -= 1                                      # 왼쪽값이 더 크면, 왼쪽으로 이동

    return ''.join(string)

#############################################

with open ("bioinfo2/rosalind_ba5c.txt", "r") as f:
    lines = f.readlines()
    
ref = lines[0].strip()
alt = lines[1].strip()

# print(f"{ref},{alt}")

#############################################

result = ident_allowgap2(ref, alt)
print(result)
