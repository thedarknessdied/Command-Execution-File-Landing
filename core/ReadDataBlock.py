# -*- coding: utf-8 -*-


class ProcessBlockItem(object):
    def __init__(self, index: int, data: any):
        self.__index: int = index
        self.__data: any = data
        self.__next: ProcessBlockItem or None = None

    def set_data(self, data: any):
        self.__data = data

    def get_data(self):
        return self.__data

    def get_next(self):
        return self.__next

    def set_next(self, node):
        self.__next = node

    def get_index(self):
        return self.__index


class ProcessBlockList(object):
    def __init__(self, max_size: int = 100):
        self.__size: int = 0
        self.__total_size: int = max_size
        self.__head: ProcessBlockItem or None = None

    def get_size(self) -> int:
        return self.__size

    def inc_size(self):
        self.__size += 1

    def dec_size(self):
        self.__size -= 1

    def get_total_size(self) -> int:
        return self.__total_size

    def get_head(self) -> ProcessBlockItem or None:
        return self.__head

    def empty(self) -> bool:
        return self.get_size() == 0

    def full(self) -> bool:
        return self.get_size() == self.get_total_size()

    def show(self):
        cur: ProcessBlockItem or None = self.get_head()
        while cur is not None:
            print(cur.get_data())
            cur = cur.get_next()

    # 尾增
    def insert(self, value: any) -> bool:
        if self.full():
            return False

        node: ProcessBlockItem = ProcessBlockItem(index=self.get_size(), data=value)
        if self.empty():
            self.__head = node
            self.inc_size()
            return True

        cur: ProcessBlockItem or None = self.get_head()
        while cur.get_next() is not None:
            cur = cur.get_next()
        cur.set_next(node)
        self.inc_size()
        return True

    def delete(self, index: int) -> (bool, any):
        if self.empty():
            return False, None
        if index == 0:
            tmp: ProcessBlockItem = self.__head
            data = tmp.get_data()
            self.__head = self.__head.next
            self.dec_size()
            del tmp
            return True, data
        else:
            pre: ProcessBlockItem or None = None
            cur: ProcessBlockItem = self.get_head()
            while cur is not None and cur.get_index() != index:
                pre = cur
                cur = cur.get_next()
            if cur is None:
                return False, None

            pre.set_next(cur.get_next())
            tmp: ProcessBlockItem = cur
            data = tmp.get_data()
            del tmp
            return True, data

    def select(self, index: int) -> (bool, ProcessBlockItem or None):
        if self.empty() or index >= self.get_size():
            return False, None
        if index == 0:
            return self.get_head()
        cur: ProcessBlockItem = self.get_head()
        while cur is not None and cur.get_index() != index:
            cur = cur.get_next()
        if cur is None:
            return False, None
        return True, cur

    def update(self, index: int, data: any) -> bool:
        res, obj = self.select(index)
        if not res:
            return res
        obj.set_data(data)
        return True
