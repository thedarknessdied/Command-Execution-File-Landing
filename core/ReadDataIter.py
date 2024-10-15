from core.ReadDataBlock import ProcessBlockList


class ReadDataIter(object):
    def __init__(self):
        self.__cur_index = 0
        self.__total_index = 0
        self.__data = dict()

    def get_data(self) -> dict:
        return self.__data

    def get_cur_index(self) -> int:
        return self.__cur_index

    def get_total_index(self) -> int:
        return self.__total_index

    def _increase_total_index(self):
        self.__total_index += 1

    def _increase_cur_index(self):
        self.__cur_index += 1

    def empty(self) -> bool:
        return self.get_total_index() == 0

    def end(self) -> bool:
        if self.get_total_index() == 0:
            return True
        return self.get_cur_index() == self.get_total_index()

    def insert(self, data: list):
        tmp = ProcessBlockList()
        for item in data:
            tmp.insert(item)
        self.get_data().setdefault(f"{self.get_total_index()}", tmp)
        self._increase_total_index()

    def __iter__(self):
        return self

    def __next__(self, *args, **kwargs):
        if self.empty():
            raise StopIteration
        if self.end():
            raise StopIteration
        _index = self.get_cur_index()
        self._increase_cur_index()
        data = self.get_data().get(f"{_index}")
        return data
