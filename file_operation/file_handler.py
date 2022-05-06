import pickle
from logging_details.custom_logging import ApplicationLogging


class FileHandler:
    def __init__(self):
        pass

    def loadModel(self, file):
        """
        It loads the given pickle file
        :param file: file name : Which we have to load
        :return: return the loaded file
        """
        try:
            with open(file, 'rb') as f:
                return pickle.loads(f.read())

        except Exception as e:
            print(str(e))