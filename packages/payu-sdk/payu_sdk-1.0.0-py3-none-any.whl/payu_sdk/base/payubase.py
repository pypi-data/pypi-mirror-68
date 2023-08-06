class Base(object):
    _instance = None

    d = dict()
    key = ""
    salt = ""

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Base, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def set_params(self,params):

        self.key = params.get("key")
        self.salt = params.get("salt")
        return (self.key ,self.salt)

    def get_params(self):

        return (self.key ,self.salt)


