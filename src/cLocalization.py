import numpy as np

class cLocalization:
    def __init__(self, nodes):
        self.nodes = nodes
        self.pos = None
        self.distances_to_nodes = None

    def calculate_dis(self):
        # TODO: Calculate position from different points and create localization from that
        pass

    def __str__(self):
        return_string = f""
        return_string += f"Current Class has: \n"
        for idx, val in enumerate(self.nodes):
            return_string += f"Node {idx}: {val[0]}, {val[1]}\n"
        return return_string

