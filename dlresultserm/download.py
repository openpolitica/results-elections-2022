from urllib.parse import urljoin
from dlresultserm.api.request import getResponse
from dlresultserm.config import url_base
from dlresultserm.utils.parsecsv import get_csv_from_string

from dlresultserm.logger import logger


def build_url(code):
    return urljoin(url_base, code)


def get_info_by_ubigeo(ubigeocode):

    api_url = build_url(ubigeocode)
    logger.debug(f"Downloading from {api_url}")
    data = getResponse(api_url)

    return {
        "data": data,
        "ubigeo": ubigeocode
    }


def get_ubigeo_list(string, index, has_header=True):

    init_index = 1 if has_header else 0

    return [row[index] for row in get_csv_from_string(string)[init_index:]]


def get_info_from_ubigeo_list(ubigeo_list):

    return [get_info_by_ubigeo(ubigeo) for ubigeo in ubigeo_list]


def process_data_to_tables(data, tables, keys):

    n_data = {}
    for table in tables:
        if isinstance(data["data"][table], list):
            n_data[table] = [[row[key] for key in keys[table]]
                             for row in data["data"][table]]

        elif isinstance(data["data"][table], dict):
            n_data[table] = [data["data"][table][key] for key in keys[table]]

        else:
            raise ValueError()

    n_data["ubigeo"] = data["ubigeo"]

    return n_data
