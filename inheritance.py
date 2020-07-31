class Alpha:
    def __init__(self, name=None):
        self.name = name

class Beta(Alpha):
    def __init__(self):
        super().__init__("bee")

class Gamma(Alpha):
    pass
    # def __init__(self):
    #     super(type, 'gee')

class Delta(Alpha):
    pass
    # def __init__(self):
    #     super.__init__(super(), 'dee')

b = Beta()
g = Gamma()
d = Delta()

print(b.name)
print(g.name)
print(d.gamma)