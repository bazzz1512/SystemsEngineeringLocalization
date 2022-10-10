import numpy as np
import math


class cLocalization:
    def __init__(self, nodes, pos):
        self.nodes = nodes
        self.pos = pos
        self.distances_to_nodes = []

    def calculate_dis(self):
        # TODO: Calculate position from different points and create localization from that
        self.distances_to_nodes = []
        for i in self.nodes:
            distance = math.sqrt((i[0] - self.pos[0]) ** 2 + (i[1] - self.pos[1]) ** 2)
            self.distances_to_nodes.append(distance)

    def __str__(self):
        return_string = f""
        return_string += f"Current Class has: \n"
        for idx, val in enumerate(self.nodes):
            return_string += f"Node {idx}: {val[0]}, {val[1]}\n"
        return_string += f"Pos: {self.pos[0]}, {self.pos[1]}\n"
        return_string += f"Current distances: \n"
        for i in self.distances_to_nodes:
            return_string += f"    {i}\n"

        return return_string
