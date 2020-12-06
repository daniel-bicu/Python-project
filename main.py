
import  requests
from bs4 import BeautifulSoup as bs

if __name__ == '__main__':
    page =requests.get('https://sites.google.com/site/fiipythonprogramming/administrative?authuser=0')
    content = bs(page.text, 'html.parser')
    print(content.prettify())

