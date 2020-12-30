# ---- IMPORTS ----

import os
import re
import sys

import requests
from bs4 import BeautifulSoup as bs

import regexs_utils as regex
import utils

# List of stop words - they aren't allowed as a function name
stop_words = ['len', 'max', 'min', 'str', 'ord', 'chr']


# ---- ----

def detect_name_function(text):
    pattern3 = False
    detected_name = regex.pattern_function_3.search(text)

    name = ''

    if detected_name:
        pattern3 = True

    if detected_name is None:
        detected_name = regex.pattern_function_1.search(text)

    if detected_name is None:
        detected_name = regex.pattern_function_2.search(text)

    if detected_name and pattern3 is False:
        name = re.split('\s|\s\(|\(|[\s]function', detected_name.group(0))[0]
    else:
        if detected_name and pattern3:
            name = detected_name.group(2)

    return name if name != '' and name not in stop_words else -1


paragraphs_pb = False

if __name__ == '__main__':

    path_to_create_dirs = sys.argv[1]
    # print(path_to_create_dirs)

    r = requests.get("https://sites.google.com/site/fiipythonprogramming/administrative?authuser=0")
    bs_page_obj = bs(r.content, 'html.parser')

    # print(bs_page_obj.prettify())

    all_links = bs_page_obj.findAll('a')

    link_labs = [link['href'] for link in all_links if regex.labs_regex.match(str(link.text))][0]

    # print(link_labs)

    lab_req = requests.get(f"https://sites.google.com{link_labs}")
    labs_page = bs(lab_req.content, 'html.parser')

    container_labs = labs_page.find('div', attrs={'class': "tyJCtd mGzaTb baZpAe"})
    links_to_labs = container_labs.findAll('a')

    for link_lab in links_to_labs:
        if regex.url_regex.match(link_lab['href']):
            # print(url['href'])
            name_of_dir = link_lab.text
            target_dir = utils.create_director(path_to_create_dirs, name_of_dir)

            go_to_link_lab = requests.get(f"https://sites.google.com{link_lab['href']}")
            laborator = bs(go_to_link_lab.content, 'html.parser')

            list_of_problems = laborator.find('ol')

            if list_of_problems is None:
                list_of_problems = laborator.findAll('p')
                paragraphs_pb = True
            else:
                paragraphs_pb = False

            try:
                with open(os.path.join(target_dir, f'lab{target_dir[-1]}.py'), "w") as file_lab:
                    if list_of_problems:
                        if paragraphs_pb is False:
                            list_of_problems = list_of_problems.findAll('li')
                        else:
                            problem = ''
                            start_of_pb = 1
                            problems = []
                            for pb in list_of_problems:

                                if regex.start_problem_pattern.match(pb.text):
                                    if start_of_pb == 1:
                                        problem += pb.text
                                    else:
                                        problems.append(problem)
                                        problem = pb.text
                                        start_of_pb = 1
                                    start_of_pb = 0
                                else:

                                    problem += pb.text

                            problems.append(problem)
                            list_of_problems = problems

                        nr_pb = 1
                        for problem in list_of_problems:
                            if paragraphs_pb:
                                text = problem
                            else:
                                text = problem.text
                            # print(text)
                            probably_name = detect_name_function(text)

                            if probably_name != -1:
                                string_hardcoded = f"def {probably_name}(param): \n\tpass\n\n"
                                file_lab.write(string_hardcoded)
                            else:
                                string_hardcoded = f"def ex{nr_pb}(param): \n\tpass\n\n"
                                file_lab.write(string_hardcoded)
                            nr_pb += 1
            except:
                print("Unable to create this file.\n")
            else:
                print("File was created successfully!")
            # break
