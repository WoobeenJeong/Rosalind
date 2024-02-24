####################################
### Exponential time complexity (O(2^n), Brute-Force, Bad)

### 1. Iterative

def Iterative_Fibo(n, k):
    new, old = 1, 1
    for _ in range(n - 1):
        new, old = old, old + new*k
    return new

### 2. Recursive

def Recursive_Fibo(n, k):
    if n <= 2:
        return 1
    else:
        return Recursive_Fibo(n-1, k) + k*Recursive_Fibo(n-2, k)

####################################
### DP : memoization (linear time complexity, O(n), Better)

### 3. Top-Down (disadvantage: recursion limit, stack overflow)

def Topdown_Fibo(n, k):
    memo = {1:1, 2:1}
    if n not in memo:
        memo[n] = Topdown_Fibo(n-1, k) + k*Topdown_Fibo(n-2, k)
    return memo[n]

### 4. Bottom-Up (Tabulation)

def Bottomup_Fibo(n, k):
    memo = {1:1, 2:1}
    for i in range(3, n+1):
        memo[i] = memo[i-1] + k*memo[i-2]
    return memo[n]

####################################
### Matrix (linear time complexity, O(logn), Best)

### 5. Matrix Exponentiation

def Matrix_Fibo(n, k):
    def multy(A, B):
        return [[A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
                [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]]
    def power(A, n):
        if n == 1:
            return A
        elif n % 2 == 0:
            return power(multy(A, A), n//2)
        else:
            return multy(A, power(multy(A, A), (n-1)//2))
    return power([[1, k], [1, 0]], n-1)[0][0]
        
####################################    

with open ("bioinfo2/rosalind_fib.txt", "r") as file:
    n, k = map(int, file.read().split())

print(Iterative_Fibo(n, k))
print(Recursive_Fibo(n, k))
print(Topdown_Fibo(n, k))
print(Bottomup_Fibo(n, k))
print(Matrix_Fibo(n, k))

### Fn = F(n-2) + F(n-1) k=3 means,
### (m=mature) F1=1 / F2=1m / F3=1m+3 / F4=4m+3 / F5=7m+12
### == 1 / 1 / 1 + 1*3 / 1+1*3 + 1*3 / 1+1*3+1*3 + (1+1*3)*3 / ...

####################################
### Explantion of matrix exponentiation

# f(2n) = f(n) + f(n-1)*k
# f(2n+1) = f(n+1) + f(n)*k

# in matrix form

# |  f(2n)  |   | 1  k |   |  f(n)  |
# |         | = |      | * |        |
# | f(2n+1) |   | 1  1 |   | f(n+1) |
