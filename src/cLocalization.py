import numpy as np
import matplotlib.pyplot as plt
import math
import random
import scipy
# from scipy import stats as st
from shapely.geometry import LineString
import scipy



class cLocalization:
    def __init__(self, nodes, pos):
        self.nodes = nodes
        self.pos = pos
        self.distances_to_nodes = []

    # TODO: Calculate position from different points and create localization from that
    def calculate_dis(self):
        self.distances_to_nodes = []
        for i in self.nodes:
            # distance = math.sqrt((i[0] - self.pos[0]) ** 2 + (i[1] - self.pos[1]) ** 2)
            distance = np.lingalg.norm(i-self.pos)
            self.distances_to_nodes.append(distance)

    def add_noise_to_dis(self, abs_error):
        for idx, huts in enumerate(self.distances_to_nodes):
            self.distances_to_nodes[idx] += (random.random() * 2 - 1) * abs_error

    # Interesting method to look at is the scipy least squares: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html
    # This function will just look for the correct return value


    def triangulate(self, n, acc=0):
        # Get the x-y pairs of circles around the nodes
        # All circles should have an x-y pair that matches up (within an error_margin)
        # This pair is where the signal is sent from
        # Use fill_circle_vals to get the x-y pairs of a circle
        possible_points = []
        for ndx in range(1, len(self.nodes)):
            x_1, y_1 = cLocalization.fill_circle_vals(np.asarray(self.distances_to_nodes[ndx - 1]) + acc,
                                                      self.nodes[ndx - 1], n)
            x_2, y_2 = cLocalization.fill_circle_vals(np.asarray(self.distances_to_nodes[ndx]) + acc, self.nodes[ndx],
                                                      n)
            first_line = LineString(np.column_stack((x_1, y_1)))
            second_line = LineString(np.column_stack((x_2, y_2)))
            intersection = first_line.intersection(second_line)
            if intersection.geom_type == 'MultiPoint':
                x, y = LineString(np.asarray(intersection)).xy
                possible_points += cLocalization.tuple_coord_from_list(x, y)
            elif intersection.geom_type == 'Point':
                x, y = intersection.xy
                possible_points += cLocalization.tuple_coord_from_list(x, y)
            else:
                if acc > 0.1:
                    print("Failed to find user")
                    return [0, 0]
                print("Can't find user, retrying with lower accuracy.")
                return self.triangulate(n, acc + 0.003)
        # mode doesn't work on noisy tuples, need to find another way to extract which tuple is most common with a tolerance
        return cLocalization.find_mode(possible_points)

    def triangulate_least_squares(self, room_points=None):
        return_val = None
        if room_points.any() != None:
            mid_room = np.average(room_points, axis=1)
            return_val = scipy.optimize.least_squares(self.get_error, x0=mid_room, bounds=([0,0],[10,10]), args=(self.nodes, self.distances_to_nodes))
        else:
            return_val = scipy.optimize.least_squares(self.get_error, x0 = np.array([0,0]),
                                                      args=(self.nodes, self.distances_to_nodes))
        return return_val.x

    @staticmethod
    def get_error(pos: np.ndarray, nodes: np.ndarray, distances: np.ndarray):
        total_error = 0
        for i, x in enumerate(distances):
            total_error += np.abs(distances[i] - np.sqrt((nodes[i][0] - pos[0]) ** 2 + (nodes[i][1] - pos[1]) ** 2))

        return total_error

    @staticmethod
    def find_mode(points):
        if len(points) > 1:
            points.sort()
            x, y = cLocalization.split_coords(points)
            diff_x = np.absolute(np.diff(x))
            diff_y = np.absolute(np.diff(y))
            ndx_min = np.argmin(cLocalization.gen_magnitudes(diff_x, diff_y))
            return points[ndx_min]
        else:
            return points[0]

    @staticmethod
    def gen_magnitudes(x, y):
        results = []
        for i in range(len(x)):
            results.append(math.sqrt(x[i] ** 2 + y[i] ** 2))
        return results

    @staticmethod
    def fill_circle_vals(distance, position, n):  # Position is node position
        # Circle equation: (x-pos(x))^2 + (y-pos(y))^2 = distance^2
        step = 2 * math.pi / n
        a = position[0]
        b = position[1]
        r = distance
        x = []
        y = []
        theta = 0
        while theta < 2 * math.pi:
            x.append(r * math.cos(theta) + a)
            y.append(r * math.sin(theta) + b)
            theta += step
        return x, y

    @staticmethod
    def tuple_coord_from_list(x, y):
        coords = []
        for i in range(len(x)):
            coords.append((x[i], y[i]))
        return coords
    

    @staticmethod
    def split_coords(coords):
        x = []
        y = []
        for coord in coords:
            x.append(coord[0])
            y.append(coord[1])
        return x, y

    def trilaterate(self, points, distances):
        # ported from https://github.com/gheja/trilateration.js
        # points -> list of np arrays in the form of [[x, y, z], [x, y, z]
        # distances -> np array [r1, r2, r3]
        p1 = points[:,0]
        p2 = points[:,1]
        p3 = points[:,2]
        r1, r2, r3 = distances

        def norm(v):
            return np.sqrt(np.sum(v ** 2))

        def dot(v1, v2):
            return np.dot(v1, v2)

        def cross(v1, v2):
            return np.cross(v1, v2)

        ex = (p2 - p1) / norm(p2 - p1)
        i = dot(ex, p3 - p1)
        a = (p3 - p1) - ex * i
        ey = a / norm(a)
        ez = cross(ex, ey)
        d = norm(p2 - p1)
        j = dot(ey, p3 - p1)
        x = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
        y = (r1 ** 2 - r3 ** 2 + i ** 2 + j ** 2) / (2 * j) - (i / j) * x
        b = r1 ** 2 - x ** 2 - y ** 2

        # floating point math flaw in IEEE 754 standard
        # see https://github.com/gheja/trilateration.js/issues/2
        if (np.abs(b) < 0.0000000001):
            b = 0

        z = np.sqrt(b)
        if np.isnan(z):
            raise Exception('NaN met, cannot solve for z')

        a = p1 + ex * x + ey * y
        p4a = a + ez * z
        p4b = a - ez * z

        return p4a, p4b

    def __str__(self):
        return_string = f""
        return_string += f"Current Class has: \n"
        for idx, val in enumerate(self.nodes):
            return_string += f"Node {idx}: {val}\n"
        return_string += f"Pos: {self.pos}\n"
        return_string += f"Current distances: \n"
        for i in self.distances_to_nodes:
            return_string += f"    {i}\n"

        return return_string


    def plot_point(self):
        for node in self.nodes:
            plt.plot(node[0], node[1], color='green', marker='s')
        plt.plot(self.pos[0], self.pos[1], 'o')
        self.calculate_dis()
        self.add_noise_to_dis(0.03)
        estim = self.triangulate(100)
        print(f"Estimated value normal: {estim}")
        estim = self.triangulate_least_squares().x
        print(f"Estimated value least_sq: {estim}")
        plt.plot(estim[0], estim[1], '^')
        plt.title("Localization Area")
        plt.savefig("Point.pdf")
        plt.show()

    def plot_path(self, path):
        est_path = []
        print("Calculating positions")
        for i, coord in enumerate(path):
            self.pos = coord
            self.calculate_dis()
            self.add_noise_to_dis(0.05)
            est_path.append(self.triangulate_least_squares(None))
            print(str(100 * (i + 1) / len(path)) + "%")
        for node in self.nodes:
            plt.plot(node[0], node[1], color='green', marker='s')
        x_est, y_est = cLocalization.split_coords(est_path)
        x_path, y_path = cLocalization.split_coords(path)
        plt.plot(x_path, y_path, label='Actual')
        plt.plot(x_est, y_est, label='Predicted')
        plt.legend()
        plt.title("Localization Area")
        plt.savefig("Path.pdf")
        plt.show()


