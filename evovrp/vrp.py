import csv
import matplotlib.pyplot as plt


class Vehicle:
    def __init__(self, max_duration, max_capacity):
        self.max_duration = max_duration
        self.max_capacity = max_capacity

    def __str__(self):
        return '[%s, %s]' % (self.max_duration, self.max_capacity)

    def __repr__(self):
        return str(self)


class Customer:
    def __init__(self, key, x, y, stacking_time, capacity):
        self.key = key
        self.x = x
        self.y = y
        self.stacking_time = stacking_time
        self.capacity = capacity

    def __str__(self):
        return '[%s, %s, %s, %s, %s]' % (self.key, self.x, self.y, self.stacking_time, self.capacity)

    def __repr__(self):
        return str(self)


class Depot:
    def __init__(self, key, x, y, max_duration, max_capacity):
        self.key = key
        self.x = x
        self.y = y
        self.max_duration = max_duration
        self.max_capacity = max_capacity

    def __str__(self):
        return '[%s, %s, %s, %s, %s]' % (self.key, self.x, self.y, self.max_duration, self.max_capacity)

    def __repr__(self):
        return str(self)


class File:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = []

    def read(self):
        # with open('datasets/' + self.file_name) as csv_file:
        with open(self.file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=' ')
            for row in csv_reader:
                self.data.append(row)
        return self.get_objects()

    def get_objects(self):
        vehicles = []
        customers = []
        depots = []
        rows = self.get_rows()

        for i in range(3):
            for j in rows[i]:
                if i == 0:
                    vehicles.append(Vehicle(j[0], j[1]))
                elif i == 1:
                    customers.append(Customer(j[0], j[1], j[2], j[3], j[4]))
                elif i == 2:
                    depots.append(Depot(j[0], j[1], j[2], j[3], j[4]))

        return [vehicles, customers, depots]

    def get_rows(self):
        vehicle_num = int(self.data[0][3])
        customer_num = int(self.data[0][2])
        depot_num = int(self.data[0][3])

        vehicle_rows = self.data[1:vehicle_num + 1]
        customer_rows = self.data[vehicle_num + 1:vehicle_num + customer_num + 1]
        depot_rows = self.data[vehicle_num + customer_num + 1: vehicle_num + customer_num + depot_num + 1]

        return [vehicle_rows, self.clean(customer_rows), self.clean(depot_rows)]

    def clean(self, rows):
        cleaned = []
        for i in rows:
            row = []
            for j in i:
                if j != '':
                    row.append(j)
            cleaned.append(row)
        return cleaned


class Graph:
    def __init__(self, objects):
        self.objects = objects

    def draw(self):
        self.draw_customers()
        self.draw_depots()
        plt.show()

    def draw_customers(self):
        coordinates = self.get_coordinates(objects[1])
        sorted(self.convert_to_float(coordinates))
        for i in coordinates:
            plt.scatter(i[0], i[1], alpha=0.5, c='C1', edgecolors='C1', s=30)

    def draw_depots(self):
        coordinates = self.get_coordinates(objects[2])
        sorted(self.convert_to_float(coordinates))
        for i in coordinates:
            plt.scatter(i[0], i[1], alpha=0.8, c='C0', edgecolors='C0', s=30)

    def get_coordinates(self, objects):
        coordinates = []
        for i in objects:
            coordinates.append([i.x, i.y])
        return coordinates

    def convert_to_float(self, data):
        for i in data:
            i[0], i[1] = float(i[0]), float(i[1])
        return data


if __name__ == '__main__':
    f = File('../datasets/pr01')
    objects = f.read()
    g = Graph(objects)
    g.draw()
