from parser_libraries import functions as f
import os
from bs4 import BeautifulSoup


COMPLEX_URL = 'https://ru.wikipedia.org/wiki/%D0%A1%D1%83%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D1%8B_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B9_%D0%A4%D0%B5%D0%B4%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%B8'
HOST = 'https://ru.wikipedia.org/'


def get_wiki_person(link, work_id):
    html = f.get_html(link)
    soup = BeautifulSoup(html.text, 'html.parser')
    full_name = soup.find('h1', class_='firstHeading').get_text().lower().replace(',', '')
    if full_name.find('(') != -1:
        full_name = full_name[:full_name.find('(')]
    full_name = f.get_name(full_name)
    print(full_name)
    soup = soup.find('table', class_='infobox')
    try:
        image_link = soup.find('td', class_='infobox-image').find('img').get('srcset')
        if image_link != None:
            image_link = 'https:' + image_link[image_link.find(', ')+2:image_link.find(' 2x')]
        else:
            image_link = 'https:' + soup.find('td', class_='infobox-image').find('img').get('src')
    except:
        image_link = f.get_yandex_image(full_name)
    date = f.get_dig_date(soup.find('span', class_='bday').get_text(), 2)

    return {'position_id': work_id, 'first_name': full_name[1], 'middle_name': full_name[2], 'last_name': full_name[0],
            'bday': date['day'], 'bmonth': date['month'], 'byear': date['year'], 'image_link': image_link, 'link': link}


def get_page(link):
    people = []
    html = f.get_html(link)
    soup = BeautifulSoup(html.text, 'html.parser')
    soup = soup.find('table', class_='infobox')
    soup = soup.find_all('tr')
    for a in soup:
        try:
            cont = a.find('th', class_='plainlist').get_text().lower()
            if cont != None:
                if cont.find('губернатор') != -1 or cont.find('председатель') != -1 or cont.find('мэр') != -1  or cont.find('премьер-министр') != -1 or cont.find('глава') != -1:
                    title = a.find('td').find('a').get('title')
                    if title.find('страница отсутствует') == -1:
                        person_link = a.find('td').find('a').get('href')
                        people.append(get_wiki_person(HOST + person_link, 33))
        except:
            continue
    return people


def parser():
    html = f.get_html(COMPLEX_URL)
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
        links = []
        people = []
        soup = soup.find('table', class_='standard')
        prob = soup.find_all('tr', class_='dark')
        soup = soup.find_all('tr')
        soup = soup[2:-1]
        for a in soup:
            flag = True
            for b in prob:
                if a == b:
                    flag = False
            if flag:
                links.append(HOST + a.find('a').get('href'))
        for link in links:
            people.extend(get_page(link))
        return people
    else:
        return [{'code': 2, 'script': os.path.basename(__file__)}]