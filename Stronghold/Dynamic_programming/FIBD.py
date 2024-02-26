### Given: Positive integers n≤100 and m≤20
### Return: The total number of pairs of rabbits that will remain after the n-th month if all rabbits live for m months
### 기존 fibonacci와 다른 점은 rabbit이 m개월을 산다는 것이다.
### 따라서, m개월 뒤 더이상 자손 생산을 못하고 자기 자신도 -1 이 되도록 수정해야 한다.

############################################
### 1. Iterative

def Iter_fibodeath(n, m):
    old = [1] + (m - 1) * [0]
    for i in range(2, n + 1):
        new = sum(old[1:])
        old = [new] + old[:-1]
    return sum(old)

#############################################

with open ("bioinfo2/rosalind_fibd.txt", "r") as file:
    n, m = map(int, file.read().split())
# print((n, m))
    
result01 = Iter_fibodeath(n, m)
print(result01)
