import time

import requests
from bs4 import BeautifulSoup


def get_sort_key(row_values):
    return int(row_values[2].replace(".", ""))


def url_scarper(response, all_results, server_number, rankings_top):
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='ranking-table')

        if table:
            rows = table.find_all('tr')

            for row in rows[1:rankings_top + 1]:
                row_values = [td.get_text(strip=True) for td in row.find_all('td')]
                all_results.append((server_number, row_values))

        else:
            print(f"HU{server_number}: Table with class 'ranking-table' not found on the page.")


def get_rankings_from_page(rankings_type: str, servers_from: int, servers_to: int, rankings_top: int):
    all_results = []
    if rankings_type == 'od':
        type = 'kill'
    elif rankings_type == 'oda':
        type = 'kill/att'
    elif rankings_type == 'odd':
        type = 'kill/def'
    elif rankings_type == 'ods':
        type = 'kill/support'
    else:
        type = 'kill'

    for server_number in range(servers_from, servers_to + 1):
        url = f"https://www.klanhaboru.hu/archive/hu{server_number}/players/{type}"

        response = requests.get(url)

        try:
            url_scarper(response, all_results, server_number, rankings_top)
        except Exception:
            print(
                f"HU{server_number}: Failed to retrieve the page. Status code: {response.status_code} in {rankings_type}. Retrying....")
            url_scarper(response, all_results, server_number, rankings_top)

    sorted_results = sorted(all_results, key=lambda x: get_sort_key(x[1]), reverse=True)

    with open(f'result_{rankings_type}.txt', "w") as file:
        for server_number, result in sorted_results:
            file.write(f"HU{server_number} {result}\n")
    time.sleep(1)


get_rankings_from_page('oda', 1, 84, 20)
get_rankings_from_page('od', 1, 84, 20)
get_rankings_from_page('odd', 1, 84, 20)
get_rankings_from_page('ods', 1, 84, 20)
