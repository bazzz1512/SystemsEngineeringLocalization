import numpy as np

class cLocalization:
    def __init__(self, nodes):
        self.nodes = nodes
        self.pos = None
        self.distances = None

    def calculate_dis(self):
        # TODO: Calculate position from different points and create localization from that