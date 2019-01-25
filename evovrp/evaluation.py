import numpy as np


class Evaluation(object):
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
            phenotype = Evaluation.to_phenotype(sol)

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

            return Evaluation.get_fitness(results)

        return evaluate

    def to_phenotype(sol):
        return np.argsort(np.argsort(sol)) + 1

    def get_fitness(results):
        fitness = 0.0
        for i in results:
            fitness = fitness + abs(1 / i[1] - i[2])
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
        return [curr_result[0] + float(curr_customer.capacity),
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

        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def check_next_customer(self, vehicle, depot, curr_result, curr_customer, before_customer, next_customer):
        if next_customer == -1:
            return False

        next_capacity = curr_result[0] + float(next_customer.capacity)
        next_distance = curr_result[1] + self.get_distance(vehicle, depot, curr_customer, next_customer)

        if next_capacity > float(vehicle.max_capacity) or next_distance > float(vehicle.max_duration):
            return False
        return True