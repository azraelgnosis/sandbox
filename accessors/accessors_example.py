class Example(object):
    def __getattr__(self, attr):
        return super().__getattribute__(attr)

    def __getitem__(self, item):
        return getattr(self, item)

    def __setattr__(self, attr, val):
        super().__setattr__(attr, val)

    def __setitem__(self, item, val):
        setattr(self, item, val)
