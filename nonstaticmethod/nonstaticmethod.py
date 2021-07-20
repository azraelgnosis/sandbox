class nonstaticmethod:
    def __init__(self, func):
        self.cls = None
        self.instance = None
        self.func = func

    def __call__(self, *args, **kwargs):
        if self.instance:
            result = self.func(self.cls, self.instance, *args, **kwargs)
        else:
            result = self.func(self.cls, *args, **kwargs)

        return result

    def __set_name__(self, owner, name):
        self.cls = owner
        self.name = name

    def __get__(self, obj, obj_type):
        self.instance = obj
        self.cls = obj_type

        return self
