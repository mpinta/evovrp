import csv

from evovrp.classes import Vehicle, Customer, Depot


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

    @staticmethod
    def clean(rows):
        cleaned = []

        for i in rows:
            row = []
            for j in i:
                if j != '':
                    row.append(j)
            cleaned.append(row)
        return cleaned
