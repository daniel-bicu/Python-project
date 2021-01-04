__doc__ = "This module offers functionalities to create & manage directors and files"

import os


def create_director(path_to_create_dirs, name):
    """
    Create a director based on path name and the desired name of a file.
    :param path_to_create_dirs: absolute path to create the dir
    :param name: name of the file in that dir
    :return: director name
    """
    dir_name = os.path.join(path_to_create_dirs, name)

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print(f'Director {dir_name} created successfully.')
    # else:
    #     print(f'The dir.{dir_name} already exists.')
    #     exit(-1)
    return dir_name


def create_function_pb(problem_name, params, descriptor_file):
    """
    Create & write in a file a simple function based on params &  problem name
    :param problem_name: the name of the function
    :param params: list of params of the function
    :param descriptor_file: gives access to the file we want to write
    :return:
    """
    if isinstance(problem_name, int):
        string_hardcoded = f"def ex{problem_name}({params}): \n\tpass\n\n"
    else:
        string_hardcoded = f"def {problem_name}({params}): \n\tpass\n\n"
    descriptor_file.write(string_hardcoded)


def create_function_subpb(problem_name, sub_problem_name, params, descriptor_file):
    """
    Create & write in a file a function of a subproblem.
    :param problem_name: problem name (main name of the function)
    :param sub_problem_name: the name of the subproblem (second name)
    :param params: list of parans of the function
    :param descriptor_file: gives access to the file we want to write
    :return:
    """
    string_hardcoded = f"def ex{problem_name}_{sub_problem_name}({params}): \n\tpass\n\n"
    descriptor_file.write(string_hardcoded)
