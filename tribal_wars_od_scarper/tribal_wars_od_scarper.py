import locale
import os
import re
import time

import requests
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL, '')
RESULT_FOLDER = 'results'

base_urls = dict(
    hu=dict(
        archive=f'https://www.klanhaboru.hu/archive/hu',
        hof=f'https://www.klanhaboru.hu/page/hall-of-fame'
    ),
    en=dict(
        archive=f'https://www.tribalwars.net/en-dk/archive/en',
        hof=f'https://www.tribalwars.net/en-dk/page/hall-of-fame'
    ),
    de=dict(
        archive=f'https://www.die-staemme.de/archive/de',
        hof=f'https://www.die-staemme.de/page/hall-of-fame'
    ),
    ae=dict(
        archive=f'https://www.tribalwars.ae/archive/ae',
        hof=f'https://www.tribalwars.ae/page/hall-of-fame'
    ),
    cz=dict(
        archive=f'https://www.divokekmeny.cz/archive/cs',
        hof=f'https://www.divokekmeny.cz/page/hall-of-fame'
    ),
    nl=dict(
        archive=f'https://www.tribalwars.nl/archive/nl',
        hof=f'https://www.tribalwars.nl/page/hall-of-fame'
    ),
    uk=dict(
        archive=f'https://www.tribalwars.co.uk/archive/uk',
        hof=f'https://www.tribalwars.co.uk/page/hall-of-fame'
    ),
    us=dict(
        archive=f'https://www.tribalwars.us/archive/us',
        hof=f'https://www.tribalwars.us/page/hall-of-fame'
    ),
    fr=dict(
        archive=f'https://www.guerretribale.fr/archive/fr',
        hof=f'https://www.guerretribale.fr/page/hall-of-fame'
    ),
    gr=dict(
        archive=f'https://www.fyletikesmaxes.gr/archive/gr',
        hof=f'https://www.fyletikesmaxes.gr/page/hall-of-fame'
    ),
    it=dict(
        archive=f'https://www.tribals.it/archive/it',
        hof=f'https://www.tribals.it/page/hall-of-fame'
    ),
    pl=dict(
        archive=f'https://www.plemiona.pl/archive/pl',
        hof=f'https://www.plemiona.pl/page/hall-of-fame'
    ),
    br=dict(
        archive=f'https://www.tribalwars.com.br/archive/br',
        hof=f'https://www.tribalwars.com.br/page/hall-of-fame'
    ),
    pt=dict(
        archive=f'https://www.tribalwars.com.pt/archive/pt',
        hof=f'https://www.tribalwars.com.pt/page/hall-of-fame'
    ),
    ro=dict(
        archive='https://www.triburile.ro/archive/ro',
        hof=f'https://www.triburile.ro/page/hall-of-fame'
    ),
    ru=dict(
        archive=f'https://www.voynaplemyon.com/ru-ru/archive/ru',
        hof=f'https://www.voynaplemyon.com/ru-ru/page/hall-of-fame'
    ),
    sk=dict(
        archive=f'https://www.divoke-kmene.sk/archive/sk',
        hof=f'https://www.divoke-kmene.sk/page/hall-of-fame'
    ),
    es=dict(
        archive=f'https://www.guerrastribales.es/archive/es',
        hof=f'https://www.guerrastribales.es/page/hall-of-fame'
    ),
    ch=dict(
        archive=f'https://www.staemme.ch/archive/ch',
        hof=f'https://www.staemme.ch/page/hall-of-fame'
    ),
    tr=dict(
        archive=f'https://www.klanlar.org/archive/tr',
        hof=f'https://www.klanlar.org/page/hall-of-fame'
    ),
    ua=dict(
        archive=f'https://www.voynaplemyon.com/uk-ua/archive/ru',
        hof=f'https://www.voynaplemyon.com/uk-ua/page/hall-of-fame'
    )
)


