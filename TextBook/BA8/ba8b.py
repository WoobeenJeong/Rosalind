# k-Center Clustering, we selected Centers so that these points would minimize MaxDistance(Data, Centers)
# 이전에는 Centers를 선택해서 Data와 Centers의 최대거리를 최소화하는 방식으로 했었다면

# new scoring function. Given a set Data of n data points and a set Centers of k centers, the squared error distortion of Data and Centers, denoted Distortion(Data, Centers)
# Distortion(Data,Centers) = (1/n) ∑all points DataPoint in Datad(DataPoint, Centers)2.


import numpy as np

# ba8a에서 가져온 Euclidean 거리 구하기

def Eucleadian(point1, point2):
    return sum((point1[i] - point2[i]) ** 2 for i in range(len(point1))) ** 0.5

def Farthest(k, center):
    points = [center[0]]
    while len(points) < k:
        farthest_point = max(center, key=lambda point: min(Eucleadian(point, each) for each in points))
        points.append(farthest_point)
    return points

with open("bioinfo2/rosalind_ba8b.txt", "r") as myfile:
    data = myfile.readlines()
    k, m = map(int, data[0].split())
    center = [list(map(float, line.split())) for line in data[1:k+1]]
    pairs = [list(map(float, line.split())) for line in data[k+2:]]

    # print(k,m,np.array(center))

centers = Farthest(k, center)

# print(np.array(centers))

# Distortion(Data,Centers) = (1/n) ∑all points DataPoint in Datad(DataPoint, Centers)^2.
distortion = sum(min(Eucleadian(pair, center) for center in centers) ** 2 for pair in pairs) / len(pairs)
result=round(distortion, 3)
print(result)
