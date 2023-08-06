from loguru import logger
from tqdm import tqdm

import pprint
import time
import requests
import sys

from src.commands.BaseCommand import BaseCommand
from src.commands.LoadConfigFileCommand import LoadConfigFileCommand
from src.core import SqlSentences
from src.core.DBPool import DBPool
from src.core.Config import Config


class SyncKohaRowsCommand(BaseCommand):

    def __init__(self):
        self.add = 'api/koha'

    def execute(self):
        logger.info("STARTING SYNCHRONIZATION LOOP")

        try:
            with DBPool.get_connection(True).cursor() as cursor:

                last_record = LoadConfigFileCommand.get_last_record()
                cursor.execute(SqlSentences.get_sql_sentence(Config.config["target"]["account_id"], last_record,
                                                             Config.config["target"]["block"]))
                records = cursor.fetchall()

                if not records:
                    logger.info("There aren't new records to synchronize. Bypassing excecution")
                    time.sleep(10)
                    return

                with tqdm(total=len(records), desc="SYNCHRONIZING ROWS") as progress_bar:
                    for record in records:
                        progress_bar.update(100 / len(records))
                        for key in record:
                            if key != "tr_datetime":
                                record[key] = SyncKohaRowsCommand.sanitize(record[key])

                post_rows_req = requests.post(f"{Config.config['target']['url_add']}/{self.add}",
                                              json={
                                                  "llave": Config.config['target']['key'],
                                                  "secreto": Config.config['target']['secret'],
                                                  "docs": records
                                              })

                if post_rows_req.status_code is not 200:
                    logger.warning(f"Request status was not 200 : {post_rows_req}")

                # write last synchronized record date without timezone
                LoadConfigFileCommand.set_last_record(records[-1]['tr_datetime'].split("+")[0])
                logger.success(f"Koha records synchronized {post_rows_req.json()}")

        except Exception as e:
            logger.exception(e)
            sys.exit(logger.error(f"There was an error while synchronizing records : {e.args}"))

    """ lower case and remove noise characters """
    @staticmethod
    def sanitize(value):
        chars_to_remove = [';', ':', '/', '.', ',', '(', ')', '-', '_']
        if isinstance(value, str):
            value = value.lower()
            value = value.translate({ord(char): '' for char in chars_to_remove})
            value = ' '.join(value.split())
        return value
