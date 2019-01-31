import csv
from evovrp.eMDVRP.vrp import Vehicle, Customer, Depot, Graph

types = ['vrp', 'pvrp', 'mdvrp', 'sdvrp', 'vrptw', 'pvrptw', 'mdvrptw', 'sdvrptw']


def read_vrp(file_name, type='mdvrptw'):
    data = []

    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ')
        for row in csv_reader:
            data.append(row)
    return _get_objects(data)


def _get_objects(data):
    vehicles = []
    customers = []
    depots = []
    rows = _get_rows(data)

    for i in range(3):
        for j in rows[i]:
            if i == 0:
                vehicles.append(Vehicle(float(j[0]), float(j[1])))
            elif i == 1:
                customers.append(Customer(float(j[0]), float(j[1]), float(j[2]), float(j[3]), float(j[4])))
            elif i == 2:
                depots.append(Depot(float(j[0]), float(j[1]), float(j[2]), float(j[3]), float(j[4])))

    return vehicles, customers, depots


def _get_rows(data):
    vehicle_num = int(data[0][3])
    customer_num = int(data[0][2])
    depot_num = int(data[0][3])

    vehicle_rows = data[1:vehicle_num + 1]
    customer_rows = data[vehicle_num + 1:vehicle_num + customer_num + 1]
    depot_rows = data[vehicle_num + customer_num + 1: vehicle_num + customer_num + depot_num + 1]

    return vehicle_rows, _clean(customer_rows), _clean(depot_rows)


def _clean(rows):
    cleaned = []
    for i in rows:
        row = []
        for j in i:
            if j != '':
                row.append(j)
        cleaned.append(row)
    return cleaned


if __name__ == '__main__':
    objects = read_vrp('../datasets/pr01')
    g = Graph(objects)
    g.draw()
