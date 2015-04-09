import unittest
from mock import Mock

from typeschema import model as mod

class TestCase(unittest.TestCase):
    def setUp(self):
        super(TestCase, self).setUp()
        self.definition_params = {
            'foo': (Mock(return_value='foo_prop'), (), {'default':0}),
            'bar': (Mock(return_value='bar_prop'), (), {}),
        }
        self.definitions = {
            'foo': self._get_define('foo'),
            'bar': self._get_define('bar'),
        }
        self.attrs = {
            'ignored': "ignored value"
        }

    def _get_define(self, name):
        prop, args, kwargs = self.definition_params[name]
        return mod.Define(prop, *args, **kwargs)

    def test_model_meta_is_correct_instance(self):
        cls = self.get_example_class()
        self.assertIsInstance(cls._meta, mod.Meta)

    def test_model_meta_has_correct_definitions(self):
        cls = self.get_example_class()
        definitions = cls._meta.definitions
        self.assertEqual(definitions, self.definitions)

    def test_model_meta_has_correct_properties(self):
        cls = self.get_example_class()
        for name, prop in cls._meta.properties.items():
            mock, args, kwargs = self.definition_params[name]
            self.assertEqual(prop, mock.return_value)
            mock.assert_called_once_with(name, *args, **kwargs)

    def get_example_class(self):
        class Example(mod.Model):
            foo = self.definitions['foo']
            bar = self.definitions['bar']
            ignored = self.attrs['ignored']

        return Example
