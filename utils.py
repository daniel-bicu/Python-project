__doc__="This module offers functionalities to create & manage directors and files"

import os


def create_director(path_to_create_dirs, name):
    dir_name = os.path.join(path_to_create_dirs, name)

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print(f'Director {dir_name} created successfully.')
    # else:
    #     print(f'The dir.{dir_name} already exists.')
    #     exit(-1)
    return dir_name