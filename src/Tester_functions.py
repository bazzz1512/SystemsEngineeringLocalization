from cLocalization import cLocalization
import numpy as np


def test_skeleton():
    pos = [0, 0]
    nodes_list = [[1, 1], [0, 0], [1, 3], [5, 2], [-1, 6]]

    instance = cLocalization(nodes_list, pos)
    instance.calculate_dis()

    print(instance)

    instance.add_noise_to_dis(2)
    print(instance)


def test_point():
    pos = [3, -4]
    nodes_list = [[-6, -6], [6, 6], [-6, 6], [6, -6]]

    instance = cLocalization(nodes_list, pos)

    instance.plot_point()


def test_path():
    pos = [0, 0]
    nodes_list = [[-6, -6], [6, 6], [-6, 6], [6, -6]]

    instance = cLocalization(nodes_list, pos)

    path = get_spiral()
    instance.plot_path(path)


def get_spiral():
    t = np.linspace(2, 18, 80)
    sins = np.sin(t)
    coss = np.cos(t)
    y = np.divide(sins, t) * 8
    x = np.divide(coss, t) * 8
    points = []
    for i in range(len(t)):
        points.append([x[i], y[i]])
    return points


def test_new_triangulation():
    pos = np.array([2, 1])
    nodes_list = np.array([[1, 1], [0, 0], [1, 3], [5, 2], [-1, 6], [6, 6], [6, -6]])
    min_room = np.min(nodes_list, axis=0)
    max_room = np.max(nodes_list, axis=0)
    min_max = np.vstack([min_room, max_room])

    print(min_room)
    print(max_room)
    print(min_max)

    instance = cLocalization(nodes_list, pos)
    instance.calculate_dis()
    print(instance)
    print(f"Error: {instance.get_error(pos, nodes_list, np.array(instance.distances_to_nodes))}")
    instance.add_noise_to_dis(2)
    print(instance)
    print(f"Error: {instance.get_error(pos, nodes_list, np.array(instance.distances_to_nodes))}")

    return_val = instance.triangulate_least_squares(min_max)
    print(return_val)

def test_different_values_save():
    new_array = np.zeros((100, 100, 2))
    nodes_list = np.array([[0, 0], [10, 0], [10, 10], [0, 10], [5,0], [5,10], [0,5], [10,5], [5,5], [2,2], [7,7], [2,7], [7,2], [1,1], [9,9], [2,3], [8,3], [3,8], [8,8], [7,1], [1,7]])
    room = np.array([[0,0], [10,10]])
    error = 0.05
    for i in range(100):
        for j in range(100):
            pos = np.array([i*0.1, j*0.1])
            instance = cLocalization(nodes_list, pos)
            instance.calculate_dis()
            instance.add_noise_to_dis(0.05)
            return_val = instance.triangulate_least_squares(room_points=room)
            new_return = return_val
            # print(new_return)
            print(f"{i}, {j}")
            # new_error = np.sqrt((pos[0]-new_return[0])**2 + (pos[1] - new_return[1])**2)
            new_array[i,j] = new_return

    np.save("data_points_many_more.npy", new_array)


