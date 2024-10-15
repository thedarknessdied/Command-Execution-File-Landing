# -*- coding: utf-8 -*-
from core.FileSystem import FileSystem


class ReadSystem(FileSystem):
    def __init__(self, utils):
        super().__init__(utils)

        self.__read_folder = self.ret_abs_path(
            self.get_utils().get_folder_system().get_read_file_folder()
        )

        self.__read_function_entry = None

        self.__read_function_entry_start = None

        self.init_reader_system()

        self.__read_methods = self._ret_all_read_file_method()

    def get_read_folder(self) -> str:
        return self.__read_folder

    def get_read_function_entry(self) -> str:
        return self.__read_function_entry

    def get_read_function_entry_start(self) -> str:
        return self.__read_function_entry_start

    def init_reader_system(self):
        self.__read_function_entry = self.get_utils().get_settings_item(
            self.get_utils().get_running_settings,
            "ENTER_FUNCTION"
        ).get("READ_ENTER_FUNCTION")

        self.__read_function_entry_start = self.get_utils().get_settings_item(
            self.get_utils().get_running_settings,
            "START_SIGNAL"
        ).get("READ_ENTER_FUNCTION_START")

        self.init_read_method()

    def get_read_methods(self) -> dict:
        return self.__read_methods

    def init_read_method(self):
        for filename in self.get_sub_file_object(
                self.get_read_folder()
        ):
            if not filename.startswith("_"):
                if filename.endswith(
                        self.get_utils().get_settings_item(self.get_utils().get_system_settings, "DEFAULT_FUNC_SUFFIX")
                ):
                    module_name = filename[:filename.find(".")]
                    module_function = self.get_utils().get_func_content(
                        f"{self.get_read_function_entry()}.{module_name}",
                        f"{self.get_read_function_entry()}"

                    )
                    if module_name not in ReadSystem.__dict__.keys():
                        setattr(
                            ReadSystem,
                            f"{self.get_read_function_entry_start()}_{module_name}",
                            module_function
                        )

    def _ret_all_read_file_method(self) -> dict:
        _result = dict()
        for func_name, func_content in ReadSystem.__dict__.items():
            if func_name is not None and func_name:
                if isinstance(func_name, str):
                    if func_name.startswith(self.get_read_function_entry_start()):
                        if _result.get(func_name, None) is None:
                            _result.setdefault(func_name, func_content)
                        else:
                            _result[func_name] = func_content
        return _result

    def _ret_read_file_method(self, name: str) -> tuple:
        _task_name = f"{self.get_read_function_entry_start()}_{name}"
        if _task_name in self.get_read_methods().keys():
            return _task_name, self.get_read_methods().get(_task_name)
        return _task_name, None

    def run(self, task_name: str, *args, **kwargs):
        method_name, method = self._ret_read_file_method(task_name)
        if method is None or not method:
            raise ValueError()
        return method(*args, **kwargs)
