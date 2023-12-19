
### position minimize the skew

#########################################
### in Brute Force

def skew_count(string):
    skew = 0
    skew_list = [0]
    for i in range(len(string)):
        if string[i] == "G":
            skew += 1
        elif string[i] == "C":
            skew -= 1
        skew_list.append(skew)
    return skew_list

def min_index(string):                      # 이 부분을 따로 min(skew_list)를 찾아버려서 시간이 엄청 오래 걸림
    skew_list = skew_count(string)          # 중복 계산으로 인해 시간이 오래 걸림
    min_index = []
    for i in range(len(skew_list)):
        if skew_list[i] == min(skew_list):
            min_index.append(i)
    return min_index

#########################################
### in One Pass

def one_pass(string):
    skew = 0
    skew_list = [0]
    min_skew = 0
    min_index = []
    for i in range(len(string)):
        if string[i] == "G":
            skew += 1
        elif string[i] == "C":
            skew -= 1
        skew_list.append(skew)
        if skew < min_skew:
            min_skew = skew
            min_index = [i+1]
        elif skew == min_skew:
            min_index.append(i+1)
    return skew_list, min_index


with open("bioinfo2/rosalind_ba1f.txt", "r") as file:
    string = file.readline().strip()
    
# print(string)

# result = skew_count(string)
# print(len(string), len(result)) # 만약 후자가 +1 이라면 정상적

# reusult2 = min_index(string)
# print(" ".join(map(str, reusult2)))

result3 = one_pass(string)
print(" ".join(map(str, result3[1])))
