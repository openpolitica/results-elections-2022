from optparse import OptionParser
import os
from pathlib import Path
from dlresultserm.builddb import insert_results_values, reset_results_tables

from dlresultserm.logger import logger, levels, setLoggerLevel
from dlresultserm.download import (
    get_ubigeo_list, get_info_from_ubigeo_list, process_data_to_tables)
from dlresultserm.utils.getresource import get_resource_content
import dlresultserm.config as config
from dlresultserm.utils.json import save_to_json_file, get_json_from_file
from dlresultserm.db.sqlite import connect

usage = "usage: %prog [options] tablename"
parser = OptionParser(usage=usage, prog="dlgsheet")
parser.add_option("-l", "--log-level", dest="loglevel",
                  help="set log level. Available options: " + ",".join(levels))

parser.add_option("-d", "--output-folder", dest="output_folder",
                  help="save to output folder", metavar="FOLDER")

# Reference https://stackoverflow.com/a/29301200/5107192


def get_comma_separated_args(option, _, value, parser):
    setattr(parser.values, option.dest, value.split(','))


def main():

    (options, _) = parser.parse_args()

    if options.loglevel is not None:
        loglevel = options.loglevel
    else:
        loglevel = "info"

    setLoggerLevel(loglevel)

    logger.debug(options)

    DEFAULT_FOLDER_NAME = "output"
    DEFAULT_JSON_FILE_NAME = "results.json"
    DEFAULT_SQLITE_FILE_NAME = "results.db"

    if(options.output_folder is not None):
        foldername = options.output_folder
    else:
        foldername = DEFAULT_FOLDER_NAME
        logger.warning(
            "Not folder name provided via --output-folder. Usign default: " +
            foldername)

    logger.info("Getting list of ubigeos")

    ubigeo_list = get_ubigeo_list(
        get_resource_content(
            config.resource_ubigeo["path"]),
        config.resource_ubigeo["index"])

    logger.info("Obtaining the data from ubigeos")

    data_list = get_info_from_ubigeo_list(ubigeo_list=ubigeo_list)

    data_processed = [
        process_data_to_tables(
            ubigeo_data,
            config.tables,
            config.keys) for ubigeo_data in data_list]

    logger.debug(data_processed)

    logger.info("Saving to csv file")
    save_to_json_file({
        "header": {
            "tables": config.tables,
            "keys": config.keys
        },
        "data": data_processed}, Path(foldername, DEFAULT_JSON_FILE_NAME))

    logger.info("Connecting to sqlite db")
    conn = connect(Path(foldername, DEFAULT_SQLITE_FILE_NAME))

    logger.info("Reseting tables")
    reset_results_tables(conn, config.tables, config.keys)

    logger.info("Inserting data in database")
    for i, data_ubigeo in enumerate(data_processed):
        logger.info(f"Inserting from ubigeo {data_ubigeo['ubigeo']} "
                    f"[{i+1}/{len(data_processed)}]")
        insert_results_values(conn, config.tables, config.keys,
                              data_ubigeo)

    logger.info("Process finished")
