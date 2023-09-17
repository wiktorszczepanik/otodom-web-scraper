import web_od.constans as const
from os import listdir
from os.path import isfile, join


class Filters:
    def __init__(self, directory=const.FILTERS_PATH) -> None:
        self.directory = directory
        self.filters_lst = []

    def collect(self):
        # collect json filter files form directory
        for file in listdir(self.directory):
            is_file, is_json = False, False
            path_and_file = join(self.directory, file)
            if isfile(path_and_file) == True:
                is_file = True
            file_extension = str(file.split(".")[-1])
            if file_extension == "json":
                is_json = True
            if is_file == True and is_json == True:
                self.filters_lst.append(path_and_file)
