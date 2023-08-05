#!/usr/bin/env python
# coding=utf-8

import os
import sys
import tkinter
import tkinter.messagebox


class App:
    """ Main application class.

    While you create your app, you should to define application constants firstly after creating app instance.
    Next you should to register your application components. So, after that you can dispatch some application events,
    if you needed.

    To run your app, you can call <class 'container.App'> start method, provide your primary component name and
    primary component's start method arguments, if it's required.

    Also, you can only build your primary component and call methods of it instantly.
    """

    NAME = 'python-application'
    DESCRIPTION = 'Python application'
    URL = ''
    VERSION = 'v0.1.0'

    _unknown_event_error = 'Unknown <%s> event.'

    _path = './'

    _components = {}
    _component = None
    _events = {}

    def __init__(self, path='./'):
        self.register('event', 'application_build', Event('application_build'))

        self._path = path

    def path(self, path):
        return self._path + '/' + path

    def exists(self, path):
        return os.path.exists(self._path + '/' + path)

    def get(self, attr: str, name: str = None):
        """ Returns application attribute.

        :param attr attribute type.
        :param name attribute name.
        """

        attribute = '_' + attr + 's'

        if attribute not in dir(self):
            raise NameError('Unknown application attribute <' + attr + '>.')

        attribute = self.__getattribute__(attribute)

        if name is None:
            return attribute

        if name not in attribute:
            raise NameError('Unknown application ' + attr + ' <' + name + '>.')

        return attribute[name]

    def start(self, component_name: str, *args):
        """ Start application method.

        Firstly, you should provide your primary component name that
        has build method for start your app.
        Next arguments will be provided to start method of your primary component if it is.

        Notice, that this method has functionality for shoving your application's errors.
        """

        if '--debug' in args:
            return self.debug(component_name, *args)

        try:
            self.build(component_name)

            if 'start' in dir(self._component):
                start = self._component.__getattribute__('start')
                start(*args)
        except Exception:
            tkinter.Tk().withdraw()
            info = sys.exc_info()

            tkinter.messagebox.showerror(info[0].__name__, info[1])

        sys.exit()

    def debug(self, component_name: str, *args):
        """ Start application method for debug mode.

        Firstly, you should provide your primary component name that
        has build method for start your app.
        Next arguments will be provided to start method of your primary component if it is.
        """

        self.build(component_name)

        if 'start' in dir(self._component):
            start = self._component.__getattribute__('start')
            start(*args)

    def build(self, component_name: str):
        """ Build application method.

        You should provide your primary component name that
        has build method for start your app.

        :raise RuntimeError if specified component has no build method.
        """

        self.trigger_event('application_build')

        component: Component = self.get('component', component_name)

        if 'build' in dir(component):
            build = component.__getattribute__('build')
            built = build()

            if built:
                self._component = built
        else:
            raise RuntimeError(component_name[0].upper() + component_name[1:] + ' component has no build method.')

        return self._component

    def register(self, attribute: str, *options, registerer: callable = None):
        """ Registers application attributes.

        Attribute name can be string with latin letters, numbers and underscores.
        """

        attr = '_register_' + attribute + 's'

        # Raise an error if attribute registerer not defined in app and it wasn't given.
        if attr not in dir(App) and not callable(registerer):
            raise NameError('Unknown registration name <' + attribute + '>.')

        # Register attribute if registerer is callable.
        # A Custom registerer has high priority, and we check and call it firstly.
        if callable(registerer):
            self.__setattr__('_' + attribute + 's', registerer(self, options[0], *options))
            return

        # However, we call defined app attribute registerer.
        registerer = self.__getattribute__(attr)
        registerer(options)

    def dispatch(self, event: str, handler: callable):
        """ Sets event handler.

        :param event: is a name of event.
        :param handler is callable function, that'll be called, while an event handled.
        """

        if event not in self._events:
            raise SystemError(self._unknown_event_error % event)

        self._events[event].append_handler(handler)

    def is_triggerable(self, event):
        """ Check an event could be triggered.
        """

        return event in self._events

    def trigger_event(self, name, *args, **kwargs):
        """ Trigger an event with specified parameters.
        """

        if name not in self._events:
            raise SystemError(self._unknown_event_error % name)

        self._events[name].trigger(self, *args, **kwargs)

    def remove_event(self, name, no_errors=False):
        """ Remove event from events list.

        For except any errors, you can provide no_errors True value.
        """

        if name not in self._events and not no_errors:
            raise SystemError(self._unknown_event_error % name)

        del self._events[name]

    def _register_events(self, options):
        if type(options[1]) is not Event:
            raise TypeError('Registered event mast be type of app.container.Event')

        self._events[options[0]] = options[1]

    def _register_components(self, options):
        component = options[1]

        if not issubclass(component, Component):
            raise TypeError('Registered component mast be type of app.container.Component')

        self._components[options[0]] = component(self)


class Component:
    app: App = None

    def __init__(self, app):
        self.app = app

    def trigger_event(self, name, *args, **kwargs):
        self.app.trigger_event(name, *args, **kwargs)


class Event:
    name = ''
    handlers = []

    data = None

    def __init__(self, name):
        self.name = name
        self.handlers = []

    def append_handler(self, handler):
        self.handlers.append(handler)

    def trigger(self, app, *args, **kwargs):
        for handler in self.handlers:
            handler(app, self, *args, **kwargs)
