from cLocalization import cLocalization
import numpy as np

def test_skeleton():
    pos = [0,0]
    nodes_list = [[1,1],[0,0],[1,3], [5,2], [-1, 6]]

    instance = cLocalization(nodes_list, pos)
    instance.calculate_dis()

    print(instance)

    instance.add_noise_to_dis(2)
    print(instance)


def test_point():
    pos = [3,-4]
    nodes_list = [[-6,-6],[6,6],[-6,6], [6,-6]]

    instance = cLocalization(nodes_list, pos)

    instance.plot_point()
    
def test_path():
    pos = [0,0]
    nodes_list = [[-6,-6],[6,6],[-6,6], [6,-6]]

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


test_point()
