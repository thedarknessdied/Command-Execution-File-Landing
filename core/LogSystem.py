# -*- coding: utf-8 -*-
from datetime import datetime
import logging


class LogSystem(object):
    CONFIG_NAME = "LOGGER"

    def __init__(self, utils):
        self.__utils = utils

        self.__logger = None

        self.__logger_settings = self.init_logger_settings()

        self.__logger_suffix = self.get_logger_settings_item("DEFAULT_LOG_SUFFIX")
        self.__log_level = logging.getLevelName(self.get_logger_settings_item("LOG_LEVEL"))
        self.__logger_filename = self.get_random_log_name()
        self.__file_handler = None
        self.__console_handler = None
        self.__log_fmt = None
        self.init()

    def get_log_fmt(self):
        return self.__log_fmt

    def get_utils(self):
        return self.__utils

    def get_logger(self):
        return self.__logger

    def get_logger_suffix(self):
        return self.__logger_suffix

    def get_logger_filename(self):
        return self.__logger_filename

    def get_logger_settings(self) -> dict:
        return self.__logger_settings

    def get_logger_settings_item(self, key: str) -> any:
        return self.get_logger_settings().get(key, None)

    def get_log_level(self):
        return self.__log_level

    def init_logger_settings(self) -> dict:
        _settings = self.get_utils().get_settings_item(
            self.get_utils().get_system_settings,
            self.CONFIG_NAME
        )

        if _settings is not None and _settings and isinstance(_settings, dict):
            return _settings
        raise ValueError()

    def _get_random_log_name(self):
        return datetime.now().strftime(self.get_logger_settings_item("LOG_NAME_FORMAT"))

    def get_random_log_name(self):
        return f"{self._get_random_log_name()}.{self.get_logger_suffix()}"

    def get_logger_message_fmt(self):
        return logging.Formatter(self.get_logger_settings_item("MES_FORMAT"))

    def init(self):
        self.__logger = logging.getLogger(self._get_random_log_name())
        self.__logger.setLevel(self.get_log_level())

        self.__log_fmt = self.get_logger_message_fmt()

        _folder = self.get_utils().get_folder_settings_item("LOG_FILE_FOLDER")
        _path = self.get_utils().get_file_system().check_path_exist(
            f"{_folder}/{self.get_logger_filename()}",
            is_file=True,
            is_create=True
        )
        self.__file_handler = logging.FileHandler(_path)
        self.set_file_handler_level()
        self.set_file_handler_msg_format()

        self.__console_handler = logging.StreamHandler()
        self.set_console_handler_level()
        self.set_file_handler_msg_format()

        self.__logger.addHandler(self.__file_handler)
        self.__logger.addHandler(self.__console_handler)

    def get_file_handler(self):
        return self.__file_handler

    def get_console_handler(self):
        return self.__console_handler

    def _set_logger_level(self, obj):
        obj.setLevel(self.get_log_level())

    def set_file_handler_level(self):
        self._set_logger_level(self.get_file_handler())

    def set_console_handler_level(self):
        self._set_logger_level(self.get_console_handler())

    def _set_logger_msg_format(self, handler):
        handler.setFormatter(self.get_log_fmt())

    def set_file_handler_msg_format(self):
        self._set_logger_msg_format(self.get_file_handler())

    def set_console__msg_format(self):
        self._set_logger_msg_format(self.get_console_handler())

    def warn(self, mes):
        self.get_logger().warning(mes)

    def debug(self, mes):
        self.get_logger().debug(mes)

    def info(self, mes):
        self.get_logger().info(mes)

    def error(self, mes):
        self. get_logger().error(mes)

    def mes(self, mes):
        self. get_logger().mes(mes)
