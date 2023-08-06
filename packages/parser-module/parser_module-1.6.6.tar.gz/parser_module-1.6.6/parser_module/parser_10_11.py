from parser_libraries import functions as f
import os
from bs4 import BeautifulSoup


URL = 'https://www.mid.ru/activity/shots/personnel/extraordinary_ambassador#main-content'
HOST = 'https://www.mid.ru'


def parser_10_11():
    rel = 6
    html = f.get_html(URL)
    counter = 1
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
        print(soup)
        contents = soup.find('section', class_='block')
        contents = contents.find_all('tr')
        contents = contents[1:4]
        people = []
        for content in contents:
            print(str(counter) + ' человек пошёл!')
            counter += 1
            name = content.find('span', class_='masha_index masha_index' + str(rel)).get_text() + ' ' + \
                   content.find('span', class_='masha_index masha_index' + str(rel + 1)).get_text() + ' ' + \
                   content.find('span', class_='masha_index masha_index' + str(rel + 2)).get_text()
            people.append({
                'name': name
            })
            rel += 7
        return people
    else:
        return [{'code': 2, 'script': os.path.basename(__file__)}]


people = parser_10_11()
print(people)