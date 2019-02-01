import evovrp.file as file
import evovrp.directory as directory
import evovrp.evaluation as evaluation

from random import randint
from NiaPy.util import Task, OptimizationType
from NiaPy.algorithms.basic.ga import GeneticAlgorithm


def print_result(best_instance):
    print('Best instance: ')
    print('Generation: ' + str(best_instance.generation))
    print('Instance: ' + str(best_instance.instance))
    print('Fitness: ' + str(round(best_instance.value, 2)))
    print('Phenotype: ' + str(best_instance.phenotype))


def main(file_name, generations, population_size):
    directory.Directory().delete_directories()

    f = file.File('../datasets/' + file_name)
    objects = f.read()

    task = Task(D=len(objects[1]), nGEN=generations, benchmark=evaluation.Evaluation(objects, generations, population_size),
                optType=OptimizationType.MINIMIZATION)
    ga = GeneticAlgorithm(seed=randint(1000, 10000), task=task, NP=population_size)

    result, fitness = ga.run()
    print_result(evaluation.Evaluation.find_overall_best_instance(fitness))


if __name__ == '__main__':
    main('example', 5, 5)
