import matplotlib.pyplot as plt


class Graph:
    def __init__(self, objects):
        self.objects = objects

    def draw(self):
        self.draw_customers()
        self.draw_depots()
        plt.show()

    def draw_customers(self):
        coordinates = self.get_coordinates(self.objects[1])
        sorted(self.convert_to_float(coordinates))
        for index, i in enumerate(coordinates):
            plt.scatter(i[0], i[1], alpha=0.5, c='C1', edgecolors='C1', s=30)
            plt.text(i[0], i[1], str(index + 1), color="black", fontsize=10)

    def draw_depots(self):
        coordinates = self.get_coordinates(self.objects[2])
        sorted(self.convert_to_float(coordinates))
        for index, i in enumerate(coordinates):
            plt.scatter(i[0], i[1], alpha=0.8, c='C0', edgecolors='C0', s=30)
            plt.text(i[0], i[1], str(index + 1), color="black", fontsize=12)

    def get_coordinates(self, objects):
        coordinates = []
        for i in objects:
            coordinates.append([i.x, i.y])
        return coordinates

    def convert_to_float(self, data):
        for i in data:
            i[0], i[1] = float(i[0]), float(i[1])
        return data
