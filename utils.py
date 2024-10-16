# -*- coding: utf-8 -*-
import importlib
from core.ReadFileSystem import ReadSystem
from core.RandomSystem import RandomSystem
from core.LogSystem import LogSystem
from core.ParseConfig import ParseConfig
from core.FolderSystem import FolderSystem
from core.FileDataIter import FileDataIter
from core.ReadDataBlock import ProcessBlockList


class Utils(object):
    MAX_STRING_LENGTH = 10

    def __init__(
            self,
            factory,
            config_filename: str = "settings.py"
    ):
        # 配置信息解析类
        self.__setting_system = ParseConfig(config_filename)

        # 文件夹处理
        self.__folder_system = FolderSystem(self)

        # 元类
        self.__factory = factory

        # 随机内容工具初始化
        self.__random_system = RandomSystem(self)

        # file_system.run 只需要提供read的脚本和文件的路径作为做基础的参数就可以运行读取文件
        self.__file_system = ReadSystem(self)

        # 日志系统
        self.__logger_system = LogSystem(self)

        # 文件内容分区工具
        self._file_data_iter = FileDataIter(self)

    def get_setting_system(self) -> ParseConfig:
        return self.__setting_system

    def get_system_settings(self) -> dict:
        return self.get_setting_system().get_system_settings()

    def get_system_settings_item(self, key: str) -> dict or str:
        return self.get_setting_system().get_system_settings_item(key)

    def get_running_settings(self) -> dict:
        return self.get_setting_system().get_running_settings()

    def get_running_settings_item(self, key: str) -> list or dict or str:
        return self.get_setting_system().get_running_settings_item(key)

    def get_random_system(self) -> RandomSystem:
        return self.__random_system

    def get_random_settings(self) -> dict:
        return self.get_random_system().get_random_settings()

    def get_random_settings_item(self, key: str) -> any:
        return self.get_random_system().get_random_settings_item(key)

    def get_file_system(self) -> ReadSystem:
        return self.__file_system

    def get_file_settings(self) -> dict:
        return self.get_file_system().get_file_settings()

    def get_file_settings_item(self, key: str) -> any:
        return self.get_file_system().get_file_settings_item(key)

    def get_folder_system(self) -> FolderSystem:
        return self.__folder_system

    def get_folder_settings(self) -> dict:
        return self.get_folder_system().get_folder_settings()

    def get_folder_settings_item(self, key: str) -> any:
        return self.get_folder_system().get_folder_settings_item(key)

    def get_logger_system(self):
        return self.__logger_system

    def get_logger_settings(self) -> dict:
        return self.get_logger_system().get_logger_settings()

    def get_logger_settings_item(self, key: str) -> any:
        return self.get_logger_system().get_logger_settings_item(key)

    def get_factory(self):
        return self.__factory

    @classmethod
    def get_settings_item(cls, callback, key: str) -> str or dict:
        return callback().get(key)

    def check_name_exist(self, name: str) -> bool:
        return name in self.__dict__.keys()

    def register_get_settings_item(self, func_name: str, func):
        if not self.check_name_exist(func_name):
            setattr(self, func_name, func)
        else:
            raise RuntimeError()

    @classmethod
    def get_func_class(cls, func_obj: str) -> any:
        return importlib.import_module(func_obj)

    def get_func_content(self, func_obj: str, func_name: str) -> any:
        return self.get_func_class(func_obj).__dict__.get(func_name, None)

    def get_func(self, func_name: str, func_path: str, func_entry: str) -> any:
        _func_name = f"{func_name}.{self.get_settings_item(self.get_system_settings, 'DEFAULT_FUNC_SUFFIX')}"
        _path = self.__file_system.check_path_exist(f"{func_path}/{_func_name}", is_file=True)
        if _path is None or not _path:
            raise FileNotFoundError()
        return self.get_func_content(f"{func_path}.{func_name}", func_entry)

    def get_data(self, read_method, path: str, *args, **kwargs):
        for data in self.get_file_system().run(
                task_name=read_method,
                path=path,
                utils=self,
                *args, **kwargs
        ):
            self.get_file_data_iter().insert(data)

    def get_file_data_iter(self):
        return self._file_data_iter

    def run(self, read_method: str, *args, **kwargs):
        _result = ""

        _tmp = self.get_factory().get_tools().get(
            self.get_folder_settings_item("TAMPER_FILE_FOLDER")
        )

        if _tmp is None or not _tmp or not isinstance(_tmp, list):
            _tmp = list()

        self.get_file_data_iter().set_tamper_list(_tmp)

        self.get_data(
            read_method,
            self.__factory.get_src_data_file(),
            *args, **kwargs
        )

        # print(self.get_file_data_iter().get_data_iter().get_data()["0"].get_size())
        # cur_list: ProcessBlockList = self.get_file_data_iter().get_data_iter().get_data()["0"]
        # cur_node = cur_list.get_head()
        # while cur_node is not None:
        #     print(cur_node.get_data(), end="")
        #     cur_node = cur_node.get_next()

        for key, data_lists in self.get_file_data_iter().get_data_iter().get_data().items():
            _tmp_result = ""
            for module_func in self.__factory.get_tools().get(
                    self.get_folder_settings_item("MODULE_FILE_FOLDER")
            ):
                cur_list: ProcessBlockList = data_lists
                cur_node = cur_list.get_head()
                while cur_node is not None:
                    if cur_node.get_next() is None:
                        _tmp_result += module_func(cur_node.get_data(), self, end=True, *args, **kwargs)
                    else:
                        _tmp_result += module_func(cur_node.get_data(), self, end=False, *args, **kwargs)
                    cur_node = cur_node.get_next()
            _result += _tmp_result

        return _result

    def divide_data(self, data: str):
        max_process_block_size = self.get_file_settings_item("MAX_PROCESS_BLOCK_SIZE")
        _result = list()
        start = 0
        data_length = len(data)
        while data_length >= max_process_block_size:
            _result.append(data[start: start + max_process_block_size])
            data_length -= max_process_block_size
            start += max_process_block_size
        if data_length != 0:
            _result.append(data[start: start + data_length])
        return _result
