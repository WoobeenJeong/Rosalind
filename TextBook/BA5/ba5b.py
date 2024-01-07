# Manhattan tourist problem = 투어방문에 최고 많은 곳을 방문하는 문제
# 투어 방문 = edge값 가중 +1 / (0,0)에서 (n,m)까지 가는 최고 가중치 거리
# 이는 dynamic programming의 기초로, 이미 input의 가중치가 가장 간단한 1로 작성된 결과를 가지고 있으므로 최대값만 계산하면 됨
# mini dynamic programming으로 지칭!

with open('bioinfo2/rosalind_ba5b.txt', 'r') as file:
    lines = file.readlines()

n, m = map(int, lines[0].split())

matrix1 = []
matrix2 = []
separate = False

for line in lines[1:]:
    line = line.strip()
    if line == '-':
        separate = True
    elif not separate:
        matrix1.append(list(map(int, line.split())))
    else:
        matrix2.append(list(map(int, line.split())))

# print(f"{matrix1},{matrix2}")

def mini_dynamic(n, m, down, right):
    
    # F = []
    # for i in range(n + 1):                                      # (n,m)행렬, (0,0)부터니까 n+1, m+1
    #     row = []
    #     print(row)
    #     for j in range(m + 1):
    #         row.append(0)
    #     F.append(row)
    #     print(F)
    
    # F = [[0 for _ in range(m + 1)] for _ in range(n + 1)]     # 축약형으로 표현 가능
    
    import numpy as np
    F = np.zeros((n + 1, m + 1))                              # numpy를 이용해, 모든 값 0인 (n+1,m+1) 행렬 가능

    # print(F)                                                  # 3가지 방식 모두 동일
    
    for i in range(1, n + 1):
        F[i][0] = F[i - 1][0] + down[i - 1][0]                 # down방향으로 값을 더하기
    for j in range(1, m + 1):
        F[0][j] = F[0][j - 1] + right[0][j - 1]                # right방향으로 값을 더하기

    for i in range(1, n + 1):
        for j in range(1, m + 1):                              # down과 right중 큰 값을 대각원소에 넣기
            F[i][j] = max(F[i - 1][j] + down[i - 1][j], F[i][j - 1] + right[i][j - 1])

    # print(F)
    
    return F[n][m]                                             # (n,m)위치의 값을 반출

result = mini_dynamic(n,m,matrix1,matrix2)
print(int(result))
