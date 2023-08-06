from unittest import TestCase

import inject


class TestFunctional(TestCase):
    def tearDown(self):
        inject.clear()

    def test(self):
        class Config(object):
            def __init__(self, greeting):
                self.greeting = greeting

        class Cache(object):
            config = inject.attr(Config)

            def load_greeting(self):
                return self.config.greeting

        class User(object):
            cache = inject.attr(Cache)

            def __init__(self, name):
                self.name = name

            def greet(self):
                return '%s, %s' % (self.cache.load_greeting(), self.name)

        def config(binder):
            binder.bind(Config, Config('Hello'))

        inject.configure(config)

        user = User('John Doe')
        greeting = user.greet()
        assert greeting == 'Hello, John Doe'

    def test_class_with_restricted_bool_casting(self):
        class DataFrame(object):
            def __nonzero__(self):
                """Python 2"""
                raise NotImplementedError('Casting to boolean is not allowed')

            def __bool__(self):
                """Python 3"""
                raise NotImplementedError('Casting to boolean is not allowed')

        def create_data_frame():
            return DataFrame()

        def config(binder):
            binder.bind_to_constructor(DataFrame, create_data_frame)

        inject.configure(config)

        assert type(inject.instance(DataFrame)) is DataFrame
        # There should not be an error when we fetch created instance
        assert type(inject.instance(DataFrame)) is DataFrame
