"""
typeschema.models defines useful classes that allow for declarative syntax
for objects with ``typeschema`` properties. A simple example looks like this.

>>> import typeschema.properties as ts

>>> class Example(Model):
...     foo = Define(ts.int, default=0)
...     bar = Define(ts.string)

Metaclass magic makes it possible to omit the name of the property. Instances of
``Example`` will have ``foo`` and ``bar`` properties, which will be instances of
``typeschema.int`` and ``typeschema.string`` respectively.

The ``Example`` class will also get a ``_meta`` attribute, instance of the ``Meta`` class
(see below). This class contains information about the way the model was declared.

"""

class Define(object):
    """
    Wraps a ``typeschema.property`` when using ``Model`` declarative syntax.
    All arguments and keyword arguments are used to instantiate the property.
    """
    def __init__(self, propclass, *args, **kwargs):
        self.name = None # set during metaclass __new__
        self.propclass = propclass
        self.args = args
        self.kwargs = kwargs

    def get_property(self):
        if self.name is None:
            raise RuntimeError('Unititialized name for Define')

        return self.propclass(self.name, *self.args, **self.kwargs)


class Meta(object):
    """
    Holds information about the definitions (``Define`` instances) and properties
    (``property`` instances) that belong to a ``Model``. Attributes:

    properties: a dict of name: property
    definitions: a dict of name: Define
    """
    def __init__(self):
        self.properties = {}
        self.definitions = {}


class ModelMeta(type):
    """
    Metaclass thas makes the declarative syntax possible. Replaces class-level
    instances of ``Define`` with instances of ``property``, and sets ``_meta`` to the proper
    ``Meta`` instance.
    """

    def __new__(cls, cls_name, bases, attrs):
        new_attrs = { '_meta': Meta() }

        for name, attr in attrs.items():
            if isinstance(attr, Define):
                attr.name = name
                cls._update_attrs_from_definition(new_attrs, attr)
            else:
                new_attrs[name] = attr

        return type.__new__(cls, cls_name, bases, new_attrs)

    @classmethod
    def _update_attrs_from_definition(cls, attrs, definition):
        property = definition.get_property()
        attrs[definition.name] = property
        meta = attrs['_meta']
        meta.properties[definition.name] = property
        meta.definitions[definition.name] = definition


class Model(object):
    """
    Base class for all classes that intend to use the declarative syntax for properties
    """
    __metaclass__ = ModelMeta

    @classmethod
    def definitions(cls):
        return dict(cls._meta.definitions)
