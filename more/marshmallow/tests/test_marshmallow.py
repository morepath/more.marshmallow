from marshmallow import Schema, ValidationError, fields, validates_schema
from more.marshmallow import (MarshmallowApp, context_loader, loader,
                              request_loader)
from webtest import TestApp as Client


def test_marshmallow():
    class User(object):
        def __init__(self, name, email):
            self.name = name
            self.email = email

    class UserSchema(Schema):
        name = fields.Str(required=True)
        email = fields.Email(required=True)

    user_schema = UserSchema()

    class App(MarshmallowApp):
        pass

    user = User('Somebody', 'somebody@example.com')

    @App.path(model=User, path='/')
    def get_user():
        return user

    @App.dump_json(model=User)
    def dump_user_json(self, request):
        return user_schema.dump(self).data

    @App.json(model=User)
    def user_default(self, request):
        return self

    @App.json(model=User, request_method='PUT',
              load=loader(user_schema))
    def user_put(self, request, obj):
        for key, value in obj.items():
            setattr(self, key, value)
        return self

    c = Client(App())

    r = c.get('/')
    assert r.json == {'name': 'Somebody', 'email': 'somebody@example.com'}
    r = c.put_json('/', {'name': "Somebody else",
                         "email": "somebody.else@example.com"})
    assert r.json == {'name': 'Somebody else',
                      'email': 'somebody.else@example.com'}
    assert user.name == 'Somebody else'
    assert user.email == 'somebody.else@example.com'

    r = c.put_json('/', {'name': 'Another'}, status=422)
    assert r.json == {'email': ['Missing data for required field.']}


def test_marshmallow_schema_class():
    class User(object):
        def __init__(self, name, email):
            self.name = name
            self.email = email

    class UserSchema(Schema):
        name = fields.Str(required=True)
        email = fields.Email(required=True)

    class App(MarshmallowApp):
        pass

    user = User('Somebody', 'somebody@example.com')

    @App.path(model=User, path='/')
    def get_user():
        return user

    @App.json(model=User, request_method='PUT',
              load=loader(UserSchema))
    def user_put(self, request, obj):
        for key, value in obj.items():
            setattr(self, key, value)
        return "done"

    c = Client(App())

    r = c.put_json('/', {'name': "Somebody else",
                         "email": "somebody.else@example.com"})
    assert user.name == 'Somebody else'
    assert user.email == 'somebody.else@example.com'

    r = c.put_json('/', {'name': 'Another'}, status=422)
    assert r.json == {'email': ['Missing data for required field.']}


def test_marshmallow_context_loader():
    class User(object):
        def __init__(self, name, email):
            self.name = name
            self.email = email

    class UserSchema(Schema):
        name = fields.Str(required=True)
        email = fields.Email(required=True)

        @validates_schema
        def validate(self, data):
            if self.context['entry'] != 'Correct':
                raise ValidationError("A problem")

    class App(MarshmallowApp):
        pass

    user = User('Somebody', 'somebody@example.com')

    @App.path(model=User, path='/')
    def get_user():
        return user

    def get_context(request):
        return {
            'entry': request.GET['entry']
        }

    @App.json(model=User, request_method='PUT',
              load=context_loader(UserSchema, get_context))
    def user_put(self, request, obj):
        for key, value in obj.items():
            setattr(self, key, value)
        return "correct"

    c = Client(App())

    r = c.put_json('/?entry=Incorrect',
                   {'name': "Somebody else",
                    "email": "somebody.else@example.com"},
                   status=422)
    assert r.json == {'_schema': ['A problem']}
    r = c.put_json('/?entry=Correct',
                   {'name': "Somebody else",
                    "email": "somebody.else@example.com"})
    assert r.json == "correct"
    assert user.name == 'Somebody else'


def test_marshmallow_request_loader():
    class User(object):
        def __init__(self, name, email):
            self.name = name
            self.email = email

    class UserSchema(Schema):
        name = fields.Str(required=True)
        email = fields.Email(required=True)

        @validates_schema
        def validate(self, data):
            if self.context['request'].GET['entry'] != 'Correct':
                raise ValidationError("A problem")

    class App(MarshmallowApp):
        pass

    user = User('Somebody', 'somebody@example.com')

    @App.path(model=User, path='/')
    def get_user():
        return user

    @App.json(model=User, request_method='PUT',
              load=request_loader(UserSchema))
    def user_put(self, request, obj):
        for key, value in obj.items():
            setattr(self, key, value)
        return "correct"

    c = Client(App())

    r = c.put_json('/?entry=Incorrect',
                   {'name': "Somebody else",
                    "email": "somebody.else@example.com"},
                   status=422)
    assert r.json == {'_schema': ['A problem']}
    r = c.put_json('/?entry=Correct',
                   {'name': "Somebody else",
                    "email": "somebody.else@example.com"})
    assert r.json == "correct"
    assert user.name == 'Somebody else'
