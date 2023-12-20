
### Number to Pattern
### A,C,G,T를 각각 0,1,2,3으로 할당
### 이때, 자리수 기준으로 곱 적용

### ba1l.py의 역함수

def pattern_to_number(number, kmer):
        
        nt = {"A":0,"C":1,"G":2,"T":3}
        pattern = ""
        
        for i in range(kmer):
            
            pattern += list(nt.keys())[list(nt.values()).index(number % 4)]
            number = number // 4
        
        pattern = "".join(reversed(pattern))

        return pattern

with open('bioinfo2/rosalind_ba1m.txt') as f:
    number = int(f.readline().strip())
    kmer = int(f.readline().strip())
    
print(number, kmer)
print(pattern_to_number(number, kmer))