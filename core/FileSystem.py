# -*- coding: utf-8 -*-
import os


class FileSystem(object):
    CONFIG_NAME = "FILE_SYSTEM"

    def __init__(self, utils):
        self.__utils = utils
        self.__file_settings = self.init_file_settings()

        self.init()

    def init(self):
        for key, value in self.get_file_settings().items():
            _key = f"__{key}"
            if _key not in dir(self):
                setattr(self, _key, value)

    def get_utils(self):
        return self.__utils

    def get_file_settings(self) -> dict:
        return self.__file_settings

    def get_file_settings_item(self, key: str) -> any:
        return self.get_file_settings().get(key, None)

    def init_file_settings(self) -> dict:
        _settings = self.get_utils().get_settings_item(
            self.get_utils().get_system_settings,
            self.CONFIG_NAME
        )

        if _settings is not None and _settings and isinstance(_settings, dict):
            return _settings
        raise ValueError()

    def get_class_item(self, item: str) -> any:
        _item = f"__{item}"
        if _item in dir(self):
            return getattr(self, _item)
        else:
            return ""

    @classmethod
    def _check_path_exist(cls, path: str) -> bool:
        return os.path.exists(path)

    def check_abs_path_exist(self, path: str) -> bool:
        return self._check_path_exist(self._ret_abs_path(path))

    @classmethod
    def _ret_abs_path(cls, path: str) -> str:
        return path if os.path.isabs(path) else os.path.abspath(os.path.join(os.getcwd(), path))

    def ret_abs_path(self, path: str) -> str:
        return self._ret_abs_path(path)

    def _create_file(self, file_path: str):
        if self.check_path_writable(file_path):
            with open(file_path, mode="w") as f:
                f.write(self.get_random_content())
        else:
            raise PermissionError()

    def _create_folder(self, folder_path: str):
        if self.check_path_writable(folder_path):
            os.makedirs(folder_path)
        else:
            raise PermissionError()

    def check_path_exist(self, path: str, is_create: bool = False, is_file: bool = True) -> str:
        path = self._ret_abs_path(path)
        if self._check_path_exist(path):
            if os.path.isfile(path) and is_file:
                return path
            elif not os.path.isfile(path) and not is_file:
                return path
        if is_create:
            if is_file:
                self._create_file(path)
            else:
                self._create_folder(path)
            return path
        return ""

    @classmethod
    def _ret_file_stat(cls, path: str):
        return os.stat(path)

    def _check_file_access(self, path: str, access: int) -> bool:
        path = self._ret_abs_path(path)
        path = os.path.dirname(path)

        if self._check_path_exist(path):
            if os.access(path, access):
                return True
        return False

    def check_file_readable(self, path: str) -> bool:
        return self._check_file_access(path, os.R_OK)

    def check_path_writable(self, path: str) -> bool:
        return self._check_file_access(path, os.W_OK)

    def check_file_executable(self, path: str) -> bool:
        return self._check_file_access(path, os.X_OK)

    def get_random_content(self) -> str:
        _result = ""
        if self.get_class_item("DEFAULT_CONTENT_ENABLE"):
            size = self.get_class_item("DEFAULT_CONTENT_SIZE")
            if size > 0:
                _result = self.__utils.get_random_system().get_random_string(size)
        return _result

    @classmethod
    def get_sub_file_object(cls, folder_name: str):
        for filename in os.listdir(folder_name):
            if filename is not None and filename and isinstance(filename, str):
                yield filename
            else:
                continue
