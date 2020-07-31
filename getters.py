class Alpha:
    def __getitem__(self, obj:str):
        try:
            a = getattr(self, obj)
        except AttributeError:
            a = None
        return a

a = Alpha()
a.x = 'ex'
print(a.x)
print(a['x'])
print(a['y'])
