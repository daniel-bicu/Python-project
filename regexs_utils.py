
__doc__ = "A module which offer precompiled regexp to use"

# --- REGEXP ----
import re

url_regex = re.compile('^/site/fiipythonprogramming/laboratories/lab-')
labs_regex = re.compile(r'^Lab|lab')
pattern_function_1 = re.compile(r'([a-z]+[0-9]*)(_[a-z0-9]+)*(\([^\)]*\)){1}')
pattern_function_2 = re.compile(r'([a-z]+[0-9]*)(_[a-z0-9]+)+([\s]+function){1}')
pattern_function_3 = re.compile(r'([\s]+function[\s]+called[\s]+)([a-z]+[_a-z0-9]*)')
start_problem_pattern = re.compile(r'[\s]*(\d{1,2}[\.|\)]{1}).')
start_sub_problem_pattern = re.compile(r'[\s]*([a-z]\)){1}')

# ---  ----
