# -*- coding: utf-8 -*-
from utils import Utils


class Task(object):
    def __init__(
            self,
            config_filename: str = "settings.py",
    ):
        # 工具类
        self.__utils = Utils(self, config_filename)

        # 初始化文件系统
        self.init_filesystem()

        self.__src_data_file = self.get_utils().get_settings_item(
            self.get_utils().get_running_settings,
            "INPUT_FILENAME"
        )
        self.__dst_data_file = self.get_utils().get_settings_item(
            self.get_utils().get_running_settings,
            "OUTPUT_FILENAME"
        )

        self.__src_data_file, self.__dst_data_file = self.init_file(
            self.__src_data_file,
            self.__dst_data_file
        )

        self.__src_filename = self._set_src_filename()
        self.__tools = dict()
        self.init_tools()

    def get_utils(self):
        return self.__utils

    def get_src_data_file(self):
        return self.__src_data_file

    def get_src_filename(self):
        return self.__src_filename

    def get_dst_data_file(self):
        return self.__dst_data_file

    def get_tools(self) -> dict:
        return self.__tools

    def _set_src_filename(self):
        tmp_path = self.get_src_data_file().replace("\\", "/")
        return tmp_path[tmp_path.rfind("/") + 1:]

    def get_folders_settings(self) -> dict:
        return self.get_utils().get_folder_system().get_folder_settings()

    def get_running_settings(self) -> dict:
        return self.get_utils().get_running_settings()

    def get_folder_item(self, key: str) -> str:
        return self.get_folders_settings().get(key)

    def get_running_item(self, key: str) -> str:
        return self.get_running_settings().get(key)

    def init_filesystem(self):
        folders = self.get_folders_settings().values()
        for item in folders:
            self.get_utils().get_file_system().check_path_exist(
                item,
                is_file=False,
                is_create=True
            )

    def init_base_file(
            self,
            path: str,
            is_create: bool = False,
            is_file: bool = True
    ):
        _path = self.get_utils().get_file_system().check_path_exist(
            path,
            is_file=is_file,
            is_create=is_create,
        )
        if _path is None or not _path:
            raise FileNotFoundError()
        return _path

    def init_file(self, path: str, out_path: str):
        _path = self.init_base_file(
            f"{self.get_folder_item('INPUT_FILE_FOLDER')}/{path}",
            is_file=True
        )

        _out_path = self.get_utils().get_file_system().check_path_exist(
            f"{self.get_folder_item('OUTPUT_FILE_FOLDER')}/{out_path}",
            is_file=True,
            is_create=True
        )
        return _path, _out_path

    def init_tool(self, item: str):
        _file_suffix = "FILE_FOLDER"
        _list_suffix = "LIST"
        _entry_suffix = "ENTER_FUNCTION"
        _result = list()

        for func in self.get_running_settings().get(f"{item}_{_list_suffix}"):
            _result.append(
                self.get_utils().get_func(
                    func,
                    self.get_folder_item(f"{item}_{_file_suffix}"),
                    self.get_utils().get_running_settings().get("ENTER_FUNCTION").get(f"{item}_{_entry_suffix}")
                )
            )

        self.__tools.setdefault(
            self.get_folder_item(f"{item}_{_file_suffix}"),
            _result
        )

    def init_tools(self):
        self.init_tool("TAMPER")
        self.init_tool("MODULE")

    def run(self, *args, **kwargs):
        data = self.get_utils().run(
            self.get_running_settings().get("READ_FUNCTION"),
            *args, **kwargs
        )

        with open(self.get_dst_data_file(), "w") as f:
            f.write(data)
