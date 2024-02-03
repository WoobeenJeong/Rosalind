# FarthestFirstTraversal(Data, k) 
#  Centers ← the set consisting of a single randomly chosen point from Data
#   while |Centers| < k
#      DataPoint ← the point in Data maximizing d(DataPoint, Centers) 
#      add DataPoint to Centers 
#  return Centers 
# d(DataPoint,Centers) = minall points x from Centersd(DataPoint, x).

# k는 클러스터의 개수, m은 차원의 개수
# pairs는 m차원의 점들의 리스트
# len(centers) < k 일때까지 centers에 점을 추가한다. = 즉 k개의 클러스터가 만들어질때까지

def euclidean_distance(point1, point2):
    return sum((point1[i] - point2[i]) ** 2 for i in range(len(point1))) ** 0.5

def FarthestFirstTraversal(pairs, k):
    centers = [pairs[0]]

    while len(centers) < k:
        max_dist_point = max(pairs, key=lambda point: min(euclidean_distance(point, center) for center in centers))
        
        # print(pairs,centers)
        
        centers.append(max_dist_point)

    for center in centers:
        print(" ".join(map(str, center)))

with open("bioinfo2/rosalind_ba8a.txt", "r") as myfile:
    data = myfile.readlines()
    k, m = map(int, data[0].split())
    pairs = [list(map(float, line.split())) for line in data[1:]]

# print(k,m,pairs)

FarthestFirstTraversal(pairs, k)

################################### previous code ########################################
### 다음 코드가 틀린 이유는 max_dist를 구할때, min_dist를 구하는 식이 잘못되었기 때문

def Error(pairs, k):
    centers = [pairs[0]]
    
    while len(centers) < k:
        max_dist = -1
        max_pair = None

        for point in pairs:
            min_dist = min([abs(point[0] - center[0]) ** 2 + abs(point[1] - center[1]) ** 2 for center in centers])
            if min_dist > max_dist:
                max_dist = min_dist
                max_pair = point

        centers.append(max_pair)

    for center in centers:
        print(f"{center[0]} {center[1]}")
        
# Error(pairs, k)
