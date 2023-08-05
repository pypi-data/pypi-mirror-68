#!/usr/bin/env python3

"""
市外局番のリストを作成

正式なものは
http://www.soumu.go.jp/main_sosiki/joho_tsusin/top/tel_number/shigai_list.html
ここにあるが、Word / PDF なので扱いづらい。￥

Wikipedia
https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC%E3%81%AE%E5%B8%82%E5%A4%96%E5%B1%80%E7%95%AA # NOQA
からもらう。
"""
from collections import defaultdict
from itertools import chain

import requests
from bs4 import BeautifulSoup

SOURCE_URL = 'https://ja.wikipedia.org/wiki/' \
             '%E6%97%A5%E6%9C%AC%E3%81%AE%E5%B8%82%E5%A4%96%E5%B1%80%E7%95%AA'

OUTPUT_FILE = 'prefix_numbers.py'

special_prefixes = [
    '020',
    '050',
    '060',
    '070',
    '080',
    '090',
    '0120',
    '0800',
    '0990',
    '0570',
]


class HtmlTableNotFound(Exception):
    pass


class InvalidHtmlTable(Exception):
    pass


def get_number_prefixes():
    response = requests.get(SOURCE_URL)
    soup = BeautifulSoup(response.content, features="html.parser")
    table = soup.find('table', {'class': 'wikitable'})
    if not table:
        raise HtmlTableNotFound()

    if table.find('tr').find('th').text.strip() != '市外局番':
        raise InvalidHtmlTable('市外局番テーブルがありません')

    for tr in table.find_all('tr'):
        td = tr.find('td')
        if not td:
            continue
        prefix_number = td.text.strip()
        if not prefix_number:
            continue
        if not prefix_number.startswith('0'):
            continue

        if not prefix_number.isdigit():
            continue
        yield prefix_number


def main():
    python_text = '# flake8: NOQA\nphone_number_prefixes = {}\n'

    indexed_numbers = defaultdict(set)
    for n in chain(get_number_prefixes(), special_prefixes):
        indexed_numbers[len(n)].add(n)

    with open(OUTPUT_FILE, 'w') as fp:
        fp.write(python_text.format(dict(indexed_numbers)))


if __name__ == '__main__':
    main()
