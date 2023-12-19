

### Appeoximate pattern matching
### mismatch의 개수가 hamming distance보다 작거나 같게
### hamming dist 함수는 앞선 ba1g.py에서 사용한 것과 동일하게 사용

def hamming(string01, string02):
    if len(string01) != len(string02):
        print("Error:Using Edit distance")

    distance = 0
    
    for i in range(len(string01)):
        if string01[i] != string02[i]:
            distance += 1
    return distance

def approx_match(pattern, text, mismatch):

    match_list = []
  
    for i in range(len(text)-len(pattern)+1):
        if hamming(pattern, text[i:i+len(pattern)]) <= mismatch:
            match_list.append(i)
            
    return match_list

with open ("bioinfo2/rosalind_ba1h.txt", "r") as file:
    pattern = file.readline().strip()
    text = file.readline().strip()
    mismatch = int(file.readline().strip())
    
# print(pattern, text, mismatch)

result = approx_match(pattern, text, mismatch)
print(" ".join(map(str, result)))