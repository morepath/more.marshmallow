class Error(Exception):
    def __init__(self, errors):
        super(Error, self).__init__("Marshmallow validation error")
        self.errors = errors
