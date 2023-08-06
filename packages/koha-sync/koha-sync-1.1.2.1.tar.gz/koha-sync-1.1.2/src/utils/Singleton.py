class Singleton(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        """"
        called before __init__
        """
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
            return cls._instance
