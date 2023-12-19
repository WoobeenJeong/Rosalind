
def counting(Text, Pattern):
    count = 0
    for i in range(len(Text) - len(Pattern) + 1):
        if Text[i:i+len(Pattern)] == Pattern:
            count += 1
    return count

with open("bioinfo2/rosalind_ba1a.txt", "r") as file:
    Text = file.readline().strip()
    Pattern = file.readline().strip() 

# print(Text, Pattern)

result = counting(Text, Pattern)
print(result)
