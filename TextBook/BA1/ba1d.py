
### find all occurences of a pattern

def brute_force(pattern, string):
    positions = []
    for i in range(len(string) - len(pattern) + 1):    # take care of range
        if string[i:i+len(pattern)] == pattern:
            positions.append(i)
    return positions

with open ("bioinfo2/rosalind_ba1d.txt", "r") as files:
    lines = files.readlines()
    pattern = lines[0].strip()
    string = lines[1].strip()
    
# print(pattern, string)

positions = brute_force(pattern, string)
print(" ".join(map(str, positions)))
