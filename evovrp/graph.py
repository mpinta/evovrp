import numpy as np
import evovrp.image as image
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, vehicles, customers, depots):
        self.vehicles = vehicles
        self.customers = customers
        self.depots = depots

    def draw(self, results, fitness):
        plt.figure(figsize=(8, 8), dpi=80)
        self.draw_depots()
        self.draw_customers()
        self.draw_legend()
        self.draw_text(fitness)
        self.draw_connections(results, fitness)
        plt.close()

    def draw_depots(self):
        coordinates = self.get_coordinates(self.depots)
        sorted(coordinates)
        for index, i in enumerate(coordinates):
            if index == 0:
                plt.scatter(i[0], i[1], alpha=0.8, c='C0', edgecolors='C0', s=30, label='Depot')
            plt.scatter(i[0], i[1], alpha=0.8, c='C0', edgecolors='C0', s=30)
            # plt.text(i[0], i[1], str(index + 1), color="black", fontsize=12)

    def draw_customers(self):
        coordinates = self.get_coordinates(self.customers)
        sorted(coordinates)
        for index, i in enumerate(coordinates):
            if index == 0:
                plt.scatter(i[0], i[1], alpha=0.5, c='C1', edgecolors='C1', s=30, label='Customer')
            plt.scatter(i[0], i[1], alpha=0.5, c='C1', edgecolors='C1', s=30)
            # plt.text(i[0], i[1], str(index + 1), color="black", fontsize=10)

    @staticmethod
    def draw_legend():
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=2)

    @staticmethod
    def draw_text(fitness):
        plt.suptitle('Generation: ' + str(fitness.generation) + ', Instance: ' + str(fitness.instance), fontsize=16)
        plt.title('Fitness: ' + str(fitness.value) + '\n' + 'Phenotype: ' + str(fitness.phenotype), fontsize=14)

    def draw_connections(self, results, fitness):
        img = image.Image(str(fitness.generation), str(fitness.instance))
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
        return coordinates
