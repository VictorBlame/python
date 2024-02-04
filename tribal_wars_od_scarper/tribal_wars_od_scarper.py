import locale
import os
import time

import requests
from bs4 import BeautifulSoup

# Set the locale for formatting numbers with thousands separators
locale.setlocale(locale.LC_ALL, '')
RESULT_FOLDER = 'results'

base_urls = dict(
    hu=f'https://www.klanhaboru.hu/archive/hu',
    en=f'https://www.tribalwars.net/en-dk/archive/en',
    de=f'https://www.die-staemme.de/archive/de',
    ae=f'https://www.tribalwars.ae/archive/ae',
    cz=f'https://www.divokekmeny.cz/archive/cs',
    nl=f'https://www.tribalwars.nl/archive/nl',
    uk=f'https://www.tribalwars.co.uk/archive/uk',
    us=f'https://www.tribalwars.us/archive/us',
    fr=f'https://www.guerretribale.fr/archive/fr',
    gr=f'https://www.fyletikesmaxes.gr/archive/gr',
    it=f'https://www.tribals.it/archive/it',
    pl=f'https://www.plemiona.pl/archive/pl',
    br=f'https://www.tribalwars.com.br/archive/br',
    pt=f'https://www.tribalwars.com.pt/archive/pt',
    ro=f'https://www.triburile.ro/archive/ro',
    ru=f'https://www.voynaplemyon.com/ru-ru/archive/ru',
    sk=f'https://www.divoke-kmene.sk/archive/sk',
    es=f'https://www.guerrastribales.es/archive/es',
    ch=f'https://www.staemme.ch/archive/ch',
    tr=f'https://www.klanlar.org/archive/tr',
    ua=f'https://www.voynaplemyon.com/uk-ua/archive/ru'
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

    for server_number in range(servers_from, servers_to + 1):
        url = f'{base_urls[domain]}{server_number}/players{type}'

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
