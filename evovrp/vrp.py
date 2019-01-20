import csv
import numpy as np
import matplotlib.pyplot as plt

from NiaPy.algorithms.basic.ga import GeneticAlgorithm
from NiaPy.util import Task, OptimizationType
from random import randint


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
        for index, i in enumerate(coordinates):
            plt.scatter(i[0], i[1], alpha=0.5, c='C1', edgecolors='C1', s=30)
            plt.text(i[0], i[1], str(index + 1), color="black", fontsize=10)

    def draw_depots(self):
        coordinates = self.get_coordinates(objects[2])
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


class ExampleBenchmark(object):
    def __init__(self, objects):
        self.Lower = 0
        self.Upper = 10
        self.objects = objects

    def function(self):
        vehicles = self.objects[0]
        customers = self.objects[1]
        depots = self.objects[2]

        def evaluate(D, sol):
            results = []
            curr_result = [0, 0, 0]
            fitness = 0.0
            vd_counter = 0
            node_counter = 0
            vehicle_changed = False
            phenotype = ExampleBenchmark.to_phenotype(sol)
 
            for i in range(D):
                node_counter += 1
                vehicle, depot = self.set_vehicle_and_depot(vd_counter, vehicles, depots)

                befo_customer = self.find_before_customer(i, vehicle_changed, customers, phenotype)
                curr_customer = self.find_customer(customers, phenotype[i])
                next_customer = self.find_next_customer(i, customers, phenotype)
                
                curr_result = self.get_result(vehicle, depot, curr_result, befo_customer, curr_customer)
                curr_result.append(node_counter)
                vehicle_changed = False

                if self.check_next_customer(vehicle, depot, curr_result, curr_customer, 
                befo_customer, next_customer) == False:
                    results.append(curr_result)
                    curr_result = [0, 0, 0]
                    vehicle_changed = True
                    vd_counter = self.set_vd_counter(vd_counter, vehicles)
                    node_counter = 0
            
            return ExampleBenchmark.get_fitness(results)

        return evaluate

    def to_phenotype(sol):
        return np.argsort(np.argsort(sol)) + 1

    def get_fitness(results):
        fitness = 0.0
        for i in results:
            fitness = fitness + abs(1/i[1] - i[2])
        return fitness

    def find_before_customer(self, i, vehicle_changed, customers, phenotype):
        if i == 0 or vehicle_changed == True:
            vehicle_changed = False
            return -1
        return self.find_customer(customers, phenotype[i - 1])

    def find_next_customer(self, i, customers, phenotype):
        if (i + 1) >= len(customers):
            return -1
        return self.find_customer(customers, phenotype[i + 1])

    def find_customer(self, customers, key):
        for i in customers:
            if i.key == str(key):
                return i

    def set_vehicle_and_depot(self, vd_counter, vehicles, depots):
        return vehicles[vd_counter], depots[vd_counter]

    def set_vd_counter(self, vd_counter, vehicles):
        if (vd_counter + 1) >= len(vehicles):
            return 0
        return vd_counter + 1

    def get_result(self, vehicle, depot, curr_result, befo_customer, curr_customer):
        return[curr_result[0] + float(curr_customer.capacity), 
        curr_result[1] + self.get_distance(vehicle, depot, befo_customer, curr_customer)]

    def get_distance(self, vehicle, depot, befo_customer, curr_customer):
        if befo_customer == -1:
            x1 = float(depot.x)
            y1 = float(depot.y)  
        else:
            x1 = float(befo_customer.x)
            y1 = float(befo_customer.y)

        x2 = float(curr_customer.x)
        y2 = float(curr_customer.y)

        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def check_next_customer(self, vehicle, depot, curr_result, curr_customer, before_customer, next_customer):
        if next_customer == -1:
            return False

        next_capacity = curr_result[0] + float(next_customer.capacity)
        next_distance = curr_result[1] + self.get_distance(vehicle, depot, curr_customer, next_customer)

        if next_capacity > float(vehicle.max_capacity) or next_distance > float(vehicle.max_duration):
            return False  
        return True


if __name__ == '__main__':
    f = File('../datasets/example')
    objects = f.read()

    rand_seed = randint(1000, 10000)
    task = Task(D=len(objects[1]), nGEN=20, benchmark=ExampleBenchmark(objects), optType=OptimizationType.MINIMIZATION)
    ga = GeneticAlgorithm(seed=1234, task=task, NP=50)

    result, fitness = ga.run()
    print(result, fitness)
    print(ExampleBenchmark.to_phenotype(result))

    g = Graph(objects)
    g.draw()