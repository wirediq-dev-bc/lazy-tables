#!/home/bcarver/.py_venvs/uci-wizard/bin/python3

from genericpath import exists
from pprint import pprint
from json import load
from re import match
from typing import Dict
from logging import basicConfig, getLogger, DEBUG


from pandas import DataFrame, ExcelWriter
from xlsxwriter.exceptions import InvalidWorksheetName

from constants import SAVE_JSON, SAVE_XLSX, LOG_FMT


LOG_LEVEL = DEBUG
basicConfig(level=LOG_LEVEL, format=LOG_FMT)
logger = getLogger(__name__)


def load_json_tables():
    with open(SAVE_JSON, mode='r') as reader:
        json_tables = load(reader)
    return json_tables


def panda_tables(json_tables: Dict):
    for key, value in json_tables.items():
        logmsg = f'\033[38;5;81mTable Count: {len(value)}\033[00m'
        print(); logger.debug(logmsg)
        group = group_handler(key, value)
        dataframes_to_excel(key, group)


def group_handler(config: str, page_tables: Dict) -> Dict:
    logmsg = f'\033[38;5;46mParsing Configurations: {config}\033[00m'
    logger.debug(logmsg)
    dfs = {}
    for tname, table in page_tables.items():
        if not isinstance(table, list):
            dfs[tname] = json_to_dataframe(table)
    return dfs


def json_to_dataframe(table: Dict) -> DataFrame:
    for key in ['Name', 'Option Name']:
        if table.get(key):
            table_cols = table[key]
            del table[key]
    return DataFrame.from_dict(table, orient='index', columns=table_cols)


def dataframes_to_excel(config: str, df_group: DataFrame):
    save_as = f'{SAVE_XLSX}/{config}.xlsx'
    with ExcelWriter(save_as, mode='w', engine='xlsxwriter') as writer:
        for name, df in df_group.items():
            logger.debug(f'\033[38;5;226mTable: {config}.{name}\033[00m\n')
            print(f'\n{df.to_markdown()}\n')
            name = safe_names(name)
            try:
                df.to_excel(writer, sheet_name=name)
            except InvalidWorksheetName:
                print(f'InvalidWorksheetName: {name}')
                exit(1)
            

def safe_names(name: str):
    if len(name) < 31:
        return name
    newname =  ''.join([i for i in name[:30]])
    return '_'.join(newname.split('_')[:-1])
    

def main():
    json_tables = load_json_tables()
    panda_tables(json_tables)


if __name__ == "__main__":
    main()
