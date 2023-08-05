class BaseProgression:
    """prog_work.base_progression.BaseProgression(object)
    Parent class for arithmetical and geometrical progression
    attributes:
        _value - value that __next__ returns
        _first - the first term of the progression
        step - the step of the progression
    methods:
        __init__
        __next__
        __getitem__
        getitem
        sum"""

    def __init__(self, first, step):
        """BaseProgression.__init__
            :param first - first term of the progression
            :param step - step of the progression"""
        if type(first) not in [int, float]:
            raise TypeError(f'term of progression should be int or float, not {type(first)}')
        self._value = first
        self._first = first
        if type(step) not in [int, float]:
            raise TypeError(f'step of progression should be int or float, not {type(step)}')
        if not step:
            raise ValueError(f'step of progression should not be equal to 0')
        self.step = step

    def __next__(self):
        return

    def __getitem__(self, item):
        """BaseProgression.__getitem__
        :param item - serial of number (or slice) of the term of the progression, indexing starts with 0
        :returns a term (list of terms if item is slice) of the progression (float)"""
        if type(item) not in [int, slice]:
            raise TypeError(f'serial number of progression\'s should be int, not {type(item)}')
        if type(item) == slice:
            result = []
            if not item.stop:
                raise ValueError('progression has no ending')
            start = item.start if item.start else 1
            stop = item.stop
            step = item.step if item.step else 1
            print(start, stop, step)
            for i in range(start, stop, step):
                if i < 0:
                    raise ValueError('serial number of progression\'s term should not be negative')
                result.append(self[i])
            return result

    def getitem(self, item):
        """BaseProgression.__getitem__
        :param item - serial of number (or slice) of the term of the progression, indexing starts with 1
        :returns a term (list of terms if item is slice) of the progression (float)"""

        if type(item) not in [int, slice]:
            raise TypeError(f'serial number of progression\'s should be int, not {type(item)}')
        if type(item) == slice:
            result = []
            if not item.stop:
                raise ValueError('progression has no ending')
            start = item.start if item.start else 1
            stop = item.stop
            step = item.step if item.step else 1
            print(start, stop, step)
            for i in range(start, stop, step):
                if i <= 0:
                    raise ValueError('serial number of progression\'s term should be positive')
                result.append(self.getitem(i))
            return result

    def sum(self, amount):
        """BaseProgression.sum
        :param amount - the amount of terms of the progression to sum
        :returns the sum of the first <amount> terms of the progression"""
        if type(amount) != int:
            raise TypeError(f'the amount of terms should be int, not {type(amount)}')
        if amount <= 0:
            raise ValueError(f'the amount of terms should be positive')

