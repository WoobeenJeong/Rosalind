####################################
### 피보나치 수열로 토끼 번식쌍 개체수 구하기
### n은 40이하, k는 5이하, 
### F1 = F2 = 1 to initiate the sequence

# Fn = F(n-2) + F(n-1) k=3 means,
# (m=mature) F1=1 / F2=1m / F3=1m+3 / F4=4m+3 / F5=7m+12

def Fibonacci(number,kpairs):
    new, old = 1, 1
    for _ in range(number - 1):
        new, old = old, old + new*kpairs
    return new

# print (Fibonacci(5,3))
# == 1 / 1 / 1 + 1*3 / 1+1*3 + 1*3 / 1+1*3+1*3 + (1+1*3)*3 / ......

with open ("bioinfo2/rosalind_fib.txt", "r") as file:
    n, k = map(int, file.read().split())
    
print(Fibonacci(n,k))
