import numpy as np
import matplotlib.pyplot as plt
import math
import random
from scipy import stats as st


class cLocalization:
    def __init__(self, nodes, pos):
        self.nodes = nodes
        self.pos = pos
        self.distances_to_nodes = []

    # TODO: Calculate position from different points and create localization from that
    def calculate_dis(self):

        self.distances_to_nodes = []
        for i in self.nodes:
            distance = math.sqrt((i[0] - self.pos[0]) ** 2 + (i[1] - self.pos[1]) ** 2)
            self.distances_to_nodes.append(distance)

    def triangulate(self, n, error_margin):
        # Get the x-y pairs of circles around the nodes
        # All circles should have an x-y pair that matches up (within an error_margin)
        # This pair is where the signal is sent from
        # Use fill_circle_vals to get the x-y pairs of a circle
        possible_points = []
        # Use the first 2 circles to build a basis for circle intercepts
        points1 = cLocalization.fill_circle_vals(self.distances_to_nodes[0], self.nodes[0], n)
        points2 = cLocalization.fill_circle_vals(self.distances_to_nodes[1], self.nodes[1], n)
        for i in range(len(points2)):
            for j in range(len(points1)):
                coord1 = points1[j]
                coord2 = points2[i]
                if cLocalization.is_equal(coord1, coord2, error_margin):
                    possible_points.append(coord1)
        for ndx in range(2, len(self.nodes)):
            points = cLocalization.fill_circle_vals(self.distances_to_nodes[ndx], self.nodes[ndx], n)
            for i, _ in enumerate(possible_points):
                match = False
                for j in range(len(points)):
                    if cLocalization.is_equal(possible_points[i], points[j], error_margin):
                        match = True
                if not match:
                    possible_points.pop(i)
        est_pos = st.mode(possible_points).mode
        if len(est_pos) == 0:
            if error_margin > 0.05:
                print("Can't find an intersection, returning.")
                return [[0, 0]]
            print("Couldn't find an intersection, trying again with larger error margin: " + str(error_margin) + "->" + str(error_margin + 0.01))
            est_pos = self.triangulate(n, error_margin + 0.01)
        return est_pos

    @staticmethod
    def is_equal(coord1, coord2, error_mar):
        x_ref, y_ref = coord1
        x_test, y_test = coord2
        x_y_pass = [False, False]
        if x_ref - error_mar <= x_test <= x_ref + error_mar:
            x_y_pass[0] = True
        if y_ref - error_mar <= y_test <= y_ref + error_mar:
            x_y_pass[1] = True
        if all(x_y_pass):
            return True
        else:
            return False

    @staticmethod
    def split_coords(coords):
        x = []
        y = []
        for coord in coords:
            x.append(coord[0])
            y.append(coord[1])
        return x, y

    @staticmethod
    def fill_circle_vals(distance, position, n): #Position is node position
        #Circle equation: (x-pos(x))^2 + (y-pos(y))^2 = distance^2
        step = 2*math.pi/n
        a = position[0]
        b = position[1]
        r = distance
        coords = []
        theta = 0
        while theta < 2*math.pi:
            coords.append((r * math.cos(theta) + a, r * math.sin(theta) + b))
            theta += step
        return coords
            
    
    def add_noise_to_dis(self, abs_error):
        for idx, huts in enumerate(self.distances_to_nodes):
            self.distances_to_nodes[idx] += (random.random() * 2 -1) * abs_error

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

    def plot_point(self):
        for node in self.nodes:
            plt.plot(node[0], node[1], color='green', marker='s')
        plt.plot(self.pos[0], self.pos[1], 'o')
        estim = self.triangulate(1500, 0.01)[0]
        plt.plot(estim[0], estim[1], '^')
        plt.title("Localization Area")
        plt.show()

    def plot_path(self, path):
        est_path = []
        print("Calculating positions")
        for i, coord in enumerate(path):
            self.pos = coord
            self.calculate_dis()
            self.add_noise_to_dis(0.005)
            est_path.append(self.triangulate(1500, 0.01)[0])
            print(str(100*(i+1)/len(path)) + "%")
        for node in self.nodes:
            plt.plot(node[0], node[1],  color='green', marker='s')
        print(est_path)
        x_est, y_est = cLocalization.split_coords(est_path)
        x_path, y_path = cLocalization.split_coords(path)
        plt.plot(x_path, y_path, label='Actual')
        plt.plot(x_est, y_est, label='Predicted')
        plt.legend()
        plt.title("Localization Area")
        plt.show()
