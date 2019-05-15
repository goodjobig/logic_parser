class IICDataGroup:
    __slots__ = ('_index', 'data', '_data_list', '_inited', '_wr_mode', '_addr')

    @staticmethod
    def is_hex(value):
        assert isinstance(value, str) and value.startswith('0x') and int(value, 16) < 256, " The value must be of type char in c "

    def __init__(self):
        self._index = 0
        self._data_list = []
        self._inited = False
        self._wr_mode = None
        self._addr = None

    def __iter__(self):
        return iter(self._data_list)

    def __len__(self):
        return len(self._data_list)

    def __str__(self):
        return "<obj DataGroup instance>  addr= %s wr = %s" % (self.addr, 0)

    def append(self, value):
        if self.is_inited():
            self.is_hex(value)
            self._data_list.append(value)
        else:
            raise ValueError("你必须先初始化地址和读写模式")

    def is_inited(self):
        try:
            a = self._addr
            b = self._wr_mode
        except AttributeError:
            self._inited = False
        else:
            self._inited = True
        return self._inited

    def get_data(self):
        return self._data_list

    @property
    def addr(self):
        return self._addr

    @addr.setter
    def addr(self, value):
        self.is_hex(value)
        self._addr = value

    @property
    def wr_mode(self):
        return self._wr_mode

    @wr_mode.setter
    def wr_mode(self, value):
        assert value == 0 or value == 1
        self._wr_mode = value


class IICDataGroupList:
    def __init__(self):
        self._index = 0
        self._group = []

    def append(self, value):
        assert isinstance(value, IICDataGroup), "append 的对象必须是 DataGroup 类型"
        self._group.append(value)

    def __iter__(self):
        return iter(self._group)

    def __len__(self):
        return len(self._group)

    def __getitem__(self, item):
        if isinstance(item, slice):
            self._group = self._group[item.start:item.stop:item.step]
            return self._group[item.start:item.stop:item.step]
        else:
            if item <= len(self._group):
                return self._group[item]
            else:
                raise KeyError("未找到你所要的值")

    def show(self):
        if len(self._group):
            for index, item in enumerate(self._group):
                print("index:%s addr:%s wr: %s data: %s" % (index, item.addr, item.wr_mode, item.get_data()))


class SPIDataGroup:
    pass


if __name__ == '__main__':
    dp = IICDataGroup()
    # dp.append('0x50')
    dp.addr = '0x50'
    dp.wr_mode = 0
    print(dp.is_inited())
    dp.append('0x15')
    dp.append('0xff')
    print(dp)


