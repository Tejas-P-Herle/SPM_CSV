from bs4 import BeautifulSoup
from urllib.request import urlopen

url = 'http://www.babynamewizard.com/the-top-1000-baby-names-of-2016-united-states-of-america'
names = None


def gen_names():
    page = urlopen(url)
    page_html = page.read()
    page_soup = BeautifulSoup(page_html, 'html.parser')

    name_list = []
    tables = page_soup.findAll('table')

    for table in [tables[1], tables[0]]:
        table_rows = table.findAll('tr')[1:]
        for table_row in table_rows:
            name_list.append(table_row.findAll('td')[1].text)

    return name_list


if __name__ == '__main__':
    names = gen_names()
