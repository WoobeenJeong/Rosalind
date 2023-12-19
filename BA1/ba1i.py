

### find most freq kmer with mismatch

def hamming(string01, string02):
    if len(string01) != len(string02):
        print("Error:Using Edit distance")

    distance = 0
    
    for i in range(len(string01)):
        if string01[i] != string02[i]:
            distance += 1
    return distance

def most_freq(string, k, d):
    pattern_dict = {}
    count = 0
    
    nt = ["A","C","G","T"]
    
    patterns = [''.join(nt[(i//(4**j))%4] for j in range(k)) for i in range(4**k)]
    pattern_dict = {pattern: 0 for pattern in patterns}
    
    #########################################
    ### 위의 두 줄짜리 코드 풀어 쓴 경우 
    
    # for i in range(4**k):
    #     pattern = ""
    #     for j in range(k):
    #         pattern += nt[(i//(4**j))%4]
    #     pattern_dict[pattern] = 0
    #########################################
    
    for pattern in pattern_dict.keys():
        pattern_dict[pattern] = sum(1 for i in range(len(string) - k + 1) if hamming(pattern, string[i:i + k]) <= d)

    #########################################
    ### 위의 두 줄짜리 코드 풀어 쓴 경우
    
    # for pattern in pattern_dict.keys():
    #     for i in range(len(string) - k + 1):
    #         pattern2 = string[i:i + k]
    #         count += 1
            
    #         if hamming(pattern, pattern2) <= d:
    #             pattern_dict[pattern] += 1
    #########################################

    max_count = max(pattern_dict.values())
    max_pattern = [k for k,v in pattern_dict.items() if v == max_count]

    return max_pattern

with open("bioinfo2/rosalind_ba1i.txt","r") as f:
    
    string = f.readline().strip()
    k,d = f.readline().strip().split(" ")
    k,d = int(k),int(d)
    
# print(string,k,d)

result = most_freq(string,k,d)
print(" ".join(result))