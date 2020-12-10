# ---- IMPORTS ----

import requests
import bs4
from bs4 import BeautifulSoup as bs
import re
import sys
import os


# ---- ----

def create_director(path_to_create_dirs, name):
    dir_name = f'{path_to_create_dirs}/{name}'

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print(f'Director {dir_name} created successfully.')
    else:
        print(f'The dir.{dir_name} already exists.')
        exit(-1)


def create_file(path_to_create_file, name):
    pass


if __name__ == '__main__':

    regex = re.compile('^/site/fiipythonprogramming/laboratories/lab-')
    path_to_create_dirs = sys.argv[1]
    # print(path_to_create_dirs)

    r = requests.get("https://sites.google.com/site/fiipythonprogramming/administrative?authuser=0")
    bs_page_obj = bs(r.content, 'html.parser')
    # print(bs_page_obj.prettify())

    all_links = bs_page_obj.findAll('a')
    link_labs = all_links[3]['href']

    lab_req = requests.get(f"https://sites.google.com{link_labs}")
    labs_page = bs(lab_req.content, 'html.parser')

    container_labs = labs_page.find('div', attrs={'class': "tyJCtd mGzaTb baZpAe"})
    links_to_labs = container_labs.findAll('a')

    for url in links_to_labs:
        if re.match(regex, url['href']):
            # print(url['href'])
            name_of_dir = url.string
            create_director(path_to_create_dirs, name_of_dir)

            go_to_link_lab = requests.get(f"https://sites.google.com{url['href']}")
            laborator = bs(go_to_link_lab.content, 'html.parser')
            list_of_problems = laborator.find('ol')
            if list_of_problems:
                list_of_problems = list_of_problems.findAll('li')
                for problem in list_of_problems:
                    pass
                    # print(problem.string)
            # break
