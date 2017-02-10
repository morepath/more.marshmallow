from .error import ValidationError


def loader(schema):
    def load(request):
        data, errors = schema.load(request.json)
        if errors:
            raise ValidationError(errors)
        return data
    return load
