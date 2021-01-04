__doc__ = "This module offers functionalities to create & manage directors and files"

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


def create_function_pb(problem_name, params, descriptor_file):
    if isinstance(problem_name, int):
        string_hardcoded = f"def ex{problem_name}({params}): \n\tpass\n\n"
    else:
        string_hardcoded = f"def {problem_name}({params}): \n\tpass\n\n"
    descriptor_file.write(string_hardcoded)


def create_function_subpb(problem_name, sub_problem_name, params, descriptor_file):
    string_hardcoded = f"def ex{problem_name}_{sub_problem_name}({params}): \n\tpass\n\n"
    descriptor_file.write(string_hardcoded)
