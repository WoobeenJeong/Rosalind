### Converge를 하는 k-means clustering
### lloyd algorithm
### center잡고 -> cluster하고 -> 다시 center잡고 -> converge까지 반복

import numpy as np

def Euclidean(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))

def Converge(centers, new_centers):
    
    threshold=1e-8
    
    for center, new_center in zip(centers, new_centers):
        if Euclidean(center, new_center) > threshold:
            return False
    return True

def Lloyd(k, m, pairs):
    # random = np.random.choice(len(pairs), k, replace=False)
    # centers = [pairs[i] for i in random]
    centers = pairs[:k]

    print(centers)
    
    while True:
        candidates = [[] for _ in range(k)]
        for point in pairs:
            dist = [Euclidean(point, center) for center in centers]
            min_dist = dist.index(min(dist))
            candidates[min_dist].append(point)
        
        new_centers = [np.mean(each, axis=0) for each in candidates]
        # print(np.matrix(new_centers))
        
        if Converge(centers, new_centers):
            break

        centers = new_centers
        
    return centers

with open("bioinfo2/rosalind_ba8c.txt", "r") as myfile:
    lines = myfile.readlines()
    k, m = map(int, lines[0].split())
    pairs = [np.array(list(map(float, line.split()))) for line in lines[1:]]

result = Lloyd(k, m, pairs)
for each in result:
    print(" ".join(map(lambda x: "{:.3f}".format(x), each)))
    
# import numpy as np

# def Euclidean(point1, point2):
#     return np.sqrt(np.sum((point1 - point2) ** 2))      # 기존에 **0.5 말고 np.sqrt를 사용

# def Lloyd(k, m, pairs):
#     centers = pairs[:k]

#     while True:
#         candidates = [[] for _ in range(k)]
#         for point in pairs:
#             dist = [Euclidean(point, center) for center in centers]
#             min_dist = np.argmin(dist)
#             candidates[min_dist].append(point)
        
#         new_centers = [np.mean(each, axis=0) for each in candidates]
        
#         if np.allclose(centers, new_centers):
#             break

#         centers = new_centers
    
#     return centers

# with open("bioinfo2/sample.txt", "r") as myfile:
#     lines = myfile.readlines()
#     k, m = map(int, lines[0].split())
#     pairs = [np.array(list(map(float, line.split()))) for line in lines[1:]]

# result = Lloyd(k, m, pairs)
# for each in result:
#     print(" ".join(map(lambda x: "{:.3f}".format(x), each)))
