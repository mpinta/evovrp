import os
import imageio
import evovrp.utils as utils
import evovrp.directory as directory


class Image:
    def __init__(self, generation, instance):
        self.image_counter = 1
        self.generation = generation
        self.instance = instance
        directory.Directory.create_directories(self.generation, self.instance)

    def save(self, plt):
        plt.savefig(utils.images_dir + utils.generation_dir + self.generation + utils.instance_dir + self.instance +
                    utils.image_name + str(self.image_counter))
        self.image_counter += 1

    def create_gif(self):
        folder_path = utils.images_dir + utils.generation_dir + self.generation + utils.instance_dir + self.instance
        images = []
        file_names = self.get_file_names(folder_path)

        for i in file_names:
            images.append(imageio.imread(folder_path + '/' + i))
        imageio.mimsave(folder_path + '.gif', images, duration=0.5)

    @staticmethod
    def get_file_names(folder_path):
        file_names = []
        for file in os.listdir(folder_path):
            file_names.append(os.fsdecode(file))
        return utils.sort_to_order(file_names)
