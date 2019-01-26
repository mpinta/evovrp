from random import randint
from NiaPy.util import Task, OptimizationType
from NiaPy.algorithms.basic.ga import GeneticAlgorithm

from evovrp.file import File
from evovrp.evaluation import Evaluation


if __name__ == '__main__':
    f = File('../datasets/example')
    objects = f.read()

    rand_seed = randint(1000, 10000)
    population_size = 5
    generations = 5

    task = Task(D=len(objects[1]), nGEN=generations, benchmark=Evaluation(objects, population_size),
                optType=OptimizationType.MINIMIZATION)
    ga = GeneticAlgorithm(seed=rand_seed, task=task, NP=population_size)

    result, fitness = ga.run()
    print(result, fitness)
    print(Evaluation.to_phenotype(result))
