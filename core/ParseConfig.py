# -*- coding: utf-8 -*-
import os
import re
from core.ParseConfigPy import ParseConfigPy


class BasicParseConfig(object):
    __config_suffix = ["py", "xml"]
    __config_parse_class = {
        "py": ParseConfigPy
    }

    def __init__(self, filename: str = "settings.py"):
        self.__config_file_type = ""
        self.__config_abs_filename, self.__config_filename = self.get_valid_config_file(filename)
        self.__config_parser = self.__config_parse_class.get(
            self.__config_file_type
        )(self.__config_filename)

    def get_config_parser(self):
        return self.__config_parser

    def get_config_filename(self):
        return self.__config_filename

    def get_config_suffix(self) -> list:
        # 提供对外的获取解析文件后缀的接口
        return self.__config_suffix

    def check_config_suffix_valid(self, suffix: str) -> bool:
        # 判断文件后缀是否是合法的
        return suffix in self.get_config_suffix()

    @classmethod
    def ret_filename_model(cls):
        return re.compile("^[0-9a-zA-Z\.]{1,}$", re.I)

    def check_suffix_valid(self, filename: str) -> bool:
        model = self.ret_filename_model()
        if model.match(filename) is None:
            return False
        filename_list = filename.split(".")
        if len(filename_list) != 2:
            return False
        _res = self.check_config_suffix_valid(filename_list[-1])
        if _res:
            self.__config_file_type = filename_list[-1]
            return True
        else:
            return False

    def get_valid_config_file(self, filename: str) -> tuple:
        if not os.path.exists(filename):
            return "", ""
        if not os.path.isabs(filename):
            _filename = os.path.abspath(
                os.path.join(
                    os.getcwd(),
                    filename
                )
            )
        else:
            _filename = filename
        if not os.path.isfile(_filename):
            return "", ""
        _filename = _filename.replace("\\", "/")
        _file: list = _filename.split("/")
        if not self.check_suffix_valid(_file[-1]):
            return "", ""
        return _filename, _file[-1]


class ParseConfig(BasicParseConfig):
    BASIC_SYSTEM_SETTINGS = "SYSTEM"
    BASIC_RUNNING_SETTINGS = "RUNNING"
    BASIC_SETTINGS = [
        BASIC_SYSTEM_SETTINGS,
        BASIC_RUNNING_SETTINGS
    ]

    def __init__(self, filename: str = "settings.py"):
        super().__init__(filename)

        self.__settings = None

    def init(self):
        _settings = self.get_config_dict()
        if _settings is None or not _settings or not isinstance(_settings, dict):
            raise TypeError()
        if not self.check_key_valid(_settings):
            raise KeyError()

        self.__settings = _settings

    def check_key_valid(self, settings:dict) -> bool:
        for item in self.BASIC_SETTINGS:
            if item not in settings.keys():
                return False
        return True

    def get_settings(self) -> dict:
        return self.__settings

    def get_config_dict(self) -> dict:
        return self.get_config_parser().get_settings()

    def get_config_item(self, key: str) -> str or dict:
        return self.get_config_dict().get(key)

    def get_system_settings(self) -> dict:
        return self.get_config_item(self.BASIC_SYSTEM_SETTINGS)

    def get_running_settings(self) -> dict:
        return self.get_config_item(self.BASIC_RUNNING_SETTINGS)

    def get_system_settings_item(self, key: str) -> dict or str:
        return self.get_system_settings().get(key)

    def get_running_settings_item(self, key: str) -> dict:
        return self.get_running_settings().get(key)
