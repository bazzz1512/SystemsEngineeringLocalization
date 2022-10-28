import numpy as np

pos_array = np.load("data_points_many_more.npy")

first_val = np.arange(0, 10, 0.1)


first_array = np.tile(first_val, (100,1))
second_array = first_array.transpose()


new_array = np.dstack((second_array, first_array))
print("huts")

distances = np.zeros((100,100))

for i in range(100):
    for j in range(100):
        distances[i,j] = np.linalg.norm(new_array[i,j]-pos_array[i,j])

print(distances)
print(np.max(distances))
print(np.where(distances==np.max(distances)))