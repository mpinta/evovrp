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
