import os
import shutil
import evovrp.utils as utils


class Directory(object):
    """Class manages directories of images.

    Class creates and deletes multiple directories.

    Attributes:
        Class does not have any attributes.
    """

    @staticmethod
    def create_directories(generation, instance):
        """Calls creation of image, generation and instance directories.

        Calls three methods, which create three different directories:
        image directory, generation directory and instance directory.

        Args:
            generation: An integer, indicating generation for directory
            to create.
            instance: An integer, indicating instance for directory
            to create.

        Returns:
            Method does not return anything.
        """

        Directory.create_image_dir()
        Directory.create_generation_dir(generation)
        Directory.create_instance_dir(generation, instance)

    @staticmethod
    def delete_directories():
        """Deletes image, generation and instance directories.

        Deletes image directory including generation directories, instance
        directories and all the possible content inside them, if
        directory exists.

        Args:
            Method does not have any arguments.

        Returns:
            Method does not return anything.
        """

        if os.path.exists(utils.images_dir):
            shutil.rmtree(utils.images_dir)

    @staticmethod
    def create_image_dir():
        """Creates image directory.

        Creates image directory, which is root directory of all other
        directories, if directory does not already exists.

        Args:
            Method does not have any arguments.

        Returns:
            Method does not return anything.
        """

        if not os.path.exists(utils.images_dir):
            os.makedirs(utils.images_dir)

    @staticmethod
    def create_generation_dir(generation):
        """Creates generation directory.

        Creates directory with generation number added to its name inside
        image directory, if directory does not already exists.

        Args:
            generation: An integer, indicating generation number for
            directory to create.

        Returns:
            Method does not return anything.
        """

        if not os.path.exists(utils.images_dir + utils.generation_dir + generation):
            os.makedirs(utils.images_dir + utils.generation_dir + generation)

    @staticmethod
    def create_instance_dir(generation, instance):
        """Creates instance directory.

        Creates directory with instance number added to its name inside
        image directory and correct generation directory, if directory
        does not already exists.

        Args:
            generation: An integer, indicating generation number of instance.
            instance: An integer, indicating instance number for directory
            to create.

        Returns:
            Method does not return anything.
        """

        if not os.path.exists(utils.images_dir + utils.generation_dir + generation + utils.instance_dir + instance):
            os.makedirs(utils.images_dir + utils.generation_dir + generation + utils.instance_dir + instance)
