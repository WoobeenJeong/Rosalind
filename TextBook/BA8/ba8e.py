import numpy as np

def hierarchical_clustering(n, matrix):
    clusters = [[i] for i in range(1, n + 1)]
    distances = np.copy(matrix)
    np.fill_diagonal(distances, np.inf)

    # print(clusters)
    # print(distances)

    cluster_history = []

    while len(clusters) > 1:
        
        ######################### 방법1 : 기초적으로 min(i,j)를 구한다 (6줄)
        # min_val = np.inf
        # min_i, min_j = -1, -1

        # for i in range(len(clusters)):
        #     for j in range(i + 1, len(clusters)):
        #         if distances[i, j] < min_val:
        #             min_val = distances[i, j]
        #             min_i, min_j = i, j
        # i, j = min_i, min_j
        
        ######################### 방법2 : numpy의 min, triu_indices, where를 이용한다 (3줄)
        # min_val = np.min(distances[np.triu_indices(len(clusters), k=1)])
        # min_i, min_j = np.where(distances == min_val)
        # min_i, min_j = min_i[0], min_j[0]
        # i, j = min_i, min_j

        ######################### 방법3 : numpy의 unravel_index를 이용한다 (1줄)
        i, j = np.unravel_index(np.argmin(distances), distances.shape)
        # print(i, j)
        
        checkpoint = [c.copy() for c in clusters]
        # print(checkpoint)

        clusters[i].extend(clusters[j])
        del clusters[j]
        # print(clusters)                           # [[1],[2],[3]] 형태의 index가 [[1,2],[3]] 형태로 수정 (i,j)=1,2 가 합쳐져서

        new_distances = np.delete(distances, j, axis=0)     
        new_distances = np.delete(new_distances, j, axis=1)
        new_distances[i, :] = 0
        new_distances[:, i] = 0
        # print(new_distances)                        # 합쳐진 index에 맞게, i행렬은 0으로, j행렬은 삭제

        for k in range(len(clusters)):                # i행렬에 들어갈 average distance 계산
            if k != i:
                dist_sum = 0
                for a in clusters[i]:
                    for b in clusters[k]:
                        dist_sum += matrix[a - 1][b - 1]                        # cluster은 1부터지만, matrix는 0부터 시작하므로 -1
                average = dist_sum / (len(clusters[i]) * len(clusters[k]))
                new_distances[i][k] = average
                new_distances[k][i] = average

        new_distances[new_distances == 0] = np.inf
        # print(new_distances)

        # print(clusters)
        
        changed = [cluster for cluster in clusters if cluster not in checkpoint]
        if changed:
            cluster_history.append([c.copy() for c in changed])

        distances = new_distances

    return cluster_history

with open('bioinfo2/rosalind_ba8e.txt', 'r') as f:
    node = int(f.readline())
    matrix = [list(map(float, line.split())) for line in f]
matrix = np.array(matrix)

result = hierarchical_clustering(node, matrix)

# for cut_nodes in result:
#     print(" ".join(map(str, cut_nodes)))
    
for clusters in result:
    for cluster in clusters:
        print(" ".join(map(str, cluster)))
        


########################################################################

import numpy as np

def hierarchical_clustering(n, matrix):
    clusters = [[i] for i in range(1, n + 1)]
    distances = np.copy(matrix)
    np.fill_diagonal(distances, np.inf)
    
    cluster_history = []

    while len(clusters) > 1:
        i, j = np.unravel_index(np.argmin(distances), distances.shape)

        checkpoint = [c.copy() for c in clusters]

        clusters[i].extend(clusters[j])
        del clusters[j]

        new_distances = np.delete(distances, j, axis=0)     
        new_distances = np.delete(new_distances, j, axis=1)
        new_distances[i, :] = 0
        new_distances[:, i] = 0

        for k in range(len(clusters)):
            if k != i:
                dist_sum = 0
                for a in clusters[i]:
                    for b in clusters[k]:
                        dist_sum += matrix[a - 1][b - 1]
                average = dist_sum / (len(clusters[i]) * len(clusters[k]))
                new_distances[i][k] = average
                new_distances[k][i] = average

        new_distances[new_distances == 0] = np.inf
        
        changed = [cluster for cluster in clusters if cluster not in checkpoint]
        if changed:
            cluster_history.append([c.copy() for c in changed])

        distances = new_distances

    return cluster_history

with open('bioinfo2/rosalind_ba8e.txt', 'r') as f:
    node = int(f.readline())
    matrix = [list(map(float, line.split())) for line in f]
matrix = np.array(matrix)

result = hierarchical_clustering(node, matrix)
        
