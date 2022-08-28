#!/home/bcarver/.py_venvs/uci-wizard/bin/python3

from logging import basicConfig, getLogger, DEBUG

from requests import get

from constants import LOG_FMT, SAVE_HTML, BASE_URL, UCI_DOCS


LOG_LEVEL = DEBUG
basicConfig(level=LOG_LEVEL, format=LOG_FMT)
logger = getLogger(__name__)


def get_html(config_url: str) -> str:
    TARGET_URL = f"{BASE_URL}/{config_url}"
    page_data = get(TARGET_URL)
    return page_data.text


def save_html(config_name: str, html_tree: str):
    SAVE_AS = f"{SAVE_HTML}/{config_name}.html"
    logger.info(f"{config_name:10}: {'SavedHTML':10}-> {SAVE_AS}")
    with open(SAVE_AS, mode='w') as writer:
        writer.writelines(html_tree)


def html_writer():
    for config, url in UCI_DOCS.items():
        tree = get_html(url)
        save_html(config_name=config, html_tree=tree)


if __name__ == "__main__":
    html_writer()
