# dynamic programming의 개념의 밑바탕이 되는 문제 : "minimum coin change" 문제
# 만약 (a,b,c)원의 동전이 존재하고 n원을 만들어야 한다면
# 최소 동전을 구하는 식 F(n) = min(F(n-a), F(n-b), F(n-c)) + 1 이 성립
# 단, 여기서 그 어떤 (a,b,c)로도 n을 만들 수 없으면 F(n) = -1 처리
# -1 처리하는 이유는, F(n) 식에서 if문으로 쉽게 -1을 배제할 수 있기 때문 (부등호로도 가능)

# F(n) = min(F(n-a), F(n-b), F(n-c)) + 1

with open("bioinfo2/rosalind_ba5a.txt", "r") as file:
    lines = file.readlines()

n = int(lines[0].strip())
coins = list(map(int, lines[1].split(',')))                 # 각 coin은 coins 리스트로 저장

### 아래 두 방식은 Bottom-up 방식

def mincoin(n, coins):
    F = [0] * (n+1)                                         # [0]*(n+1)로 하면 F[n=0] = 0이 되어서 F[1]부터 시작 가능
    for i in range(1, n+1):                                 # n+1까지 돌려야 F[n]까지 계산 가능 (python은 0부터 시작이므로 "항상 주의")
        F[i] = -1                                           # 만약 n을 만드는 coin이 없으면 -1로 처리 
        for each in coins:                                  # coins와 헷갈리지 않게 each로 표현
            if i >= each and F[i-each] != -1:               # 남은금액(n=i)가 동전(each) 이상이고, F[i-each]가 -1이 아니면(=환전불가제외)
                if F[i] == -1 or F[i] > F[i-each] + 1:      # F[i]가 애초에 -1이거나, F[i-each] + 1이 더 작으면
                    F[i] = F[i-each] + 1                    # 더 작은 값으로 F[i] 갱신
    return F[n]


### 위 코드를 더 간단히 작성하면

def mincoin_ver2(n, coins):
    F = [float('inf')] * (n+1)                             # float('inf')인 이유는 inf인 input이 들어오는 경우가 없기 때문   
    F[0] = 0
    
    for i in range(1, n+1):
        for each in coins:
            if i >= each:
                F[i] = min(F[i], F[i - each] + 1)         # min함수를 사용해서, 기존에 for문과 부등식이 필요한 부분을 짧게 처리

    # print(F)

    if F[n] == float('inf'):                              # 만약 F[n]이 inf면, n을 만드는 each(coin)이 없다는 뜻이므로 -1 처리
        return -1
    else:
        return F[n]
    
# print(n, coins)

# result = mincoin(n, coins)                              # 둘 중 어느걸 써도 상관없음
result = mincoin_ver2(n, coins)
print(result)
