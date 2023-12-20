
### generate d-neighbors of a string/pattern
### 여기서는 앞의 두 방법 말고, 세번째 방법을 사용

################################################
### 방법 1 소거법 elimination
### 문제점은 pattern, d가 길어지면 메모리, 시간문제
### 그리고 나열 순서 문제도 발생

from itertools import product

def hamming(string01, string02):
    if len(string01) != len(string02):
        print("Error:Using Edit distance")
    return sum(s1 != s2 for s1, s2 in zip(string01, string02))

def d_neighbor01(pattern, d):
    
    nt = {"A","C","G","T"}
    all_possible = []
    neighbor_list = []
    
    all_possible = list(product(nt, repeat=len(pattern)))
    for i in range(len(all_possible)):
        all_possible[i] = ''.join(all_possible[i])

    for each in all_possible:
        if hamming(pattern, each) <= d:
            neighbor_list.append(each)

    return neighbor_list

################################################
### 방법 2 : recurrence 재귀로 -> 순서 문제 발생
### 게다가 잘못 재귀를 쓰면 stack-overflow 발생

def d_neighbor02(pattern, d):
    nt = ['A', 'C', 'G', 'T']

    def generate(current_pattern, remaining_d):
        if remaining_d == 0:
            return [current_pattern]
        
        neighbors = [pattern]

        for i in range(len(current_pattern)):
            for n in nt:
                if current_pattern[i] != n:
                    new_pattern = current_pattern[:i] + n + current_pattern[i+1:]
                    neighbors += generate(new_pattern, remaining_d - 1)
                    
        neighbors = list(dict.fromkeys(neighbors))
        return neighbors
    
    return generate(pattern, d)

################################################
### 방법 3 : 반복문으로 작성 + 핵심은 중복을 set()으로 안 잡아서 순서를 가져오기
### 이것도 순서를 제대로 가져오지 못함 + 더 복잡하게 변조 필요

def d_neighbor03(pattern, d):
    nt = ['A', 'C', 'G', 'T']
    patterns = [pattern]

    for _ in range(d):
        new_patterns = []
        visited_patterns = set()
        
        for current_pattern in patterns:
            for i in range(len(current_pattern)):
                for n in nt:
                    if current_pattern[i] != n:
                        new_pattern = current_pattern[:i] + n + current_pattern[i+1:]

                        if new_pattern not in visited_patterns:
                            visited_patterns.add(new_pattern)
                            new_patterns.append(new_pattern)

        patterns = new_patterns

    return patterns

################################################
### 방법 4. 반복문 함수를 반복하도록 이중 반복
### 일단 d개 변조된 패턴을 생성하는 함수 

def d_mutate(pattern, d):
    nt = ['A', 'C', 'G', 'T']
    neighbor = []
    new_patterns = [pattern]
    visited_patterns = set()

    for _ in range(d):
        for current_pattern in list(new_patterns):
            for i in range(len(current_pattern)):
                for n in nt:
                    if current_pattern[i] != n:
                        new_pattern = current_pattern[:i] + n + current_pattern[i + 1:]

                        if new_pattern not in visited_patterns:
                            visited_patterns.add(new_pattern)
                            new_patterns.append(new_pattern)

                            if hamming(pattern, new_pattern) == d:
                                neighbor.append(new_pattern)
    return neighbor

def d_neighbor04(pattern, d):
    result = []
    for error in range(d, 0, -1):
        mutated_pattern = d_mutate(pattern, error)
        result.extend(mutated_pattern)
    result.append(pattern)
    return result

################################################
### main (인풋 파일, 아웃풋 함수 설정)

with open ('bioinfo2/rosalind_ba1n.txt') as f:
    pattern = f.readline().strip()
    d = int(f.readline().strip())
# print((pattern, d))

result = d_neighbor04(pattern, d)

################################################
### 검산용 verification
### I want to check :

method = d_neighbor04

################################################

def verification(pattern, d):
    result = method(pattern, d)
    sort_list = sorted(result)
            
    hamming_dict = {}
    for each in sort_list:
        distance = hamming(pattern, each)
        hamming_dict.setdefault(distance, []).append(each)
    print(len(sort_list), sum(len(values) for values in hamming_dict.values()))
    for key, values in hamming_dict.items():
        print(f"{len(values)}",{(key):values})

    return " "

# print(verification(pattern, d))

################################################
## 출력 형태 변형 및 저장

print(*result, sep='\n')

output_file_path = "ba1n_output.txt"

with open(output_file_path, "w") as output_file:
    output_file.write("\n".join(result))

print(f"Results saved to {output_file_path}")
