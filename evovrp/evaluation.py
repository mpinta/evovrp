import operator
import numpy as np
import evovrp.graph as graph
import evovrp.image as image
import evovrp.method as method
import evovrp.classes as classes


class Evaluation(object):
    """Class evaluates instances.

    Class evaluates each instance in every generation. Firstly, it changes
    genotype given from selected evolutionary algorithm to phenotype, that
    is suitable for solving vehicle routing problem. The main evaluation
    method then attempts to solve the problem with a converted phenotype
    and obtains a result or so-called "fitness". The method calls the graph
    drawing function, which saves the drawn image and at the end creates a
    gif. Gif is also created from all the best instances from each generation.
    Lastly, it finds overall best estimated instance and returns it.

    Attributes:
        objects: An array of three different arrays, each with different type,
        storing Vehicle, Customer and Depot objects, indicating data.
        iterations: An integer, indicating number of repetitions.
        population_size: An integer, indicating number of instances that will
        be created inside one generation.
        phenotype_coding: An enum type, indicating which genotype-to-phenotype
        coding will be used in evaluation.
        fitness_list: An array of Fitness objects, indicating final results of
        instances in evaluation.
    """

    fitness_list = []

    def __init__(self, objects, iterations, population_size, phenotype_coding):
        """Inits Evaluation with objects, generations, population size and
        phenotype coding, sets lower and upper values to zero and ten, sets
        penalty value, instance counter and generation counter."""
        self.Lower = 0
        self.Upper = 10
        self.penalty = 20
        self.vehicles = objects[0]
        self.customers = objects[1]
        self.depots = objects[2]
        self.instance_counter = 0
        self.generation_counter = 1
        self.population_size = population_size
        self.generations = iterations / population_size
        self.phenotype_coding = phenotype_coding

    def function(self):
        """Calls the evaluate method.

        Calls the evaluate method and makes it private.

        Args:
            Method does not have any arguments.

        Returns:
            A method which returns an integer, indicating fitness value.
        """

        def evaluate(d, genotype):
            """Evaluates instances.

            The method is the main function for evaluating instances. The genotype of
            instance converts to a phenotype version, which is suitable for solving the
            vehicle routing problem. Then it selects the current vehicle and depot and
            the previous, current and next customer based on the numbers in the phenotype
            and calculates the distance between them. If the distance or capacity is too large
            for the current vehicle, the vehicle and depot change. Lastly it finds overall best
            estimated instance and returns it.

            Args:
                d: An integer, indicating number of customers.
                genotype: An array of float values, indicating genotype of an instance.

            Returns:
                A float, indicating fitness value of an instance.
            """

            self.set_instance_counter()
            self.set_generation_counter()

            results = []
            customers_counter = 0
            vehicle_depot_counter = 0
            vehicle_depot_changed = False
            phenotype = self.to_phenotype(genotype)
            curr_result = classes.Result(self.generation_counter, self.instance_counter)
            g = graph.Graph(self.customers, self.depots)

            for i in range(d):
                customers_counter += 1
                curr_result = self.set_vehicle_depot(curr_result, vehicle_depot_counter)

                prev_customer = self.find_previous_customer(i, vehicle_depot_changed, phenotype)
                curr_customer = self.find_customer(phenotype[i])
                next_customer = self.find_next_customer(i, phenotype)

                curr_result = self.get_result(curr_result, prev_customer, curr_customer)
                curr_result = self.add_customer_to_result(curr_result, curr_customer)
                vehicle_depot_changed = False

                if self.phenotype_coding == method.Method.SECOND and \
                        curr_result.depot.customers_num == customers_counter:
                    vehicle_depot_changed = True

                if not self.check_next_customer(curr_result, curr_customer, next_customer) or vehicle_depot_changed:
                    curr_result = self.get_last_distance(curr_result, curr_customer)

                    if self.check_for_penalty(curr_result):
                        self.add_penalty(curr_result)
                    results.append(curr_result)

                    if self.phenotype_coding == method.Method.FIRST or \
                            (self.phenotype_coding == method.Method.SECOND and
                             curr_result.depot.customers_num == customers_counter):
                        vehicle_depot_changed = True
                        vehicle_depot_counter = self.set_vehicle_depot_counter(vehicle_depot_counter)
                        customers_counter = 0
                    curr_result = classes.Result(self.generation_counter, self.instance_counter)

            fitness = self.create_fitness(results, phenotype)
            g.draw(results, fitness)

            if self.instance_counter == self.population_size:
                self.find_best_instance()
                if self.generation_counter == self.generations:
                    self.create_best_instances_gif()
                    self.create_fitness_image()

            return fitness.value
        return evaluate

    def set_instance_counter(self):
        """Sets the instance counter.

        Sets and increments the instance counter for one value.

        Args:
            Method does not have any arguments.

        Returns:
            Method does not return anything.
        """

        self.instance_counter += 1

    def set_generation_counter(self):
        """Sets the generation counter.

        Sets and increments the generation counter for one value
        and sets the instance counter to one if the instance
        counter value is bigger than the population size.

        Args:
            Method does not have any arguments.

        Returns:
            Method does not return anything.
        """

        if self.instance_counter > self.population_size:
            self.generation_counter += 1
            self.instance_counter = 1

    def set_vehicle_depot_counter(self, vehicle_depot_counter):
        """Sets the vehicle-depot counter.

        Sets and increases the vehicle-depot counter for one value.
        If the vehicle-depot counter value plus one is bigger than
        vehicles length, returns zero value.

        Args:
            vehicle_depot_counter: An integer, indicating counter for
            vehicle and depot.

        Returns:
            An integer, indicating vehicle-depot counter value.
        """

        if (vehicle_depot_counter + 1) >= len(self.vehicles):
            return 0
        return vehicle_depot_counter + 1

    def set_vehicle_depot(self, curr_result, vehicle_depot_counter):
        """Sets vehicle and depot.

        Sets vehicle and depot objects based on the vehicle-depot
        counter.

        Args:
            curr_result: A Result object, indicating result from
            evaluation.
            vehicle_depot_counter: An integer, indicating counter for
            vehicle and depot.

        Returns:
            A Result object with set vehicle and depot objects,
            indicating result from evaluation.
        """

        curr_result.vehicle = self.vehicles[vehicle_depot_counter]
        curr_result.depot = self.depots[vehicle_depot_counter]
        return curr_result

    @staticmethod
    def find_overall_best_instance(fitness):
        """Finds overall best instance.

        Searches and finds overall best estimated instance.

        Args:
            fitness: A float, indicating fitness value of instance.

        Returns:
            A Fitness object, indicating overall best instance.
        """

        for i in Evaluation.fitness_list:
            if i.value == fitness:
                return i

    def find_best_instance(self):
        """Finds best instances.

        Searches and finds best estimated instance from each
        generation.

        Args:
            Method does not have any arguments.

        Returns:
            Method does not return anything.
        """

        instances = [i for i in Evaluation.fitness_list if i.generation == self.generation_counter]
        best_instance = min(instances, key=operator.attrgetter('value'))
        best_instance.best_instance = True

    def find_customer(self, key):
        """Finds a customer.

        Finds a particular customer based on given key value.

        Args:
            key: An integer, indicating customers identification number.

        Returns:
            A Customer object, indicating the particular customer.
        """

        for i in self.customers:
            if i.key == key:
                return i

    def find_previous_customer(self, i, vehicle_depot_changed, phenotype):
        """Finds the previous customer.

        Finds particular previous customer based on given key value. If i
        value is zero or vehicle and depot objects were changed, it
        returns negative one value.

        Args:
            i: An integer, indicating loop number in evaluate method.
            vehicle_depot_changed: A boolean, indicating if vehicle and
            depot objects where changed.
            phenotype: An array of float values, indicating phenotype of
            instance.

        Returns:
            A method which returns Customer object, indicating
            the particular customer.
        """

        if i == 0 or vehicle_depot_changed is True:
            return -1
        return self.find_customer(phenotype[i - 1])

    def find_next_customer(self, i, phenotype):
        """Finds the next customer.

        Finds particular next customer based on given key value. If i
        value plus one value is bigger then customers length, returns
        negative one value.

        Args:
            i: An integer, indicating loop number in evaluate method.
            phenotype: An array of float values, indicating phenotype of
            instance.

        Returns:
            A method which returns Customer object, indicating
            the particular customer.
        """

        if (i + 1) >= len(self.customers):
            return -1
        return self.find_customer(phenotype[i + 1])

    @staticmethod
    def check_for_penalty(curr_result):
        """Checks for a penalty.

        Checks if current results distance is bigger than vehicles
        maximum duration value.

        Args:
            curr_result: A Result object, indicating result from
            evaluation.

        Returns:
            A boolean value, true or false.
        """

        if curr_result.distance > curr_result.vehicle.max_duration:
            return True
        return False

    def check_next_customer(self, curr_result, curr_customer, next_customer):
        """Checks the next customer.

        Checks the further capacity and distance of vehicle and
        returns if current vehicle can pass to the next customer.

        Args:
            curr_result: A Result object, indicating result from
            evaluation.
            curr_customer: A Customer object, indicating current
            customer in evaluation.
            next_customer: A Customer object, indicating next
            customer in evaluation.

        Returns:
            A boolean value, true or false.
        """

        if next_customer == -1:
            return False

        next_capacity = curr_result.capacity + next_customer.capacity
        next_distance = curr_result.distance + self.get_distance(curr_result.depot, curr_customer, next_customer)

        if next_capacity > curr_result.vehicle.max_capacity or next_distance > curr_result.vehicle.max_duration:
            return False
        return True

    @staticmethod
    def create_best_instances_gif():
        """Calls creation of best instances gif.

        Gets an array of integers, indicating indexes of best
        instances among other and calls creation of best instances
        gif creation.

        Args:
            Method does not have any arguments.

        Returns:
            Method does not return anything.
        """

        indexes = [i for i in range(len(Evaluation.fitness_list)) if Evaluation.fitness_list[i].best_instance]
        image.Image.create_best_instances_gif(indexes)

    @staticmethod
    def create_fitness_image():
        """Calls creation of fitness image.

        Calls creation of image that shows fitness values
        through generations.

        Args:
            Method does not have any arguments.

        Returns:
            Method does not return anything.
        """

        graph.Graph.draw_fitness_graph(Evaluation.fitness_list)

    def create_fitness(self, results, phenotype):
        """Creates a new fitness.

        Creates a new Fitness object and saves current generation,
        instance number, fitness value and phenotype to it.

        Args:
            results: An array of Result objects, indicating results from
            evaluation.
            phenotype: An array of float values, indicating phenotype of
            instance.

        Returns:
            A Fitness object, indicating final result of instance in
            evaluation.
        """

        fitness = classes.Fitness(self.generation_counter, self.instance_counter,
                                  self.get_fitness(results), phenotype)
        Evaluation.fitness_list.append(fitness)
        return fitness

    @staticmethod
    def get_distance(depot, customer_one, customer_two):
        """Gets a distance between two points.

        Calculates and gets a distance between two points, which can be
        customer to customer, depot to customer or customer to depot.

        Args:
            depot: A Depot object, indicating current depot in evaluation.
            customer_one: A Customer object, indicating fist customer.
            customer_two: A Customer object, indicating second customer.

        Returns:
            A float, indicating distance between two points.
        """

        if customer_one == -1:
            x1 = depot.x
            y1 = depot.y
        else:
            x1 = customer_one.x
            y1 = customer_one.y

        if customer_two == -1:
            x2 = depot.x
            y2 = depot.y
        else:
            x2 = customer_two.x
            y2 = customer_two.y

        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def get_fitness(results):
        """Gets the current fitness.

        Calculates and gets the fitness value of current evaluated instance.

        Args:
            results: An array of Result objects, indicating results from
            evaluation.

        Returns:
            A float, indicating fitness value of an instance.
        """

        fitness = 0.0
        for i in results:
            fitness += i.distance
        return fitness

    def get_result(self, curr_result, prev_customer, curr_customer):
        """Gets the current result.

        Gets the current capacity value and distance and stores them
        into current result.

        Args:
            curr_result: A Result object, indicating result from
            evaluation.
            prev_customer: A Customer object, indicating previous
            customer in evaluation.
            curr_customer: A Customer object, indicating current
            customer in evaluation.

        Returns:
            A Result object, indicating result from evaluation.
        """

        curr_result.capacity += curr_customer.capacity
        curr_result.distance += self.get_distance(curr_result.depot, prev_customer, curr_customer)
        return curr_result

    def get_last_distance(self, curr_result, curr_customer):
        """Gets the last distance.

        Gets the distance from current customer to current depot or
        so-called "last distance".

        Args:
            curr_result: A Result object, indicating result from
            evaluation.
            curr_customer: A Customer object, indicating current
            customer in evaluation.

        Returns:
            A Result object, indicating result from evaluation.
        """

        curr_result.distance += self.get_distance(curr_result.depot, curr_customer, -1)
        return curr_result

    @staticmethod
    def add_customer_to_result(curr_result, curr_customer):
        """Adds a customer to the result.

        Adds the current customer to Result object.

        Args:
            curr_result: A Result object, indicating result from
            evaluation.
            curr_customer: A Customer object, indicating current
            customer in evaluation.

        Returns:
            A Result object, indicating result from evaluation.
        """

        curr_result.customers.append(curr_customer)
        return curr_result

    def add_penalty(self, curr_result):
        """Adds a penalty to result.

        Adds a penalty to distance of current result.

        Args:
            curr_result: A Result object, indicating result from
            evaluation.

        Returns:
            A Result object, indicating result from evaluation.
        """

        curr_result.distance += self.penalty
        return curr_result

    @staticmethod
    def to_first_phenotype(genotype):
        """Converts genotype to phenotype with first method.

        Converts genotype of instance to phenotype with first method,
        which switch each genotype gene value with its ascending order
        index.

        Args:
            genotype: An array of float values, indicating genotype
            of an instance.

        Returns:
            An array of integer values, indicating phenotype.
        """

        return (np.argsort(np.argsort(genotype)) + 1).tolist()

    def to_second_phenotype(self, genotype):
        """Converts genotype to phenotype with second method.

        Converts genotype of instance to phenotype with second method,
        which first divides genotype in groups, each for one customer.
        Then it switches each genotype gene value with its ascending
        order index.

        Args:
            genotype: An array of float values, indicating genotype
            of an instance.

        Returns:
            An array of integer values, indicating phenotype.
        """

        divider = 10 / len(self.depots)

        scale = [0]
        for i in range(len(self.depots)):
            setattr(self.depots[i], 'phenotype', [])
            scale.append(scale[-1] + divider)

        ordered = Evaluation.to_first_phenotype(genotype)

        for i in range(len(genotype)):
            for j in range(len(scale)):
                if genotype[i] == scale[-1]:
                    self.depots[-1].phenotype.append(ordered[i])
                    break

                if scale[j] <= genotype[i] < scale[j + 1]:
                    self.depots[j].phenotype.append(ordered[i])
                    break

        phenotype = []
        for i in self.depots:
            setattr(i, 'customers_num', len(i.phenotype))
            phenotype += i.phenotype
            delattr(i, 'phenotype')

        return phenotype

    def to_phenotype(self, genotype):
        """Calls the conversion to phenotype.

        Calls the specific conversion from genotype to phenotype based
        on phenotype coding value.

        Args:
            genotype: An array of float values, indicating genotype
            of an instance.

        Returns:
            A method which returns an array of integer values,
            indicating phenotype.
        """

        if self.phenotype_coding == method.Method.FIRST:
            return self.to_first_phenotype(genotype)
        elif self.phenotype_coding == method.Method.SECOND:
            return self.to_second_phenotype(genotype)
