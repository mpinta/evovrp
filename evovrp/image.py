import os


class Image:
    def save(self, plt, population, generation, index):
        self.create_generation_directory(str(generation))
        self.create_population_directory(str(population), str(generation))
        plt.savefig('../images/generation' + str(generation) + '/population' + str(population) + '/image' + str(index))

    @staticmethod
    def create_generation_directory(generation):
        if not os.path.exists('../images/generation' + generation):
            os.makedirs('../images/generation' + generation)

    @staticmethod
    def create_population_directory(population, generation):
        if not os.path.exists('../images/generation' + generation + '/population' + population):
            os.makedirs('../images/generation' + generation + '/population' + population)
