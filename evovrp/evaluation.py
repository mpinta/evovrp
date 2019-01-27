import numpy as np
import evovrp.graph as graph
import evovrp.classes as classes


class Evaluation(object):
    def __init__(self, objects, population_size):
        self.Lower = 0
        self.Upper = 10
        self.penalty = 20
        self.vehicles = objects[0]
        self.customers = objects[1]
        self.depots = objects[2]
        self.instance_counter = 0
        self.generation_counter = 1
        self.population_size = population_size

    def function(self):
        def evaluate(d, sol):
            self.set_instance_counter()
            self.set_generation_counter()

            results = []
            vehicle_depot_counter = 0
            vehicle_depot_changed = False
            phenotype = self.to_phenotype(sol)
            curr_result = classes.Result(self.generation_counter, self.instance_counter)

            g = graph.Graph(self.vehicles, self.customers, self.depots)

            for i in range(d):
                curr_result = self.set_vehicle_depot(curr_result, vehicle_depot_counter)

                pre_customer = self.find_previous_customer(i, vehicle_depot_changed, phenotype)
                curr_customer = self.find_customer(phenotype[i])
                nxt_customer = self.find_next_customer(i, phenotype)

                curr_result = self.get_result(curr_result, pre_customer, curr_customer)
                curr_result = self.add_customer_to_result(curr_result, curr_customer)
                vehicle_depot_changed = False

                if not self.check_next_customer(curr_result, curr_customer, nxt_customer):
                    curr_result = self.get_last_distance(curr_result, curr_customer)

                    if self.check_for_penalty(curr_result):
                        self.add_penalty(curr_result)

                    results.append(curr_result)
                    curr_result = classes.Result(self.generation_counter, self.instance_counter)
                    vehicle_depot_changed = True
                    vehicle_depot_counter = self.set_vehicle_depot_counter(vehicle_depot_counter)

            g.draw(results)
            return self.get_fitness(results)
        return evaluate

    def set_instance_counter(self):
        self.instance_counter += 1

    def set_generation_counter(self):
        if self.instance_counter > self.population_size:
            self.generation_counter += 1
            self.instance_counter = 1

    def set_vehicle_depot_counter(self, vehicle_depot_counter):
        if (vehicle_depot_counter + 1) >= len(self.vehicles):
            return 0
        return vehicle_depot_counter + 1

    def set_vehicle_depot(self, curr_result, vehicle_depot_counter):
        curr_result.vehicle = self.vehicles[vehicle_depot_counter]
        curr_result.depot = self.depots[vehicle_depot_counter]
        return curr_result

    def find_customer(self, key):
        for i in self.customers:
            if i.key == str(key):
                return i

    def find_previous_customer(self, i, vehicle_depot_changed, phenotype):
        if i == 0 or vehicle_depot_changed is True:
            return -1
        return self.find_customer(phenotype[i - 1])

    def find_next_customer(self, i, phenotype):
        if (i + 1) >= len(self.customers):
            return -1
        return self.find_customer(phenotype[i + 1])

    @staticmethod
    def check_for_penalty(curr_result):
        if curr_result.distance > float(curr_result.vehicle.max_duration):
            return True
        return False

    def check_next_customer(self, curr_result, curr_customer, nxt_customer):
        if nxt_customer == -1:
            return False

        nxt_capacity = curr_result.capacity + float(nxt_customer.capacity)
        nxt_distance = curr_result.distance + self.get_distance(curr_result.depot, curr_customer, nxt_customer)

        if nxt_capacity > float(curr_result.vehicle.max_capacity) or nxt_distance > \
                float(curr_result.vehicle.max_duration):
            return False
        return True

    @staticmethod
    def get_distance(depot, customer_one, customer_two):
        if customer_one == -1:
            x1 = float(depot.x)
            y1 = float(depot.y)
        else:
            x1 = float(customer_one.x)
            y1 = float(customer_one.y)

        if customer_two == -1:
            x2 = float(depot.x)
            y2 = float(depot.y)
        else:
            x2 = float(customer_two.x)
            y2 = float(customer_two.y)

        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def get_fitness(results):
        fitness = 0.0
        for i in results:
            fitness += i.distance
        return fitness

    def get_result(self, curr_result, pre_customer, curr_customer):
        curr_result.capacity += float(curr_customer.capacity)
        curr_result.distance += self.get_distance(curr_result.depot, pre_customer, curr_customer)
        return curr_result

    def get_last_distance(self, curr_result, curr_customer):
        curr_result.distance += self.get_distance(curr_result.depot, curr_customer, -1)
        return curr_result

    @staticmethod
    def add_customer_to_result(curr_result, curr_customer):
        curr_result.customers.append(curr_customer)
        return curr_result

    def add_penalty(self, curr_result):
        curr_result.distance += self.penalty
        return curr_result

    @staticmethod
    def to_phenotype(sol):
        return np.argsort(np.argsort(sol)) + 1
