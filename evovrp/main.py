import evovrp.file as file
import evovrp.directory as directory
import evovrp.evaluation as evaluation

from random import randint
from NiaPy.util import Task, OptimizationType
from NiaPy.algorithms.basic.ga import GeneticAlgorithm


def test(file_name, generations, population_size):
    directory.Directory().delete_directories()

    f = file.File('../datasets/' + file_name)
    objects = f.read()

    rand_seed = randint(1000, 10000)
    task = Task(D=len(objects[1]), nGEN=generations, benchmark=evaluation.Evaluation(objects, population_size),
                optType=OptimizationType.MINIMIZATION)
    ga = GeneticAlgorithm(seed=rand_seed, task=task, NP=population_size)

    result, fitness = ga.run()
    print(result, fitness)
    print(evaluation.Evaluation.to_phenotype(result))


if __name__ == '__main__':
    test('example', 5, 5)
