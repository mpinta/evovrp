class Vehicle:
    """Class represents a vehicle.

    Class represents a vehicle as an object.

    Attributes:
        max_duration: A float, indicating vehicles maximum duration.
        max_capacity: A float, indicating vehicles maximum capacity.
    """

    def __init__(self, max_duration, max_capacity):
        """Inits Vehicle with maximum duration and maximum capacity."""
        self.max_duration = max_duration
        self.max_capacity = max_capacity


class Customer:
    """Class represents a customer.

    Class represents a customer as an object.

    Attributes:
        key: An integer, indicating customers identification number.
        x: A float, indicating customers x-coordinate.
        y: A float, indicating customers y-coordinate.
        stacking_time: A float, indicating customers stacking time.
        capacity: A float, indicating customers capacity.
    """

    def __init__(self, key, x, y, stacking_time, capacity):
        """Inits Vehicle with identification number, x-coordinate,
        y-coordinate, stacking time and capacity."""
        self.key = key
        self.x = x
        self.y = y
        self.stacking_time = stacking_time
        self.capacity = capacity


class Depot:
    """Class represents a depot.

    Class represents a depot as an object.

    Attributes:
        key: An integer, indicating depots identification number.
        x: A float, indicating depots x-coordinate.
        y: A float, indicating depots y-coordinate.
    """

    def __init__(self, key, x, y):
        """Inits Depot with identification number, x-coordinate and
        y-coordinate."""
        self.key = key
        self.x = x
        self.y = y


class Result:
    """Class represents a result.

    Class represents a result of each iteration in evaluation as an object.

    Attributes:
        generation: An integer, indicating current generation in evaluation.
        instance: An integer, indicating current instance number in evaluation.
        capacity: An integer, indicating current capacity in evaluation.
        distance: A float, indicating current distance in evaluation.
        vehicle: A Vehicle object, indicating current vehicle in evaluation.
        depot: A Depot object, indicating current depot in evaluation.
        customers: An array of Customer objects, indicating done customers
        in evaluation.
    """

    def __init__(self, generation, instance):
        """Inits Result with generation and instance number, sets other
        attributes to their default value."""
        self.generation = generation
        self.instance = instance
        self.capacity = 0
        self.distance = 0.0
        self.vehicle = None
        self.depot = None
        self.customers = []


class Fitness:
    """Class represents results of evaluated instance.

    Class represents results of evaluated instance as an object.

    Attributes:
        generation: An integer, indicating generation of instance.
        instance: An integer, indicating number of instance.
        value: A float, indicating fitness value of instance.
        phenotype: An array of integers, indicating phenotype of instance.
        best_instance: A boolean, indicating if instance is best
        in its generation.
    """

    def __init__(self, generation, instance, value, phenotype):
        """Inits Fitness with generation, instance number, value and phenotype,
        sets best instance to false."""
        self.generation = generation
        self.instance = instance
        self.value = value
        self.phenotype = phenotype
        self.best_instance = False

