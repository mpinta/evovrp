import os
import imageio
import evovrp.utils as utils
import evovrp.directory as directory


class Image:
    """Class manages images and gifs.

    Class manages creation and saving of images from graph in
    correct directories. It also manages creation and saving of
    gifs from saved images.

    Attributes:
        generation: An integer, indicating generation for image
        to create.
        instance: An integer, indicating instance for image
        to create.
        image_counter: An integer, indicating image number in
        order to create.
        full_images: An array of strings, indicating path of last
        saved image per instance.
    """

    full_images = []

    def __init__(self, generation, instance):
        """Inits Graph with generation and instance, sets image
        counter to one and calls creation of image, generation
        and instance directories."""
        self.generation = generation
        self.instance = instance
        self.image_counter = 1
        directory.Directory.create_directories(self.generation, self.instance)

    def save(self, plt):
        """Saves an image.

        Saves an image from graph. Directory path is made of image directory
        generation number directory and instance number directory inside of it.
        Image counter increases after the image is saved.

        Args:
            plt: A Matplotlib Pyplot object, indicating current plot.

        Returns:
            Method does not return anything.
        """

        plt.savefig(utils.images_dir + utils.generation_dir + self.generation + utils.instance_dir + self.instance +
                    utils.image_name + str(self.image_counter))
        self.image_counter += 1

    def create_instance_gif(self):
        """Saves an instance gif.

        Gets and saves images of instance building process to a gif
        format. Directory path is made of image directory and generation
        number directory.

        Args:
            Method does not have any arguments.

        Returns:
            Method does not return anything.
        """

        folder_path = utils.images_dir + utils.generation_dir + self.generation + utils.instance_dir + self.instance
        images = []
        file_names = self.get_file_names(folder_path)

        Image.full_images.append(folder_path + '/' + file_names[-1])

        for i in file_names:
            images.append(imageio.imread(folder_path + '/' + i))
        imageio.mimsave(folder_path + '.gif', images, duration=0.5)

    @staticmethod
    def create_best_instances_gif(indexes):
        """Saves best instances gif.

        Gets and saves images of best instances building process to a gif
        format. Directory path is made of image directory.

        Args:
            indexes: An array of integers, indicating indexes of best
            instances among other instances.

        Returns:
            Method does not return anything.
        """

        folder_path = utils.images_dir
        images = []
        file_names = Image.full_images

        for i in range(len(file_names)):
            if i in indexes:
                images.append(imageio.imread(file_names[i]))
        imageio.mimsave(folder_path + utils.best_instances_gif_name + '.gif', images, duration=1)

    def get_file_names(self, folder_path):
        """Gets file names.

        Gets all the file names from given folder path.

        Args:
            folder_path: A string, indicating folder path.

        Returns:
            A method, which returns array of strings, sorted by its
            number in ascending order.
        """

        file_names = []
        for file in os.listdir(folder_path):
            file_names.append(os.fsdecode(file))
        return self.sort_to_order(file_names)

    @staticmethod
    def sort_to_order(file_names):
        """Sorts file names to order.

        Sorts file names to ascending order.

        Args:
            file_names: An array of strings, indicating file names.

        Returns:
            An array of strings, sorted by its number in ascending order.
        """

        file_names.sort(key=lambda i: int(''.join(filter(str.isdigit, i))))
        return file_names
