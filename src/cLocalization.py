import numpy as np
import math
import random


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

    def triangulate(self):
        # Get the x-y pairs of circles around the nodes
        # All circles should have an x-y pair that matches up (within an error_margin)
        # This pair is where the signal is sent from
        # Use fill_circle_vals to get the x-y pairs of a circle
        return 0

    @staticmethod
    def fill_circle_vals(distance, position, n): #Position is node position
        #Circle equation: (x-pos(x))^2 + (y-pos(y))^2 = distance^2
        print(distance)
        x_and_y = []
        x_pos, y_pos = position[0], position[1]
        for x in np.linspace(-distance+x_pos, distance+x_pos, n):
            print(x)
            c = y_pos**2 + x**2 - distance**2 -2*x_pos*x + x_pos**2
            y1, y2, sols = cLocalization.quadratic_function(1, -2*y_pos, c)
            match sols:
                case 1:
                    x_and_y.append((x, y1))
                case 2:
                    x_and_y.append((x, y1))
                    x_and_y.append((x, y2))
                case _:
                    print("Something went wrong in fill_circle_vals()")
        return x_and_y
            
    @staticmethod
    def quadratic_function(a, b, c):
        try:
            discriminant = math.sqrt(b**2 - 4*a*c)
            if discriminant == 0:
                return (-b/(2*a), 0, 1)
            else:
                return ((-b+discriminant)/(2*a), (-b-discriminant)/(2*a), 2)
        except ValueError:
            print("Imaginary root, invalid node?")
    
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

