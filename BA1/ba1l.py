
### Pattern to Number
### 1. A,C,G,T를 각각 0,1,2,3으로 할당
### 이때, 자리수 기준으로 곱 적용


def pattern_to_number(pattern):
        
        nt = {"A":0,"C":1,"G":2,"T":3}
        k = len(pattern)
        num = 0
        
        for i in range(k):
            num += nt[pattern[i]] * (4**(k-i-1))

        return num


with open('bioinfo2/rosalind_ba1l.txt') as f:
    pattern = f.readline().strip() 
    
print(pattern)
print(pattern_to_number(pattern))
      
# print(pattern_to_number("AAC")) # 0 + 0 + 1
# print(pattern_to_number("ACA")) # 0 + 4 + 0
# print(pattern_to_number("CAA")) # 16 + 0 + 0

