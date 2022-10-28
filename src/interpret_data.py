import numpy as np

pos_array = np.load("data_points.npy")

first_val = np.arange(0, 10, 0.1)


first_array = np.tile(first_val, (100,1))
second_array = first_array.transpose()


new_array = np.dstack((second_array, first_array))
print("huts")