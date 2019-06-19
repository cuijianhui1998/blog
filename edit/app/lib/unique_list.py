

class UniqueList():
    '''
    创建了一个简单的无重复列表,用来存储在查询时能够去除掉重复的元素,
    并且按照我插入的顺序排序
    '''
    def __init__(self):
        self._list = []

    def extend(self,iterable):
        for i in iterable:
            if i not in self._list:
                self._list.append(i)

    def append(self,key):
        if key not in self._list:
            self._list.append(key)

    def __getitem__(self, item):
         return self._list[item]



