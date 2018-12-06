import numpy as np
from NiaPy.algorithms.basic.ga import GeneticAlgorithm
from NiaPy.util import Task, OptimizationType


class ExampleBenchmark(object):

    def __init__(self):
        # Nastavimo zgornjo in spodnjo mejo za vsako vrednost v polju sol genotipa.
        self.Lower = 0
        self.Upper = 10

    def function(self):
        def evaluate(D, sol): # TODO: spremeni to funkcijo
            """ To se zažene na vsekem primerku v populaciji, da ga oceni.
                D je velikost polja tega enega primerka.
                sol je polje tega primerka
            """

            # 1. korak: najprej pretvori genotip sol v fenotip

            phenotype = ExampleBenchmark.to_phenotype(sol)

            # 2. korak: zdaj pa oceni kvaliteto tega fenotipa

            fitness = 0.0  # To je končna ocena
            for i in range(D):
                fitness = fitness + abs(phenotype[i] - i)

            return fitness

        return evaluate

    def to_phenotype(sol):  # TODO
        # np.argsort(np.argsort(a))
        return np.round(sol)


if __name__ == '__main__':
    random_seed = 1234

    r"""
    D {integer} -- Number of dimensions
    nFES {integer} -- Number of function evaluations
    nGEN {integer} -- Number of generations or iterations
    benchmark {class} or {string} -- Problem to solve
    o {array} -- Array for shifting
    of {function} -- Function applied on shifted input
    M {matrix} -- Matrix for rotating
    fM {function} -- Function applied after rotating
    optF {real} -- Value added to benchmark function return
    """

    # D je število customerjev
    task = Task(D=10, nGEN=100, benchmark=ExampleBenchmark(), optType=OptimizationType.MINIMIZATION)

    # NP - število primerkov v populaciji
    ga = GeneticAlgorithm(seed=random_seed, task=task, NP=100)
    rezultat, fitness = ga.run()
    print(rezultat, fitness)
    print(ExampleBenchmark.to_phenotype(rezultat))
