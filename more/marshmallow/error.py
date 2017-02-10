class ValidationError(Exception):
    def __init__(self, errors):
        super(ValidationError, self).__init__("Marshmallow validation error")
        self.errors = errors
