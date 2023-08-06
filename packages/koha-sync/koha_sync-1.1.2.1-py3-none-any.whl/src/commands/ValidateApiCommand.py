import pprint

from loguru import logger

from src.commands.BaseCommand import BaseCommand
from src.core.Config import Config

import requests
import sys


class ValidateApiCommand(BaseCommand):

    def __init__(self):
        self.add_koha = 'api/koha'
        self.headers = {
            "Accept": "application/json"
        }

    def execute(self):

        logger.info("VALIDATING API AVAILABILITY")

        try:
            status_req = requests.post(f"{Config.config['target']['url_add']}/{self.add_koha}", headers=self.headers)
        except Exception as e:
            sys.exit(logger.error(f"There was an error for request  : {e.args}"))

        if status_req.status_code != 401:
            sys.exit(logger.error(f"API {Config.config['target']['url_add']}/{self.add_koha} "
                                  f"status code {status_req.status_code}"))

        else:
            logger.success(f"API available")
