#!/home/bcarver/.py_venvs/uci-wizard/bin/python3


from scraper import html_writer
from extractor import extraction_loop
from build_excel import panda_tables


def main():
    html_writer()
    json_tables = extraction_loop()
    panda_tables(json_tables)


if __name__ == "__main__":
    main()
