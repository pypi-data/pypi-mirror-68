"""prog_work.geometrical_progression
this module is intended for work with geometrical progression

Creation of geometrical progression
    If you do know the first term of the progression and it's step,
    create the progression directly with GeometricalProgression.__init__
    If you have another information about the progression use geometrical_progression to create it.
"""


from prog_work.base_progression import BaseProgression
from prog_work.exceptions import UncertainProgressionError, InfiniteSumError


class GeometricalProgression(BaseProgression):
    """prog_work.geometrical_progression.GeometricalProgression(BaseProgression)
        the class for geometrical progressions
        attributes:
            _value - value that __next__ returns
            _first - the first term of the progression
            step - the step of the progression
        methods:
            __init__
            __next__
            __getitem__
            getitem
            sum
            inf_sum"""

    def __init__(self, first, step):
        super(GeometricalProgression, self).__init__(first, step)
        if not first:
            raise ValueError('the first term of the geometrical progression shouldn\'t be equal to 0')
        if not step - 1:
            raise ValueError('the step of geometrical progression shouldm\'t be equal to 1')

    def __next__(self):
        result = self._value
        self._value *= self.step
        return result

    def __getitem__(self, item):
        super(GeometricalProgression, self).__getitem__(item)
        if type(item) == int:
            if item < 0:
                raise ValueError('serial number of progression\'s term should not be negative')
            return self._first * self.step**item

    def getitem(self, item):
        super(GeometricalProgression, self).getitem(item)
        if type(item) == int:
            if item <= 0:
                raise ValueError('serial number of progression\'s term should be positive')
            return self._first + self.step**(item - 1)

    def sum(self, amount):
        return self._first * (self.step**amount - 1) / (self.step - 1)

    def inf_sum(self):
        """GeometricalProgression.inf_sum
        if abs(GeometricalProgression.step) < 1
        :returns infinite sum of the progression
        else
        :raises prog_work.exceptions.InfiniteSumError"""
        if abs(self.step) < 1:
            return self._first / (1 - self.step)
        raise InfiniteSumError

    def __str__(self):
        first = int(self._first) if int(self._first) == self._first else self._first
        step = int(self.step) if int(self.step) == self.step else self.step
        return f'b[n]={first}*{step}**(n-1)'

    def __repr__(self):
        return f'GP({self._first}, {self.step})'


def geometrical_progression(**kwargs):
    """prog_work.geometrical_progression.geometrical_progression(**kwargs)
     To create a progression you need to pass two parameters such as:
         val{num}
         step
         sum{num}
         inf_sum
     You can pass
         two values:
            gp = geometrical_progression(val34=1238.45, val21=4675.776)
         value and step:
            gp = geometrical_progression(val18=42, step=1.02)
         sum and step:
            gp = geometrical_progression(sum80=12345.6789, step=2)
         inf_sum and step:
            gp = geometrical_progression(inf_sum=10, step=0.5)
            if abs(step) > 1
            :raises InfiniteSumError
         other parameters will raise an exception
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
            d = (kwargs[keys[0]] / kwargs[keys[1]])**(1 / (dig1 - dig2))
        else:
            d = (kwargs[keys[1]] / kwargs[keys[0]])**(1 / (dig2 - dig1))
        first = kwargs[keys[0]] / d**(dig1 - 1)

    elif ('val' in keys[0] or 'val' in keys[1]) and 'step' in keys:
        if type(kwargs['step']) not in [int, float]:
            raise TypeError(f'step of progression should be int or float, not {type(kwargs["step"])}')
        d = kwargs['step']
        if 'val' in keys[0]:
            if type(kwargs[keys[0]]) not in [int, float]:
                raise TypeError(f'term of progression should be int or float, not {type(kwargs[keys[0]])}')
            dig = int(keys[0].split('val')[1])
            first = kwargs[keys[0]] / d**(dig - 1)
        else:
            if kwargs[keys[1]] not in [int, float]:
                raise TypeError(f'term of progression should be int or float, not {type(kwargs[keys[1]])}')
            dig = int(keys[1].split('val')[1])
            first = kwargs[keys[1]] / d**(dig-1)
    elif ('sum' in keys[0] or 'sum' in keys[1]) and 'step' in keys and 'inf_sum' not in keys:
        if type(kwargs['step']) not in [int, float]:
            raise TypeError(f'step of progression should be int or float, not {type(kwargs["step"])}')
        d = kwargs['step']
        if 'sum' in keys[0]:
            if type(kwargs[keys[0]]) not in [int, float]:
                raise TypeError(f'sum of progression should be int or float, not {type(kwargs[keys[0]])}')
            dig = int(keys[0].split('sum')[1])
            first = kwargs[keys[0]] * (d - 1) / (d**dig - 1)
        else:
            if kwargs[keys[1]] not in [int, float]:
                raise TypeError(f'sum of progression should be int or float, not {type(kwargs[keys[1]])}')
            dig = int(keys[1].split('sum')[1])
            first = kwargs[keys[1]] * (d - 1) / (d**dig - 1)
    elif 'sum' in keys[0] and 'sum' in keys[1]:
        raise UncertainProgressionError
    elif ('sum' in keys[0] and 'val' in keys[1]) or ('val' in keys[0] and 'sum' in keys[1]):
        raise UncertainProgressionError
    elif ('val' in keys[0] or 'val' in keys[1]) and 'inf_sum' in keys:
        raise UncertainProgressionError
    elif (('sum' in keys[0] and keys[0] != 'inf_sum') or ('sum' in keys[1] and keys[1] != 'inf_sum'))\
            and 'inf_sum' in keys:
        raise UncertainProgressionError
    elif 'inf_sum' in keys and 'step' in keys:
        d = kwargs['step']
        if abs(d) > 1:
            raise InfiniteSumError
        first = kwargs['inf_sum'] * (1 - d)
    else:
        raise ValueError('invalid parameters')
    return GeometricalProgression(first, d)


if __name__ == '__main__':
    g = geometrical_progression(sum4=10, val4=2)
    print(g)

