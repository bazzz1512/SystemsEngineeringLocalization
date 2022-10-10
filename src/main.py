from cLocalization import cLocalization

pos = [0,0]
nodes_list = [[1,1],[0,0],[1,3], [5,2], [-1, 6]]

instance = cLocalization(nodes_list, pos)
instance.calculate_dis()

print(instance)