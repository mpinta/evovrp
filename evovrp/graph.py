import numpy as np
import evovrp.image as image
import evovrp.utils as utils
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, vehicles, customers, depots):
        self.vehicles = vehicles
        self.customers = customers
        self.depots = depots

    def draw(self, results):
        plt.figure()
        self.draw_customers()
        self.draw_depots()
        self.draw_connections(results)
        plt.close()

    def draw_customers(self):
        coordinates = self.get_coordinates(self.customers)
        sorted(utils.convert_to_float(coordinates))
        for index, i in enumerate(coordinates):
            plt.scatter(i[0], i[1], alpha=0.5, c='C1', edgecolors='C1', s=30)
            plt.text(i[0], i[1], str(index + 1), color="black", fontsize=10)

    def draw_depots(self):
        coordinates = self.get_coordinates(self.depots)
        sorted(utils.convert_to_float(coordinates))
        for index, i in enumerate(coordinates):
            plt.scatter(i[0], i[1], alpha=0.8, c='C0', edgecolors='C0', s=30)
            plt.text(i[0], i[1], str(index + 1), color="black", fontsize=12)

    def draw_connections(self, results):
        img = image.Image(utils.convert_to_string(results[0].generation), utils.convert_to_string(results[0].instance))
        img.save(plt)

        for i in results:
            color = np.random.random(3)
            coordinates = self.get_connection_coordinates(i)

            for index, j in enumerate(coordinates):
                if index == len(coordinates)-1:
                    break
                plt.plot([j[0], coordinates[index + 1][0]], [j[1], coordinates[index + 1][1]], alpha=0.5, c=color)
                img.save(plt)
        img.create_gif()

    @staticmethod
    def get_coordinates(objects):
        coordinates = []
        for i in objects:
            coordinates.append([i.x, i.y])
        return coordinates

    def get_connection_coordinates(self, result):
        coordinates = self.get_coordinates(result.customers)
        coordinates.insert(0, [result.depot.x, result.depot.y])
        coordinates.append([result.depot.x, result.depot.y])
        return utils.convert_to_float(coordinates)
