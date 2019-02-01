class Vehicle:
    def __init__(self, max_duration, max_capacity):
        self.max_duration = max_duration
        self.max_capacity = max_capacity


class Customer:
    def __init__(self, key, x, y, stacking_time, capacity):
        self.key = key
        self.x = x
        self.y = y
        self.stacking_time = stacking_time
        self.capacity = capacity


class Depot:
    def __init__(self, key, x, y):
        self.key = key
        self.x = x
        self.y = y


class Result:
    def __init__(self, generation, instance):
        self.capacity = 0
        self.distance = 0.0
        self.vehicle = None
        self.depot = None
        self.customers = []
        self.generation = generation
        self.instance = instance


class Fitness:
    def __init__(self, generation, instance, value, phenotype):
        self.generation = generation
        self.instance = instance
        self.value = value
        self.phenotype = phenotype
        self.best_instance = False
