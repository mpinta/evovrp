from evovrp.eMDVRP import Reader, Printer
from evovrp.eMDVRP.vrp import Depot
import numpy as np
from NiaPy.algorithms.basic.ba import BatAlgorithm
from NiaPy.util import Task, OptimizationType
import math


class FillStation(object):
    def __init__(self, key, x, y, filling_time):
        self.key = key
        self.x = x
        self.y = y
        self.filling_time = filling_time


class ExampleBenchmark(object):

    def __init__(self, vehicles, customers, depots, fill_stations):
        # Nastavimo zgornjo in spodnjo mejo za vsako vrednost v polju sol genotipa.
        self.Lower = 0
        self.Upper = 1

        self.customers = customers
        self.depots = depots
        self.vehicles = vehicles
        # self.fill_stations = depots + fill_stations
        self.fill_stations = fill_stations

        self.fill_stations_mapping = np.linspace(0, 1, len(self.fill_stations) + 1)
        self.customers_maping = np.linspace(0, 1, len(self.customers) + 1)

    def function(self):
        def evaluate(D, sol, return_path=False):
            """ To se zažene na vsekem primerku v populaciji, da ga oceni.
                D je velikost polja tega enega primerka.
                sol je polje tega primerka
            """

            # 1. korak: najprej pretvori genotip sol v fenotip

            phenotype = ExampleBenchmark.to_phenotype(sol)
            # times = dict()
            path = list()

            # 2. korak: zdaj pa oceni kvaliteto tega fenotipa

            fitness = 0.0  # To je končna ocena

            vehicle_i = 0
            vehicle_space = self.vehicles[vehicle_i].max_capacity
            # vehicle_duration = self.vehicles[vehicle_i].max_duration
            vehicle_tank = 150
            vehicle_distance = 0.0
            vehicle_depot = depots[vehicle_i]
            # times[vehicle_i] = 0.0

            current = depots[0]

            i = 0
            while i < len(phenotype):
                # for i in range(len(phenotype)):
                next = self.customers[phenotype[i]]
                if vehicle_space < next.capacity:
                    next = vehicle_depot

                distance = math.sqrt(
                    (current.x - next.x) ** 2 +
                    (current.y - next.y) ** 2
                )

                vehicle_distance = vehicle_distance + distance
                # vehicle_tank = vehicle_tank - distance  # krat za težkost

                if not isinstance(next, Depot):
                    vehicle_space = vehicle_space - next.capacity

                # times[vehicle_i] = times[vehicle_i] + path_time

                if vehicle_tank > 0:
                    fitness = fitness + distance
                    path.append((current.x, current.y, next.x, next.y, vehicle_i))
                else:  # ko pade tank pod kritično mejo
                    elec = self.fill_stations[np.digitize(sol[i], self.fill_stations_mapping) - 1]
                    distance_current_elect = math.sqrt(
                        (current.x - elec.x) ** 2 +
                        (current.y - elec.y) ** 2
                    )
                    distance_elect_next = math.sqrt(
                        (elec.x - next.x) ** 2 +
                        (elec.y - next.y) ** 2
                    )

                    fitness = fitness + distance_current_elect + distance_elect_next
                    path.append((current.x, current.y, elec.x, elec.y, vehicle_i))
                    path.append((elec.x, elec.y, next.x, next.y, vehicle_i))
                    vehicle_tank = 150

                    if isinstance(elec, Depot):
                        vehicle_space = self.vehicles[vehicle_i].max_capacity

                if isinstance(next, Depot):
                    vehicle_i = (vehicle_i + 1) % len(self.vehicles)
                    vehicle_space = self.vehicles[vehicle_i].max_capacity
                    # vehicle_duration = float(self.vehicles[vehicle_i].max_duration)
                    vehicle_tank = 150
                    vehicle_depot = depots[vehicle_i]

                    vehicle_distance = 0.0
                    current = vehicle_depot
                else:  # Finished all, make trip back home
                    i = i + 1
                    current = next
            else:
                next = vehicle_depot
                distance = math.sqrt(
                    (current.x - next.x) ** 2 +
                    (current.y - next.y) ** 2
                )

                vehicle_distance = vehicle_distance + distance
                fitness = fitness + distance
                path.append((current.x, current.y, next.x, next.y, vehicle_i))

            if return_path:
                return path
            else:
                return fitness

        return evaluate

    def to_phenotype(sol):
        # return np.argsort(np.argsort(sol))
        return np.argsort(np.argsort(sol))


if __name__ == '__main__':
    vrp = Reader.read_vrp('../datasets/pr01')
    vehicles, customers, depots = vrp
    random_seed = 1234

    r"""
    D {integer} -- Number of dimensions
    nFES {integer} -- Number of function evaluations
    nGEN {integer} -- Number of generations or iterations
    benchmark {class} or {string} -- Problem to solve
    o {array} -- Array for shifting
    of {function} -- Function applied on shifted input
    M {matrix} -- Matrix for rotating
    fM {function} -- Function applied after rotating
    optF {real} -- Value added to benchmark function return
    """

    fill_stations = [FillStation(0, 50, 50, 20),
                     FillStation(0, 50, -50, 20),
                     FillStation(0, -50, 50, 20),
                     FillStation(0, -50, -50, 20)]

    # D je število customerjev
    task = Task(D=len(customers),
                nGEN=10000,
                benchmark=ExampleBenchmark(vehicles, customers, depots, fill_stations),
                optType=OptimizationType.MINIMIZATION)

    # NP - število primerkov v populaciji
    ga = BatAlgorithm(seed=random_seed, task=task, NP=15000)
    # ga = GeneticAlgorithm(seed=random_seed, task=task, NP=150)
    rezultat, fitness = ga.run()
    print(rezultat, fitness)
    print(ExampleBenchmark.to_phenotype(rezultat))

    benchmark = ExampleBenchmark(vehicles, customers, depots, fill_stations)
    benchmark_function = benchmark.function()

    Printer.draw(customers,
                 depots,
                 paths=benchmark_function(len(customers), rezultat, return_path=True),
                 fill_stations=fill_stations)