def get_sort_key(row_values, rankings_type):
    if rankings_type == 'player_village':
        return int(row_values[4].replace('.', ''))
    elif rankings_type == 'player_point':
        return int(row_values[3].replace('.', ''))
    else:
        return int(row_values[2].replace('.', ''))


def check_folders_and_create_if_necessary(folder):
    if not os.path.exists(RESULT_FOLDER):
        os.makedirs(RESULT_FOLDER)
    if not os.path.exists(f'{RESULT_FOLDER}/{folder}'):
        os.makedirs(f'{RESULT_FOLDER}/{folder}')
    else:
        pass


def format_numbers(row_values):
    return [locale.format_string('%d', int(value), grouping=True) if value.encode('utf-8').decode(
        'unicode_escape').isdigit() else value for value in row_values]


def url_scarper(response, domain, all_results, server_number, rankings_top):
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='ranking-table')

        if table:
            rows = table.find_all('tr')
            if rankings_top > len(rows) - 1:
                rankings_top = len(rows) - 1

            for row_num, row in enumerate(rows[1:rankings_top + 1], start=1):
                row_values = [td.get_text(strip=True) for td in row.find_all('td')]
                row_values = format_numbers(row_values)
                all_results.append((server_number, row_num, row_values))

        else:
            print(f'{domain.upper()}{server_number}: Table with class \'ranking-table\' not found on the page.')


def hof_url_cleaner(url: str):
    return re.sub('[^0-9]', '', url)


def find_closed_servers(hof_url):
    closed_servers = []
    response = requests.get(hof_url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    inactive_li_elements = soup.find_all('li', class_='inactive')

    for li_element in inactive_li_elements:
        href = li_element.find('a')['href']
        if not any(substring in href for substring in ['huc', 'hup']):
            closed_servers.append(hof_url_cleaner(href))

    return closed_servers


def get_rankings_from_page(domain: str, rankings_type: str, servers_from: int, servers_to: int, rankings_top: int):
    all_results = []
    global_row_num = 1
    if rankings_type == 'od':
        type = '/kill'
    elif rankings_type == 'oda':
        type = '/kill/att'
    elif rankings_type == 'odd':
        type = '/kill/def'
    elif rankings_type == 'ods':
        type = '/kill/support'
    elif rankings_type == 'player_village' or rankings_type == 'player_point':
        type = ''
    else:
        type = '/kill'

    check_folders_and_create_if_necessary(domain)
    find_closed_servers(base_urls[domain]['hof'])

    for server_number in range(servers_from, servers_to + 1):
        url = f'{base_urls[domain]["archive"]}{server_number}/players{type}'

        response = requests.get(url)

        try:
            url_scarper(response, domain, all_results, server_number, rankings_top)
        except Exception:
            print(
                f'{domain.upper()}{server_number}: Failed to retrieve the page. Status code: {response.status_code} in {rankings_type}. Retrying....')
            url_scarper(response, domain, all_results, server_number, rankings_top)

    sorted_results = sorted(all_results, key=lambda sorting_field: get_sort_key(sorting_field[2], rankings_type),
                            reverse=True)

    with open(f'{RESULT_FOLDER}/{domain}/result_{rankings_type}_{domain}.txt', 'w', encoding="utf-8") as file:
        for server_number, _, result in sorted_results:
            formatted_result = format_numbers(result)
            file.write(f'#{global_row_num} {domain.upper()}{server_number} {formatted_result}\n')
            global_row_num += 1
    time.sleep(0.15)


get_rankings_from_page('hu', 'player_point', 1, 3, 50)
# get_rankings_from_page('de', 'player_village', 1, 223, 50)
# get_rankings_from_page('de', 'od', 1, 223, 20)
# get_rankings_from_page('de', 'oda', 1, 223, 20)
# get_rankings_from_page('de', 'odd', 1, 223, 20)
# get_rankings_from_page('de', 'ods', 1, 223, 20)
