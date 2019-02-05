import csv
import evovrp.classes as classes


class File(object):
    """Class reads and parses input files.

    Class reads input files or so-called "datasets" and parses them
    into specific objects.

    Attributes:
        data: A static array of strings, indicating data which
        was read.
    """

    data = []

    @staticmethod
    def read(file_name):
        """Reads a csv file.

        Reads a csv file and appends each row to a static array
        of strings.

        Args:
            file_name: A string, indicating name of a file which
            will be read.

        Returns:
            A method, which returns an array consisting of three
            different arrays, each with different type, storing
            parsed data as objects.
            Types are: Vehicle, Customer and Depot.
        """

        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=' ')
            for row in csv_reader:
                File.data.append(row)
        return File.get_objects()

    @staticmethod
    def get_objects():
        """Creates objects from data.

        Creates and parses data, which is in form of string rows,
        to objects with Vehicle, Customer and Depot types.

        Args:
            Method does not have any arguments.

        Returns:
            An array consisting of three different arrays, each
            with different type, storing parsed data as objects.
            Types are: Vehicle, Customer and Depot.
        """

        vehicles = []
        customers = []
        depots = []
        rows = File.get_rows()

        for i in range(3):
            for j in rows[i]:
                if i == 0:
                    vehicles.append(classes.Vehicle(float(j[0]), float(j[1])))
                elif i == 1:
                    customers.append(classes.Customer(float(j[0]), float(j[1]), float(j[2]), float(j[3]), float(j[4])))
                elif i == 2:
                    depots.append(classes.Depot(float(j[0]), float(j[1]), float(j[2])))
        return [vehicles, customers, depots]

    @staticmethod
    def get_rows():
        """Gets individual rows from data.

        Gets individual rows from data and stores them separately
        into three different arrays.

        Args:
            Method does not have any arguments.

        Returns:
            An array consisting of three different arrays, each
            with own cleaned data rows in form of strings.
        """

        vehicle_num = int(File.data[0][3])
        customer_num = int(File.data[0][2])
        depot_num = int(File.data[0][3])

        vehicle_rows = File.data[1:vehicle_num + 1]
        customer_rows = File.data[vehicle_num + 1:vehicle_num + customer_num + 1]
        depot_rows = File.data[vehicle_num + customer_num + 1: vehicle_num + customer_num + depot_num + 1]
        return [vehicle_rows, File.clean(customer_rows), File.clean(depot_rows)]

    @staticmethod
    def clean(rows):
        """Cleans data rows.

        Cleans each individual row of data and so removes
        unnecessary spaces.

        Args:
            rows: An array of strings, indicating data rows.

        Returns:
            An array of strings.
        """

        cleaned = []
        for i in rows:
            row = []
            for j in i:
                if j != '':
                    row.append(j)
            cleaned.append(row)
        return cleaned
