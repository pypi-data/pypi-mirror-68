import pprint
from datetime import datetime

from loguru import logger
from jsonschema import validate

from src.commands.BaseCommand import BaseCommand
from src.core.Config import Config

import os
import sys
import yaml


class LoadConfigFileCommand(BaseCommand):

    yml_schema = """
    type: object
    properties:
      testing:
        type: array
        items:
          enum:
            - this
            - is
            - a
            - test
    """

    def __init__(self, **kwargs):
        self.file_path = kwargs.get('file_path')
        self.file_content = None

    def execute(self):
        logger.info("VERIFYING AND LOADING CONFIG FILE")

        if not os.path.isfile(self.file_path):
            sys.exit(logger.error(f"Configuration file {self.file_path} does not exist"))
        else:
            logger.success("Configuration file exists")

            try:
                with open(self.file_path, mode='r+', encoding='utf-8') as config_file:
                    self.file_content = config_file.read()
                    logger.success("Configuration file is readable and writable")

            except IOError as e:
                sys.exit(logger.error(f"Configuration file {self.file_path} is not readable or writable : {e.args}"))

            try:
                self.file_content = yaml.load(self.file_content, Loader=yaml.FullLoader)
                validate(self.file_content, yaml.load(LoadConfigFileCommand.yml_schema, Loader=yaml.FullLoader))
                logger.success("Configuration file has valid syntax")

            except yaml.YAMLError as e:
                sys.exit(logger.error(f"Configuration file {self.file_path} has format errors : {e.args}"))

            if "db" not in self.file_content:
                sys.exit(logger.error("Configuration file has not : 'db"))
            else:
                logger.success("Configuration file has : 'db'")

                for key, value in Config.config['db'].items():

                    if key not in self.file_content['db']:
                        sys.exit(logger.error(f"Configuration file missing required attribute : [db][{key}]"))

                    else:
                        logger.success(f"Configuration file has required attribute : [db][{key}]")
                        if self.file_content['db'][key] is None:
                            sys.exit(logger.error(f"Configuration file has not value : [db][{key}]"))
                        else:
                            Config.config['db'][key] = self.file_content['db'][key]
                            logger.success(f"Configuration file has required value : [db][{key}]")

            if "target" not in self.file_content:
                sys.exit(logger.error("Configuration file has not : 'target"))
            else:
                logger.success("Configuration file has : 'target'")

                for key, value in Config.config['target'].items():

                    if key not in self.file_content['target']:
                        sys.exit(logger.error(f"Configuration file missing required attribute : [target][{key}]"))

                    else:
                        logger.success(f"Configuration file has required attribute : [target][{key}]")

                        if self.file_content['target'][key] is None:
                            sys.exit(logger.error(f"Configuration file has not value : [target][{key}]"))
                        else:
                            Config.config['target'][key] = self.file_content['target'][key]
                            logger.success(f"Configuration file has required value : [target][{key}] = "
                                           f"{self.file_content['target'][key]}")

        Config.path = self.file_path

    @staticmethod
    def get_last_record():
        try:
            if not LoadConfigFileCommand.is_state():
                logger.warning("CREATING STATE FIELD : There is not previous state")

                with open(Config.path, mode='a', encoding='utf-8') as config_file:
                    state = {
                        "last_record_date": datetime(1970, 1, 1),
                        "accessed_count": 0
                    }
                    yaml.dump({"state": state}, config_file)
                    return state["last_record_date"]

            else:
                with open(Config.path, mode='r', encoding='utf-8') as config_file:
                    return yaml.load(config_file, Loader=yaml.FullLoader)['state']['last_record_date']

        except IOError as e:
            sys.exit(logger.error(f"There was a problem while reading state : {e.args}"))

    @staticmethod
    def set_last_record(date):
        try:
            if LoadConfigFileCommand.is_state():

                with open(Config.path, mode='r', encoding='utf-8') as config_file:
                    config_file_content = yaml.load(config_file, Loader=yaml.FullLoader)
                    config_file_content['state']['last_record_date'] = date
                    config_file_content['state']['accessed_count'] = config_file_content['state']['accessed_count'] + 1

                with open(Config.path, mode='w', encoding='utf-8') as config_file:
                    logger.warning(f"UPDATING STATE FIELD : [last_record_date] {date}")
                    yaml.dump(config_file_content, config_file)

        except IOError as e:
            sys.exit(logger.error(f"There was a problem while setting state : {e.args}"))

    @staticmethod
    def is_state() -> bool:
        try:
            with open(Config.path, mode='r', encoding='utf-8') as config_file:
                config_file_content = yaml.load(config_file, Loader=yaml.FullLoader)
                if 'state' not in config_file_content:
                    return False
            return True
        except IOError as e:
            sys.exit(logger.error(f"There was a problem while validating state : {e.args}"))


