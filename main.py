# ---- IMPORTS ----

import requests
import bs4
from bs4 import BeautifulSoup as bs
import re
import sys
import os


# ---- ----

def create_director(path_to_create_dirs, name):
    dir_name = os.path.join(path_to_create_dirs, name)

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print(f'Director {dir_name} created successfully.')
    # else:
    #     print(f'The dir.{dir_name} already exists.')
    #     exit(-1)
    return dir_name


def detect_name_function(text):
    pattern1 = re.compile(r'([a-z]+)([_a-z0-9]+)*(\(.*\))+')
    pattern2 = re.compile(r'([a-z]+)(_[a-z0-9]+)+([\s]+function)')
    nume_fct = pattern1.search(text)

    name = ''
    if nume_fct:
        name += nume_fct.group(1)
        name += nume_fct.group(2) if nume_fct.group(2) else ''
    else:
        nume_fct = pattern2.search(text)
        if nume_fct:
            name += nume_fct.group(1)
            name += nume_fct.group(2) if nume_fct.group(2) else ''

    return name if name != '' else -1


# --- REGEXP ----
url_regex = re.compile('^/site/fiipythonprogramming/laboratories/lab-')
labs_regex = re.compile(r'^Lab|lab')
# ---  ----
paragraphs_pb = False

if __name__ == '__main__':

    path_to_create_dirs = sys.argv[1]
    # print(path_to_create_dirs)

    r = requests.get("https://sites.google.com/site/fiipythonprogramming/administrative?authuser=0")
    bs_page_obj = bs(r.content, 'html.parser')

    # print(bs_page_obj.prettify())

    all_links = bs_page_obj.findAll('a')

    link_labs = [link['href'] for link in all_links if labs_regex.match(str(link.text))][0]

    # print(link_labs)

    lab_req = requests.get(f"https://sites.google.com{link_labs}")
    labs_page = bs(lab_req.content, 'html.parser')

    container_labs = labs_page.find('div', attrs={'class': "tyJCtd mGzaTb baZpAe"})
    links_to_labs = container_labs.findAll('a')

    for link_lab in links_to_labs:
        if url_regex.match(link_lab['href']):
            # print(url['href'])
            name_of_dir = link_lab.text
            target_dir = create_director(path_to_create_dirs, name_of_dir)

            go_to_link_lab = requests.get(f"https://sites.google.com{link_lab['href']}")
            laborator = bs(go_to_link_lab.content, 'html.parser')

            list_of_problems = laborator.find('ol')

            if list_of_problems is None:
                list_of_problems = laborator.findAll('p')
                paragraphs_pb = True
            else:
                paragraphs_pb = False

            print("Director NOU")

            with open(os.path.join(target_dir, f'lab{target_dir[-1]}.py'), "w") as file_lab:
                if list_of_problems:
                    if paragraphs_pb is False:
                        list_of_problems = list_of_problems.findAll('li')
                    else:
                        problema = ''
                        start_of_pb = 1
                        problems = []
                        for pb in list_of_problems:
                            # print(pb.text)
                            if re.match(r'[\s]*(\d{1,2}[\.|\)]{1}).', pb.text):
                                # print("Cu nr:", pb.text)
                                if start_of_pb == 1:
                                    problema += pb.text
                                else:
                                    problems.append(problema)
                                    problema = pb.text
                                    start_of_pb = 1
                                start_of_pb = 0
                            else:
                                # print("FARA NR", pb.text)
                                problema += pb.text

                        # list_of_problems = [pb for pb in list_of_problems
                        #                     if len(str(pb.text)) and re.match(r'(\s*)(\d{1,2}[\.|\)]{1}).', pb.text) or
                        #                     re.match(r'^(\s*)(Example|example|Ex)', pb.text)]
                        problems.append(problema)
                        list_of_problems = problems

                    nr_pb = 1
                    for problem in list_of_problems:
                        if paragraphs_pb:
                            text = problem
                        else:
                            text = problem.text
                        #print(text)
                        probably_name = detect_name_function(text)

                        if  probably_name != -1:
                            string_hardcoded = f"def {probably_name}(param): \n\tpass\n\n"
                            file_lab.write(string_hardcoded)
                        else:
                            string_hardcoded = f"def ex{nr_pb}(param): \n\tpass\n\n"
                            file_lab.write(string_hardcoded)
                        nr_pb += 1
            # break
