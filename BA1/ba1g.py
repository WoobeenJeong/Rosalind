

### Hamming distance : X,Y 두 개의 string 존재 시, |X|=|Y|로 길이 같을 때, X를 Y로 바꾸기 위한 최소 개수 = 다른 글자 개수 (XOR개념)


def XOR(string01, string02):
    if len(string01) != len(string02):
        print("Error:Using Edit distance")
    
    distance = 0
    
    for i in range(len(string01)):
        if string01[i] != string02[i]:
            distance += 1
    return distance

with open("bioinfo2/rosalind_ba1g.txt", "r") as file:
    string1 = file.readline().strip()
    string2 = file.readline().strip()
    
result = XOR(string1,string2)
print(result)