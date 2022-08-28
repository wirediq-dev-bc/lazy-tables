#!/home/bcarver/.py_venvs/uci-wizard/bin/python3

from genericpath import exists
from pprint import pprint
from re import match, compile
from typing import Dict, List
from json import dump, load
from sys import argv, exit
from logging import getLogger, basicConfig, DEBUG, INFO

from bs4 import BeautifulSoup, element

from constants import UCI_DOCS, SAVE_HTML, SAVE_JSON, LOG_FMT



LOG_LEVEL = DEBUG
basicConfig(level=LOG_LEVEL, format=LOG_FMT)
logger = getLogger(__name__)


def parse_args():
    ARG = argv[1]
    if not ARG:
        LOG_LEVEL = INFO
    elif match('--viewer', ARG):
        read_uci_tables()
    elif match('--debug', ARG):
        LOG_LEVEL = DEBUG
    elif match('--.*', ARG):
        logger.error(f'UnknownToken: {ARG}')
        exit(1)
    logger.setLevel(level=LOG_LEVEL)


def make_soup(config: str, html_parser: str = 'html.parser') -> BeautifulSoup:
    html_tree_path = f"{SAVE_HTML}/{config}.html"
    logger.debug(f"{'Load HTML from path':16}: {html_tree_path}\n")
    with open(html_tree_path, mode='r') as reader:
        soup = BeautifulSoup(reader, html_parser)
    return soup


def uci_extract(soup: BeautifulSoup) -> Dict:
    page_tables = {}

    table: element.Tag
    for table in soup.find_all('table'):        
        try:
            table_identifier = table.find('th').text
        except AttributeError:
            continue

        if match('.*Name.*', table_identifier):
            tname = find_table_name(table)
            tbs = table_handler(table)

            if page_tables.get(tname):
                multi_keyed = multi_key_handler(page_tables[tname], tbs)
                page_tables[tname] = multi_keyed
            else:
                page_tables[tname] = tbs

    return page_tables


def find_table_name(table: element.Tag) -> str:
    try:
        table_name = table.find_previous('h3')
        tname = table_name.attrs['id']
    except AttributeError:
        table_name = table.find_previous('h2')
        tname = table_name.attrs['id']
    logger.debug(f" {'Table Name':10}: {tname}")
    return tname


def table_handler(table: element.Tag) -> Dict[str, List]:
    extracted = {}
    table_values = table.find_all('tr')

    rows: element.Tag
    col_count = 0
    for rows in table_values:
        cols = rows.find_all(class_=compile('col'))

        if len(cols) > 2:
            listy = [c.text.strip() for c in cols[:-1]]
            extracted[listy[0]] = listy[1:]
        else:
            listy = [c.text.strip() for c in cols]
            if len(cols) < col_count:
                tmp = [*['null' for _ in range(col_count - 3)], listy[1]]
            else:
                tmp = [listy[1]]
            extracted[listy[0]] = tmp

        col_count = len(cols)

    return extracted


def multi_key_handler(multi_keyed, table) -> List[Dict]:
    if isinstance(multi_keyed, list):
        mkeyed = [*multi_keyed, table]
    else:
        mkeyed = [multi_keyed, table]
    return mkeyed


def giga_dict_to_json(payload: Dict, ):
    with open(SAVE_JSON, mode='w') as writer:
        dump(payload, writer)


def extraction_loop():
    UCI_CONFIGURATIONS = {}
    for config in UCI_DOCS:
        good_soup = make_soup(config)
        scraped = uci_extract(good_soup)
        UCI_CONFIGURATIONS[config] = scraped
        logger.debug(f'Table Count: {len(scraped)}\n')
    return UCI_CONFIGURATIONS


def read_uci_tables():
    if not exists(SAVE_JSON):
        logger.error(f"FileNotFoundError: {SAVE_JSON}")
        exit(1)
    with open(SAVE_JSON, mode='r') as reader:
        json_tables = load(reader)
    pprint(json_tables, width=160, sort_dicts=False)
    exit(0)


def main():
    parse_args()
    giga_dict = extraction_loop()
    giga_dict_to_json(giga_dict)


if __name__ == "__main__":
    main()
