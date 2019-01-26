import numpy as np
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, vehicles, customers, depots):
        self.vehicles = vehicles
        self.customers = customers
        self.depots = depots

    def draw(self, results):
        self.draw_customers()
        self.draw_depots()
        self.draw_connections(results)
        plt.show()

    def draw_customers(self):
        coordinates = self.get_coordinates(self.customers)
        sorted(self.convert_to_float(coordinates))
        for index, i in enumerate(coordinates):
            plt.scatter(i[0], i[1], alpha=0.5, c='C1', edgecolors='C1', s=30)
            plt.text(i[0], i[1], str(index + 1), color="black", fontsize=10)

    def draw_depots(self):
        coordinates = self.get_coordinates(self.depots)
        sorted(self.convert_to_float(coordinates))
        for index, i in enumerate(coordinates):
            plt.scatter(i[0], i[1], alpha=0.8, c='C0', edgecolors='C0', s=30)
            plt.text(i[0], i[1], str(index + 1), color="black", fontsize=12)

    def draw_connections(self, results):
        for i in results:
            color = np.random.random(3)
            coordinates = self.get_connection_coordinates(i)
            for index_j, j in enumerate(coordinates):
                if index_j == len(coordinates)-1:
                    break
                plt.plot([j[0], coordinates[index_j + 1][0]], [j[1], coordinates[index_j + 1][1]], alpha=0.5, c=color)

    def get_connection_coordinates(self, result):
        coordinates = self.get_coordinates(result.customers)
        coordinates.insert(0, [result.depot.x, result.depot.y])
        coordinates.append([result.depot.x, result.depot.y])
        return self.convert_to_float(coordinates)

    @staticmethod
    def get_coordinates(objects):
        coordinates = []
        for i in objects:
            coordinates.append([i.x, i.y])
        return coordinates

    @staticmethod
    def convert_to_float(data):
        for i in data:
            i[0], i[1] = float(i[0]), float(i[1])
        return data
