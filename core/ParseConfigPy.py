# -*- coding: utf-8 -*-
import importlib


class ParseConfigPy(object):
    def __init__(self, filename: str, *args, **kwargs):
        self.__settings = self.set_settings(filename)

    @classmethod
    def set_settings(cls, filename: str) -> dict:
        module = importlib.import_module(filename.split(".")[0])
        if "SETTINGS" in dir(module):
            return module.SETTINGS
        else:
            return dict()

    def refresh_settings(self, filename: str):
        self.__settings = self.set_settings(filename)

    def get_settings(self) -> dict:
        return self.__settings
