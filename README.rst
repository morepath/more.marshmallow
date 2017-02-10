more.marshmallow: (de)serialization support for Morepath
========================================================

This package provides Morepath integration for the Marshmallow_ object
serialization library:

.. _Marshmallow: https://marshmallow.readthedocs.io

Marshmallow can automate user input validation and conversion in a HTTP API. It
also provides serialization support. This lets you automatically translate
objects to JSON structures and back using a schema.

Schema
------

You can define a schema using Marshmallow:

.. code-block:: python

  from marshmallow import Schema, fields

  class MySchema(Schema):
      title = fields.Str()

  my_schema = MySchema()

Serialize
---------

You can serialize using this schema:

.. code-block:: python

  @App.json(model=Document)
  def document_get(self, request)
      return my_schema.dump(self)

You can also make this serialization automatically occur
whenever you return an ``Document`` instance from a view, using
`dump_json`_:

.. code-block:: python

  @App.dump_json(model=Document)
     return my_schema.dump(self)

Now you can simplify the GET view:

.. code-block:: python

  @App.json(model=Document)
  def document_get(self, request)
      return self

.. _`dump_json`:  http://morepath.readthedocs.io/en/latest/api.html#morepath.App.dump_json

Deserialize
-----------

So far we haven't actually used ``more.marshmallow`` yet. This integration helps
with deserialization of the request body as it is POSTed or PUT to a view. First
we must create a loader for our schema:

.. code-block:: python

  from more.marshmallow import loader

  my_schema_load = loader(my_schema)

Alternatively you can pass in the Marshmallow schema class to control the
loader; the loader automatically instantiates it:

.. _code-block:: python

  my_schema_load = loader(MySchema)

We can use this loader to handle a PUT request for instance:

.. code-block:: python

  @App.json(model=Document, request_method='PUT', load=my_schema_load)
  def document_post(self, request, obj):
      # obj is now a deserialized dict of whatever got
      # PUT onto this view that you can use to update
      # self

Deserialize with Context
------------------------

Your deserialization and validation logic may be dependent on application
context, such as the request. You can use ``request_loader`` to construct a
``load`` function that makes sure there is a ``request`` entry in the
``context`` attribute on Marshmallow schemas. Note that you need to pass the
schema *class* into this function, not a schema instance:

.. code-block:: python

  from more.marshmallow import request_loader

  my_schema_load = request_loader(MySchema)

You can also control context construction manually with ``context_loader``:

.. code-block:: python

  from more.marshmallow import context_loader

  def get_context(request):
     return {
         "whatever": "you want",
     }
  my_schema_load = context_loader(MySchema, get_context)

``context_loader`` gets a request instance as the argument so you can use it to
access information.

Error handling
--------------

If deserialization fails due to a deserialization error (a required field is
missing, or a field is of the wrong datatype, for instance), you want to show
some kind of error message. The ``load`` functions created by
``more.marshmallow`` raise the ``more.marshmallow.Error`` exception in case of
errors.

This exception object has an ``errors`` attribute with the validation errors.
You must define an exception view for it, otherwise validation errors are
returned as "500 internal server error" to API users.

This package provides a default exception view implementation. If you subclass
your application from ``more.marshmallow.MarshmallowApp`` then you get a default
error view for ``Error`` that has a 422 status code with a JSON response with
the marshmallow errors structure:


.. code-block:: python

  from more.marshmallow import MarshmallowApp

  class App(MarshmallowApp):
      pass

Now your app has reasonable error handling built-in.
