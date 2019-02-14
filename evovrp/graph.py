import numpy as np
import evovrp.image as image
import matplotlib.pyplot as plt


class Graph:
    """Class manages drawing of a graph.

    Class manages drawing of a graph; it draws customers, depots,
    connections between them and a legend. It also draws text
    information about generation, instance and fitness value on
    the graph. It is responsible for drawing a graph that shows
    fitness values through generations.

    Attributes:
        customers: An array of Customer objects, indicating all the
        customers.
        depots: An array of Depot objects, indicating all the depots.
    """

    def __init__(self, customers, depots):
        """Inits Graph with customers and depots."""
        self.customers = customers
        self.depots = depots

    @staticmethod
    def draw_fitness_graph(fitness_list):
        """Draws fitness values graph and saves image.

        Draws graph that shows fitness values through
        generations and then calls saving of it.

        Args:
            fitness_list: An array of Fitness objects, indicating
            final results of instances in evaluation.

        Returns:
            Method does not return anything.
        """

        generations = fitness_list[-1].generation
        instances = fitness_list[-1].instance

        data = Graph.get_fitness_data(fitness_list)
        values = [i[0] for i in data]
        titles = [i[1] for i in data]

        plt.figure(figsize=(20, 15), dpi=120)
        plt.rcParams.update({'font.size': 16})

        counter = 0
        for i in range(generations):
            color = np.random.random(3)
            plt.bar(titles[counter:(counter + instances)], values[counter:(counter + instances)],
                    .8, alpha=0.5, label='Generation ' + str(i + 1), color=color)
            counter += instances

        plt.xticks([])
        plt.ylabel('Fitness')
        plt.xlabel('Instances')
        Graph.draw_legend()
        plt.suptitle('Fitness values through generations', fontsize=22)

        image.Image.save_fitness_image(plt)
        plt.close()

    @staticmethod
    def draw_legend():
        """Draws legend.

        Draws a legend, which is made of a color circle and
        belonging label.

        Args:
            Method does not have any arguments.

        Returns:
            Method does not return anything.
        """

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)

    @staticmethod
    def draw_text(fitness):
        """Draws text.

        Draws text with information about generation, instance and
        fitness value of graph.

        Args:
            fitness: A Fitness object, indicating final result of instance
            in evaluation.

        Returns:
            Method does not return anything.
        """

        plt.suptitle('Generation: ' + str(fitness.generation) + ', Instance: ' + str(fitness.instance), fontsize=16)
        plt.title('Fitness: ' + str(round(fitness.value, 2)), fontsize=14)

    def draw(self, results, fitness):
        """Draws a graph.

        Main method, responsible for drawing a graph. It creates new figure and
        draws customers and depots. After that, it draws a legend and text with
        information about generation, instance and fitness value of graph.
        Lastly it creates connections between customers and depots and closes
        the figure.

        Args:
            results: An array of Result objects, indicating results from
            evaluation.
            fitness: A Fitness object, indicating final result of instance
            in evaluation.

        Returns:
            Method does not return anything.
        """

        plt.figure(figsize=(10, 10), dpi=90)
        self.draw_depots()
        self.draw_customers()
        self.draw_legend()
        self.draw_text(fitness)
        self.draw_connections(results, fitness)
        plt.close()

    def draw_depots(self):
        """Draws depots.

        Draws each depot on a graph in form of a point. Position of a
        point is determined from depots x and y coordinates.

        Args:
            Method does not have any arguments.

        Returns:
            Method does not return anything.
        """

        coordinates = self.get_coordinates(self.depots)
        sorted(coordinates)
        for index, i in enumerate(coordinates):
            if index == 0:
                plt.scatter(i[0], i[1], alpha=0.8, c='C0', edgecolors='C0', s=30, label='Depot', zorder=2)
            plt.scatter(i[0], i[1], alpha=0.8, c='C0', edgecolors='C0', s=30, zorder=2)

    def draw_customers(self):
        """Draws customers.

        Draws each customer on a graph in form of a point. Position of a
        point is determined from customers x and y coordinates.

        Args:
            Method does not have any arguments.

        Returns:
            Method does not return anything.
        """

        coordinates = self.get_coordinates(self.customers)
        sorted(coordinates)
        for index, i in enumerate(coordinates):
            if index == 0:
                plt.scatter(i[0], i[1], alpha=0.8, c='C1', edgecolors='C1', s=30, label='Customer', zorder=2)
            plt.scatter(i[0], i[1], alpha=0.8, c='C1', edgecolors='C1', s=30, zorder=2)

    def draw_connections(self, results, fitness):
        """Draws connections and saves images.

        Draws connections between already drawn customers and depots on
        a graph and calls saving its each intermediate state to an image.
        Connections are obtained from array of results.

        Args:
            results: An array of Result objects, indicating results from
            evaluation.
            fitness: A Fitness object, indicating final result of instance
            in evaluation.

        Returns:
            Method does not return anything.
        """

        img = image.Image(str(fitness.generation), str(fitness.instance))
        img.save(plt)

        for i in results:
            color = np.random.random(3)
            coordinates = self.get_connection_coordinates(i)

            for index, j in enumerate(coordinates):
                if index == len(coordinates)-1:
                    break
                plt.plot([j[0], coordinates[index + 1][0]], [j[1], coordinates[index + 1][1]],
                         alpha=0.5, c=color, zorder=1)
                img.save(plt)
        img.create_instance_gif()

    @staticmethod
    def get_coordinates(data):
        """Gets coordinates.

        Gets x and y coordinates from multiple objects and stores them
        separately to an array, consisting of arrays of two float values.

        Args:
            data: An array of objects, indicating customers or depots.

        Returns:
            An array consisting of arrays of two float values, x-coordinate
            and y-coordinate.
        """

        coordinates = []
        for i in data:
            coordinates.append([i.x, i.y])
        return coordinates

    @staticmethod
    def get_fitness_data(fitness_list):
        """Gets fitness data.

        Gets fitness value, generation and instance from
        fitness results.

        Args:
            fitness_list: An array of Fitness objects, indicating
            final results of instances in evaluation.

        Returns:
            An array consisting of arrays of float and string values.
        """

        coordinates = []
        for i in fitness_list:
            coordinates.append([i.value, str(i.generation) + '.' + str(i.instance)])
        return coordinates

    def get_connection_coordinates(self, results):
        """Gets connection coordinates.

        Gets x and y coordinates of customers and depots from results.

        Args:
            results: An array of Result objects, indicating results from
            evaluation.

        Returns:
            An array consisting of arrays of two float values, x-coordinate
            and y-coordinate.
        """

        coordinates = self.get_coordinates(results.customers)
        coordinates.insert(0, [results.depot.x, results.depot.y])
        coordinates.append([results.depot.x, results.depot.y])
        return coordinates
