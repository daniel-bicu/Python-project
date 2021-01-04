__doc__ = "A module which give details about functions: name finding, retrieve & give the correct nr params of a function"

import regexs_utils as regex
import re

stop_words = ['len', 'max', 'min', 'str', 'ord', 'chr', 'content']
opened_paranths = ['(', '[', '{']
closed_paranths = [')', ']', '}']


def search_problems(text):
    problem = ''
    start_of_pb = 1
    problems = []
    for paragraph in text:
        if regex.start_problem_pattern.match(paragraph.text):
            if start_of_pb == 1:
                problem += paragraph.text
                # problem += '\n'
            else:
                problems.append(problem)
                problem = paragraph.text
            start_of_pb = 0
        else:
            problem += paragraph.text
            problem += '\n'

    problems.append(problem)

    return problems


def search_sub_problems(paragraphs_pb, problem):
    sb_pbs = []
    sub_problem_points = []
    if paragraphs_pb and regex.start_sub_problem_pattern.match(problem[2:]):
        sub_problem_points = problem[2:].split('\n')
        # print(sub_problems)
        start_sub_pb = True

        sub_pb_text = ''
        for sub_problem in sub_problem_points:
            if regex.start_sub_problem_pattern.match(sub_problem):
                if start_sub_pb:
                    sub_pb_text += sub_problem
                else:
                    sb_pbs.append(sub_pb_text)
                    sub_pb_text = sub_problem

                start_sub_pb = False
            else:
                sub_pb_text += sub_problem
        sb_pbs.append(sub_pb_text)
    return sb_pbs


def get_list_of_params(nr_params):
    list_of_params = []
    if nr_params >= 4:
        return "*parametrii"

    for param in range(0, nr_params):
        parametru = f"parametru{param + 1}"
        list_of_params.append(parametru)

    list_of_params = ",".join(list_of_params)
    return list_of_params


def count_params(text):
    stack = []
    nr_params = 1

    for caracter in text:
        if caracter == ',' and len(stack) == 0:
            nr_params += 1
        if caracter in opened_paranths:
            stack.append(caracter)
        if caracter in closed_paranths and len(stack) != 0:
            stack.pop()
        if caracter == ')' and len(stack) == 0:
            return nr_params


def get_function_details(text):
    pattern3 = False
    detected_name = regex.pattern_function_3.search(text)

    name = ''
    nr_params = 1

    if detected_name:
        pattern3 = True

    if detected_name is None:
        detected_name = regex.pattern_function_1.search(text)
        if detected_name:
            poz_start_function = text.index(detected_name.group())
            poz1 = text.find('(', poz_start_function)
            nr_params = count_params(text[poz1 + 1:])

    if detected_name is None:
        detected_name = regex.pattern_function_2.search(text)

    if detected_name and pattern3 is False:
        name = re.split(r'\s|\s\(|\(|[\s]function', detected_name.group(0))[0]
    else:
        if detected_name and pattern3:
            name = detected_name.group(2)

    # if detected_name:
    #     print(detected_name.group())
    return (name, nr_params) if name != '' and name not in stop_words else (-1, 1)
