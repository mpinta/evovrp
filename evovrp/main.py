import file
import method
import directory
import evaluation

from random import randint
from NiaPy.util import Task, OptimizationType
from NiaPy.algorithms.basic.ga import GeneticAlgorithm


def print_result(best_instance):
    """Prints a result.

    Prints overall best instance information to output.

    Args:
        best_instance: A Fitness object, indicating overall best instance.

    Returns:
        Method does not return anything.
    """

    print('Best instance: ')
    print('Generation: ' + str(best_instance.generation))
    print('Instance: ' + str(best_instance.instance))
    print('Fitness: ' + str(round(best_instance.value, 2)))
    print('Phenotype: ' + str(best_instance.phenotype))


def main(file_name, algorithm, iterations, population_size, phenotype_coding):
    """Main function.

    Function is used for connecting the main parts of a project. Firstly, it
    calls deletion of before created image directories. Then it calls file
    reading method and so gets parsed objects from it. It creates new task
    with given information and runs it using selected evolutionary algorithm.
    Lastly, it calls printing information of overall best instance to output.

    Args:
        file_name: A string, indicating name of a file, which will be read.
        algorithm: A NiaPy algorithm, indicating evolutionary algorithm
        that will be used.
        iterations: An integer, indicating number of repetitions.
        population_size: An integer, indicating number of instances that will
        be created inside one generation.
        phenotype_coding: An enum type, indicating which genotype-to-phenotype
        coding will be used in evaluation.

    Returns:
        Method does not return anything.
    """

    directory.Directory().delete_directories()
    objects = file.File.read('../datasets/' + file_name)

    task = Task(D=len(objects[1]), nFES=iterations, benchmark=evaluation.Evaluation(
        objects, iterations, population_size, phenotype_coding), optType=OptimizationType.MINIMIZATION)
    alg = algorithm(seed=randint(1000, 10000), task=task, NP=population_size)

    result, fitness = alg.run()
    print_result(evaluation.Evaluation.find_overall_best_instance(fitness))


if __name__ == '__main__':
    main('C-mdvrptw/pr00', GeneticAlgorithm, 25, 5, method.Method.FIRST)

