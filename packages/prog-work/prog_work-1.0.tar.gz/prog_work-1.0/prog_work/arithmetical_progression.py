"""prog_work.arithmetical_progression
this module is intended for work with arithmetical progression

Creation of arithmetical progression
    If you do know the first term of the progression and it's step,
    create the progression directly with ArithmeticalProgression.__init__
    If you have another information about the progression use arithmetical_progression to create it.
"""

from prog_work.base_progression import BaseProgression


class ArithmeticalProgression(BaseProgression):
    """prog_work.arithmetical_progression.ArithmeticalProgression(BaseProgression)
    the class for arithmetical progressions
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

    def __next__(self):
        result = self._value
        self._value += self.step
        return result

    def getitem(self, item):
        super(ArithmeticalProgression, self).getitem(item)
        if type(item) == int:
            if item <= 0:
                raise ValueError('serial number of progression\'s term should be positive')
            return self._first + (item - 1) * self.step

    def __getitem__(self, item):
        super(ArithmeticalProgression, self).__getitem__(item)
        if type(item) == int:
            if item < 0:
                raise ValueError('serial number of progression\'s term should not be negative')
            return self._first + item * self.step

    def sum(self, amount):
        super(ArithmeticalProgression, self).sum(amount)
        return (2 * self._first + (amount - 1) * self.step) / 2 * amount

    def __str__(self):
        first = int(self._first) if int(self._first) == self._first else self._first
        step = int(self.step) if int(self.step) == self.step else self.step
        return f'a[n] = {first}+({step})(n - 1)'

    def __repr__(self):
        return f'AP({self._first}, {self.step})'


def arithmetical_progression(**kwargs):
    """prog_work.arithmetical_progression.arithmetical_progression(**kwargs)
    To create a progression you need to pass two parameters such as:
        val{num}
        step
        sum{num}
    You can pass
        value and sum:
            ap = arithmetical_progression(val3=10, sum12=123)
        two values:
            ap = arithmetical_progression(val1=123, val123=4)
        two sums:
            ap = arithmetical_progression(sum30=228, sum3=2)
        value and step:
            ap = arithmetical_progression(val30=10, step=-3.5)
        sum and step:
            ap = arithmetical_progression(sum2=3.123, step=0.12)
    other parameters will raise an exception"""
    keys = list(kwargs.keys())
    length = len(keys)
    if length - 2:
        raise ValueError(f'The amount of parameters should be 2, not {length}')

    if 'val' in keys[0] and 'val' in keys[1]:
        for i in kwargs:
            if type(kwargs[i]) not in [int, float]:
                raise TypeError(f'term of progression should be int or float, not {type(kwargs[i])}')
        dig1 = int(keys[0].split('val')[1])
        dig2 = int(keys[1].split('val')[1])
        if dig1 > dig2:
            d = (kwargs[keys[0]] - kwargs[keys[1]]) / (dig1 - dig2)
        else:
            d = (kwargs[keys[1]] - kwargs[keys[0]]) / (dig2 - dig1)
        first = kwargs[keys[0]] - (dig1 - 1) * d
    elif ('val' in keys[0] or 'val' in keys[1]) and 'step' in keys:
        if type(kwargs['step']) not in [int, float]:
            raise TypeError(f'step of progression should be int or float, not {type(kwargs["step"])}')
        d = kwargs['step']
        if 'val' in keys[0]:
            if type(kwargs[keys[0]]) not in [int, float]:
                raise TypeError(f'term of progression should be int or float, not {type(kwargs[keys[0]])}')
            dig = int(keys[0].split('val')[1])
            first = kwargs[keys[0]] - (dig - 1) * d
        else:
            if kwargs[keys[1]] not in [int, float]:
                raise TypeError(f'term of progression should be int or float, not {type(kwargs[keys[1]])}')
            dig = int(keys[1].split('val')[1])
            first = kwargs[keys[1]] - (dig - 1) * d
    elif ('sum' in keys[0] or 'sum' in keys[1]) and 'step' in keys:
        if type(kwargs['step']) not in [int, float]:
            raise TypeError(f'step of progression should be int or float, not {type(kwargs["step"])}')
        d = kwargs['step']
        if 'sum' in keys[0]:
            if type(kwargs[keys[0]]) not in [int, float]:
                raise TypeError(f'sum of progression should be int or float, not {type(kwargs[keys[0]])}')
            dig = int(keys[0].split('sum')[1])
            first = (kwargs[keys[0]] / dig) - d * (dig - 1) / 2
        else:
            if kwargs[keys[1]] not in [int, float]:
                raise TypeError(f'sum of progression should be int or float, not {type(kwargs[keys[1]])}')
            dig = int(keys[1].split('sum')[1])
            first = (kwargs[keys[1]] / dig) - d * (dig - 1) / 2
    elif 'sum' in keys[0] and 'sum' in keys[1]:
        for i in kwargs:
            if type(kwargs[i]) not in [int, float]:
                raise TypeError(f'sum of progression should be int or float, not {type(kwargs[i])}')

        dig1 = int(keys[0].split('sum')[1])
        dig2 = int(keys[1].split('sum')[1])
        d = (kwargs[keys[1]] / dig2 - kwargs[keys[0]] / dig1) * (2 / (dig2 - dig1))
        first = (kwargs[keys[0]] / dig1) - d * (dig1 - 1) / 2

    elif ('sum' in keys[0] and 'val' in keys[1]) or ('val' in keys[0] and 'sum' in keys[1]):
        if 'sum' in keys[0]:
            if type(kwargs[keys[0]]) not in [int, float]:
                raise TypeError(f'sum of progression should be int or float, not {type(kwargs[keys[0]])}')
            if type(kwargs[keys[1]]) not in [int, float]:
                raise TypeError(f'term of progression should be int or float, not {type(kwargs[keys[1]])}')
            dig1 = int(keys[0].split('sum')[1])
            dig2 = int(keys[1].split('val')[1])
            d = (2 * kwargs[keys[0]] / dig1 - 2 * kwargs[keys[1]]) / (dig1 - 2 * dig2 + 1)
            first = kwargs[keys[1]] - (dig2 - 1) * d
        else:
            if type(kwargs[keys[0]]) not in [int, float]:
                raise TypeError(f'term of progression should be int or float, not {type(kwargs[keys[0]])}')
            if type(kwargs[keys[1]]) not in [int, float]:
                raise TypeError(f'sum of progression should be int or float, not {type(kwargs[keys[1]])}')
            dig1 = int(keys[0].split('val')[1])
            dig2 = int(keys[1].split('sum')[1])
            d = (2 * kwargs[keys[1]] / dig2 - 2 * kwargs[keys[0]]) / (dig2 - 2 * dig1 + 1)
            first = kwargs[keys[0]] - (dig1 - 1) * d
    else:
        raise ValueError('invalid parameters')
    return ArithmeticalProgression(first, d)


if __name__ == '__main__':
    a = arithmetical_progression(val2=82982478256, sum100=0)
    print(a)








