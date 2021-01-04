# ---- IMPORTS ----

import os
import re
import sys

import requests
from bs4 import BeautifulSoup as bs

import regexs_utils as regex
import file_utils
import preprocessing_utils as information_manager

paragraphs_pb = False
nr_params = 1

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
    # print(links_to_labs)

    for link_lab in links_to_labs:
        if regex.url_regex.match(link_lab['href']):
            # print(url['href'])
            name_of_dir = link_lab.text
            target_dir = file_utils.create_director(path_to_create_dirs, name_of_dir)

            go_to_link_lab = requests.get(f"https://sites.google.com{link_lab['href']}")
            laborator = bs(go_to_link_lab.content, 'html.parser')

            list_of_problems = laborator.find('ol')
            # print(list_of_problems)
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
                            list_of_problems = information_manager.search_problems(list_of_problems)

                        # print("Lab", target_dir)
                        # print(list_of_problems)
                        # print("-"*10)
                        nr_pb = 1
                        for problem in list_of_problems:
                            sb_pbs = information_manager.search_sub_problems(paragraphs_pb, problem)
                            # print("AM SUBPB?", sb_pbs)
                            if len(sb_pbs) == 0:
                                if paragraphs_pb:
                                    text = problem
                                else:
                                    text = problem.text  # scot dintr-un li acel text <li...> text ... < /li>

                                (probably_name, nr_params) = information_manager.get_function_details(text)

                                params = information_manager.get_list_of_params(nr_params)

                                if probably_name != -1:
                                    file_utils.create_function_pb(probably_name, params, file_lab)
                                else:
                                    file_utils.create_function_pb(nr_pb, params, file_lab)
                            else:
                                nr_subpb = 1
                                for subpb in sb_pbs:
                                    (probably_name, nr_params) = information_manager.get_function_details(subpb)

                                    if probably_name != -1:
                                        file_utils.create_function_subpb(nr_pb, probably_name, params, file_lab)
                                    else:
                                        file_utils.create_function_subpb(nr_pb, nr_subpb, params, file_lab)
                                    nr_subpb += 1
                            nr_pb += 1
            except:
                print("Unable to create this file.\n")
            else:
                print("File was created successfully!")
            # break
