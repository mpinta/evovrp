import os
import shutil
import evovrp.utils as utils


class Directory(object):
    @staticmethod
    def create_directories(generation, instance):
        Directory.create_generation_dir(generation)
        Directory.create_instance_dir(generation, instance)

    @staticmethod
    def delete_directories():
        if os.path.exists(utils.images_dir):
            shutil.rmtree(utils.images_dir)

    @staticmethod
    def create_image_dir():
        if not os.path.exists(utils.images_dir):
            os.makedirs(utils.images_dir)

    @staticmethod
    def create_generation_dir(generation):
        if not os.path.exists(utils.images_dir + utils.generation_dir + generation):
            os.makedirs(utils.images_dir + utils.generation_dir + generation)

    @staticmethod
    def create_instance_dir(generation, instance):
        if not os.path.exists(utils.images_dir + utils.generation_dir + generation + utils.instance_dir + instance):
            os.makedirs(utils.images_dir + utils.generation_dir + generation + utils.instance_dir + instance)
