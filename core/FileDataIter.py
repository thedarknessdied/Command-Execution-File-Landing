from core.ReadDataIter import ReadDataIter


class FileDataIter(object):
    def __init__(self, utils):
        self.__utils = utils

        self.__process_size_random_enable = self.get_file_settings_item("RANDOM_PROCESS_BLOCK_ENABLE")
        self.__process_size_editable_enable = self.get_file_settings_item("EDIT_PROCESS_BLOCK_ENABLE")
        self.__process_size = self.get_file_settings_item("MAX_PROCESS_BLOCK_SIZE")

        self.__tamper_list: list = list()
        self.__check_tamper: bool = False

        self.__data_iter = ReadDataIter()

    def get_process_size_editable_enable(self):
        return self.__process_size_editable_enable

    def get_tamper_list(self) -> list:
        return self.__tamper_list

    def get_check_tamper(self) -> bool:
        return self.__check_tamper

    def set_tamper_list(self, tamper_list: list):
        self.__tamper_list = tamper_list
        self.__check_tamper = self.check_need_process()

    def check_need_process(self) -> bool:
        return self.__tamper_list is not None and self.__tamper_list

    def insert(self, data: any, *args, **kwargs):
        if self.get_check_tamper():
            for tamper_func in self.get_tamper_list():
                data = tamper_func(data, *args, **kwargs)

        if self.get_process_size_editable_enable():
            read_sets = self.divide_process_data(data)
        else:
            read_sets = [data, ]

        self.get_data_iter().insert(read_sets)

    def get_utils(self):
        return self.__utils

    def get_data_iter(self):
        return self.__data_iter

    def get_file_settings_item(self, key: str) -> str:
        return self.get_utils().get_file_settings_item(key)

    def get_process_size_random_enable(self) -> any:
        return self.__process_size_random_enable

    def get_process_size(self) -> any:
        return self.__process_size

    def get_max_block_size(self, func):
        _res = func()
        if _res is None or not _res or not isinstance(_res, int) or _res <= 0:
            _res = 1024

        if self.get_process_size_random_enable():
            return self.get_utils().get_random_system().get_random_number(
                start=1, end=_res
            )
        else:
            return _res

    def get_max_process_block_size(self):
        return self.get_max_block_size(self.get_process_size)

    @classmethod
    def divide_data(cls, data: bytes, func):
        _result = list()
        start = 0
        data_length = len(data)
        while data_length >= func():
            _result.append(data[start: start + func()])
            data_length -= func()
            start += func()
        if data_length != 0:
            _result.append(data[start: start + data_length])
        return _result

    def divide_process_data(self, data: bytes):
        return self.divide_data(data, self.get_max_process_block_size)
