from cLocalization import cLocalization

def test_skeleton():
    pos = [0,0]
    nodes_list = [[1,1],[0,0],[1,3], [5,2], [-1, 6]]

    instance = cLocalization(nodes_list, pos)
    instance.calculate_dis()

    print(instance)

    instance.add_noise_to_dis(2)
    print(instance)

def test_path():
    pos = [0,0]
    nodes_list = [[-3,-3],[3,3],[-3,3], [3,-3]]

    instance = cLocalization(nodes_list, pos)
    instance.calculate_dis()
    instance.add_noise_to_dis(0.05)

    path = [[0,0], [0.1, 0.1], [0.2, 0.2], [1, 1]]
    instance.plot_path(path)
