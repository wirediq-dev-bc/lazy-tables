#!/home/bcarver/.py_venvs/uci-wizard/bin/python3

LOG_ID = '[%(lineno)d][%(filename)s][%(funcName)s](%(levelname)s)'
LOG_FMT = '{:60} >> %(message)s'.format(LOG_ID)

BASE_PATH = '/usr/src'

SAVE_HTML = f'{BASE_PATH}/app/docs/html'
SAVE_JSON = f'{BASE_PATH}/app/docs/tables.json'
SAVE_XLSX = f'{BASE_PATH}/app/docs/xlsx'

BASE_URL = 'https://openwrt.org/docs/guide-user'

UCI_DOCS = {
    'dhcp': 'base-system/dhcp',
    'network': 'network/ucicheatsheet',
    'firewall': 'firewall/firewall_configuration'
}
