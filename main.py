
#Load in the necessary libraries

import  requests #for calling pages
import bs4
from bs4 import BeautifulSoup as bs
import re

if __name__ == '__main__':

    regex = re.compile('^/site/fiipythonprogramming/laboratories/lab-')
    #load the webpage content by calling a get from requests
    r = requests.get("https://sites.google.com/site/fiipythonprogramming/administrative?authuser=0")

    #Convert to a bs object
    bs_page_obj = bs(r.content, 'html.parser')

    #print(bs_page_obj.prettify())
    all_links = bs_page_obj.findAll('a')
    link_labs = all_links[3]['href']

    lab_req = requests.get(f"https://sites.google.com{link_labs}")
    labs_page = bs(lab_req.content, 'html.parser')

    container_labs = labs_page.find('div', attrs={'class': "tyJCtd mGzaTb baZpAe"})
    links_to_labs = container_labs.findAll('a')

    for url in links_to_labs:
        if re.match(regex, url['href']):
            #print(url['href'])
            go_to_link_lab = requests.get(f"https://sites.google.com{url['href']}")
            laborator = bs(go_to_link_lab.content, 'html.parser')
            list_of_problems = laborator.find('ol')
            if list_of_problems:
                list_of_problems = list_of_problems.findAll('li')
                for problem in list_of_problems:
                    print(problem.string)
            #break
    #print(links_to_labs[1]['href'])