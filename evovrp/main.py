from random import randint
from NiaPy.util import Task, OptimizationType
from NiaPy.algorithms.basic.ga import GeneticAlgorithm

from evovrp.file import File
from evovrp.graph import Graph
from evovrp.evaluation import Evaluation


if __name__ == '__main__':
    f = File('../datasets/example')
    objects = f.read()

    rand_seed = randint(1000, 10000)
    task = Task(D=len(objects[1]), nGEN=20, benchmark=Evaluation(objects), optType=OptimizationType.MINIMIZATION)
    ga = GeneticAlgorithm(seed=1234, task=task, NP=50)

    result, fitness = ga.run()
    print(result, fitness)
    print(Evaluation.to_phenotype(result))

    g = Graph(objects)
    g.draw()
