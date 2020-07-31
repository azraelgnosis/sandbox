class Alpha:
    def __init__(self, a='aye'):
        self._a = a
        self._b = 'bee'

    @property
    def a(self):
        return self._a
    
    @a.setter
    def a(self, val):
        self._a = val

    @property
    def b(self):
        return self.b
        
alpha = Alpha()
beta = Alpha("huh")