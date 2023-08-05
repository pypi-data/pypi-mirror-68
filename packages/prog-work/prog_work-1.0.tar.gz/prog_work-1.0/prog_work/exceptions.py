class ProgressionException(Exception):
    """prog_work.exceptions.ProgressionException(Exception)
    Base exception for progression exceptions"""
    pass


class UncertainProgressionError(ProgressionException):
    def __init__(self):
        """prog_work.exceptions.UncertainProgressionError(ProgressionException)
        :raise if it's impossible to creat a progression with given information"""
        super(UncertainProgressionError, self).__init__('ambiguity in initializing the progression')


class InfiniteSumError(ProgressionException):
    def __init__(self):
        """prog_work.exceptions.InfiniteSumError(ProgressionException)
        :raise if the geometrical progression doen\'t have infinite sum"""
        super(InfiniteSumError, self).__init__('this geometrical progression doesn\'t have a sum')
