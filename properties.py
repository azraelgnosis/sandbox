class Alpha(object):
    def __init__(self):
        self._a = 1
        self._b = 2
        self._c = 3

    @property
    def a(self):
        return self.a

    @property
    def b(self):
        return self._b

    @property
    def c(self):
        return 32

# Alpha().a  # infinite loop
print(type(Alpha().b))
print(type(Alpha().c))