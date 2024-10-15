# -*- coding: utf-8 -*-
import random


class RandomSystem(object):
    CONFIG_NAME = "RANDOM_SYSTEM"

    def __init__(self, utils):
        self.__utils = utils
        self.__random_settings = self.init_random_settings()

        self.__normal_charset = ""
        self.__variable_charset = ""

        self.init()

    def init(self):
        for key, value in self.get_random_settings().items():
            _key = f"__{key}"
            if _key not in dir(self):
                setattr(self, _key, value)

        self.__normal_charset = self.combine_charset_settings(
            ["ASCII_LOWERCASE", "ASCII_UPPERCASE", "DIGITS", "UNDERLINE"]
        )
        self.__variable_charset = self.combine_charset_settings(
            ["ASCII_LOWERCASE", "ASCII_UPPERCASE", "UNDERLINE"]
        )

    def get_utils(self):
        return self.__utils

    def get_random_settings(self) -> dict:
        return self.__random_settings

    def get_random_settings_item(self, key: str) -> any:
        return self.get_random_settings().get(key, None)

    def get_normal_charset(self) -> str:
        return self.__normal_charset

    def get_variable_charset(self) -> str:
        return self.__variable_charset

    def init_random_settings(self) -> dict:
        _settings = self.get_utils().get_settings_item(
            self.get_utils().get_system_settings,
            self.CONFIG_NAME
        )

        if _settings is not None and _settings and isinstance(_settings, dict):
            return _settings
        raise ValueError()

    def combine_charset_settings(self, charsets: list) -> str:
        _result = ""
        for item in charsets:
            _tmp_result = self.get_class_item(item)
            if _tmp_result is not None and _tmp_result and isinstance(_tmp_result, str):
                _result += _tmp_result
        return _result

    def get_class_item(self, item: str) -> any:
        _item = f"__{item}"
        if _item in dir(self):
            return getattr(self, _item)
        else:
            return ""

    @classmethod
    def get_random_number(cls, start: int, end: int) -> int:
        return random.randint(start, end)

    def _get_random_char(self, charset: str) -> str:
        return charset[self.get_random_number(0, len(charset) - 1)]

    def get_random_string(self, length: int = 1):
        _start = self.get_class_item("MINIMUM_NUMBER_START")
        _offset = self.get_class_item("MAX_NUMBER_OFFSET")
        length = length if length > 0 else self.get_random_number(
            _start,
            _start + _offset
        )
        _result = ""
        for _ in range(length):
            _result += self._get_random_char(self.__normal_charset)
        return _result

    def get_random_variable(self, length: int = 1):
        _start = self.get_class_item("MINIMUM_NUMBER_START")
        _offset = self.get_class_item("MAX_NUMBER_OFFSET")
        length = length if length > 0 else self.get_random_number(
            _start,
            _start + _offset
        )
        _result = self._get_random_char(self.__variable_charset)
        _result += self.get_random_string(length - 1)
        return _result

    def get_random_filename(
            self,
            length: int = 1,
            pre_length: int = 0,
            suffix_length: int = 3
    ):
        _result = ""

        pre_length = pre_length if pre_length >= 0 else 0
        if pre_length != 0:
            _result += self.get_random_string(pre_length) + "_"
        _start = self.get_class_item("MINIMUM_NUMBER_START")
        _offset = self.get_class_item("MAX_NUMBER_OFFSET")
        length = length if length > 0 else self.get_random_number(
            _start,
            _start + _offset
        )
        _result += self.get_random_string(length)

        suffix_length = suffix_length if suffix_length >= 0 else 3
        if suffix_length != 0:
            _result += "." + self.get_random_string(suffix_length)

        return _result
