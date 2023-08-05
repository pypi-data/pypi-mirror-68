#!/usr/bin/env python
# coding=utf-8

import abc
import json
import os

import pygame
from pygame.font import Font

from soigne.container import Component, Event, App


class GameGui(Component):
    """ Game interface.

    Serves to control the game interface and processes game events.
    It contains a set of parameters and methods for adding interface elements.
    """

    COMPONENTS = {}
    COLORS = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
    }
    EVENTS = {
        pygame.QUIT: 'quit',
        pygame.ACTIVEEVENT: 'activeevent',
        pygame.KEYDOWN: 'keydown',
        pygame.KEYUP: 'keyup',
        pygame.MOUSEMOTION: 'mousemotion',
        pygame.MOUSEBUTTONUP: 'mousebuttonup',
        pygame.MOUSEBUTTONDOWN: 'mousebuttondown',
        pygame.JOYAXISMOTION: 'joyaxismotion',
        pygame.JOYBALLMOTION: 'joyballmotion',
        pygame.JOYHATMOTION: 'joyhatmotion',
        pygame.JOYBUTTONUP: 'joybuttonup',
        pygame.JOYBUTTONDOWN: 'joybuttondown',
        pygame.VIDEORESIZE: 'videoresize',
        pygame.VIDEOEXPOSE: 'videoexpose',
        pygame.USEREVENT: 'userevent',
    }

    FRAMES = 30

    DOUBLEBUF = pygame.DOUBLEBUF
    FULLSCREEN = -pygame.FULLSCREEN
    HWSURFACE = pygame.HWSURFACE
    NOFRAME = pygame.NOFRAME
    OPENGL = pygame.OPENGL
    RESIZABLE = pygame.RESIZABLE
    SCALED = pygame.SCALED

    dimensions = (800, 450)
    caption = 'GuiComponent'
    icon = None
    background = 'black'
    centred = True
    font = 'Arial'
    flags = 0
    depth = 0
    display = 0

    window = None
    active_layout = None
    drawn_layout = None
    element_states = None
    elements = {}

    def __init__(self, app):
        Component.__init__(self, app)
        pygame.init()
        self._register_components()

        self.app.register('event', 'quit', Event('quit'))
        self.app.register('event', 'activeevent', Event('activeevent'))
        self.app.register('event', 'keydown', Event('keydown'))
        self.app.register('event', 'keyup', Event('keyup'))
        self.app.register('event', 'mousemotion', Event('mousemotion'))
        self.app.register('event', 'mousebuttonup', Event('mousebuttonup'))
        self.app.register('event', 'mousebuttondown', Event('mousebuttondown'))
        self.app.register('event', 'joyaxismotion', Event('joyaxismotion'))
        self.app.register('event', 'joyballmotion', Event('joyballmotion'))
        self.app.register('event', 'joyhatmotion', Event('joyhatmotion'))
        self.app.register('event', 'joybuttonup', Event('joybuttonup'))
        self.app.register('event', 'joybuttondown', Event('joybuttondown'))
        self.app.register('event', 'videoresize', Event('videoresize'))
        self.app.register('event', 'videoexpose', Event('videoexpose'))
        self.app.register('event', 'userevent', Event('userevent'))

    def init(self):
        """ Game interface initialization method.

        Registers the state of elements.
        Sets the rendering options for the game interface and window.
        """

        if self.centred:
            os.environ['SDL_VIDEO_CENTERED'] = '1'

        self.window = self.component('display').set_mode(
            self.dimensions,
            flags=self.flags,
            depth=self.depth,
            display=self.display
        )

        return self

    def color(self, name, alpha=None):
        """ Get color method. """

        if name not in self.COLORS:
            raise NameError('Unknown colour <' + str(name) + '> name. You can use only: '
                            + str.join(', ', self.COLORS.keys()) + '.')

        color = self.COLORS[name]

        if alpha is not None:
            return color[0], color[1], color[2], alpha

        return color

    def component(self, name='self'):
        """ Get game interface component method. """

        if name == 'self':
            return self

        if name not in self.COMPONENTS:
            raise NameError('Unknown gui <' + name + '> component. There are only '
                            + str.join(', ', self.COMPONENTS.keys()) + ' component in GUI class.')

        return self.COMPONENTS[name]

    def element(self, name=None, x=None, y=None):
        """ Returns the elements of an interface.

        With the given name, the element will be returned from the list by name.

        If you specify the position coordinates, an element will be found in the list,
        which crosses the specified position.
        """

        element = None

        if name and x is None and y is None:
            if name not in self.elements:
                raise NameError('Unknown <' + name + '> element.')

            element = self.elements[name]
        elif x >= 0 and y >= 0:
            for el in self.elements.values():
                if self.check_position(el.position, el.get_rect(), x, y):
                    element = el

        return element

    @staticmethod
    def check_position(position, dimensions, x, y):
        return position[0] < x < position[0] + dimensions.width and position[1] < y < position[1] + dimensions.height

    def has_flag(self, flag):
        return self.flags & flag != 0

    def set_colors(self, **colors):
        """ Add colors method.

        You should provide key-value pair of color name and rgb color value.
        """

        for name, color in colors.items():
            if type(color) is not tuple:
                raise TypeError('Invalid color parameters. Expected tuple, ' + str(type(color)) + ' given.')

            self.COLORS[name] = color

    def set_dimensions(self, width=800, height=450):
        """ Sets the size of the application window.

        Must be called before initializing the interface.
        """

        self.dimensions = (width, height)

    def set_centered(self, centered=True):
        """ Sets the rule that the application window must be outlined in the center of the screen.

        Must be called before initializing the interface.
        """

        self.centred = centered

    def set_flags(self, flags: int):
        self.flags = flags

    def set_depth(self, depth: int):
        """ Sets the number of bits for a color.

        It is usually best not to pass a depth argument. The default will be set
        The best and fastest color depth for the system.
        """

        self.depth = depth

    def set_display(self, display: int):
        self.display = display

    def set_icon(self, path, size=(32, 32)):
        self.icon = self.component('image').load(path).convert_alpha()  # Создаём (загружаем) иконку

        self.icon.set_colorkey(self.color('black'))
        self.icon.blit(self.icon, size)

        self.component('display').set_icon(self.icon)

    def set_caption(self, caption):
        self.caption = caption if caption else self.app.NAME

        self.component('display').set_caption(self.caption)

    def set_background(self, color):
        self.background = color

        self.window.fill(self.color(self.background))

    def set_layout(self, layout):
        self.active_layout = layout

    def add(self, name, element, x=0, y=0, parent=None, area=None, flags=0):
        """ Adds an interface element.

        Accepts an object of type pygame.Surface as an element.

        If an object of type app.gamegui.Element was passed, this object is added to the list,
        and the specified parameters after it overwrite the corresponding parameters of the specified object.
        """
        element_name = Element.parse_name(name)

        if isinstance(element, pygame.Surface):
            self.elements[element_name['name']] = element =\
                Element(element, element_name['name'], x, y, area, flags, parent)
        elif isinstance(element, Element):
            element.set_name(element_name['name'])
            element.set_position(x, y)
            element.set_parent(parent)
            element.set_area(area)
            element.set_flags(flags)

            self.elements[element_name['name']] = element
        else:
            raise TypeError('Unknown type of element ' + str(type(element))
                            + ". Element can be type of <class 'pygame.Surface'> or <class 'app.gamegui.Element'>.")

        # Register element events
        for event in Element.EVENTS:
            event_name = element.name + '_' + event

            self.app.register('event', 'on_' + event_name, Event('on_' + event_name))
            self.app.register('event', 'off_' + event_name, Event('off_' + event_name))

        self._set_element_states(element_name, element)

    def reset_elements(self):
        # for element in self.elements:
        #     for event in Element.EVENTS:
        #         self.app.remove_event('on_' + element + '_' + event, no_errors=True)
        #         self.app.remove_event('off_' + element + '_' + event, no_errors=True)
        #
        #     del self.elements[element]

        self.elements = {}

    def draw_elements(self):
        for element in self.elements.values():
            surface = self.window

            if element.parent is not None:
                surface = element.parent.subsurface(element.get_rect())

            x, y = self.component('mouse').get_pos()
            if element.need_change_hover_state and self.check_position(element.position, element.get_rect(), x, y):
                element.change_state(self.app, 'on', 'hovered')

            surface.blit(*element.surface())

    def draw_active_layout(self):
        layout = self.active_layout

        if layout is not None:
            layout(self).draw()

    def draw(self, callback=None, *args):
        """ Draws the application interface.

        Invokes the passed handler after rendering.
        """

        self.update()

        if callable(callback):
            callback(*args)

    def update(self, redraw_gui=True, resize_gui=False):
        """ Updates the game interface.

        With the specified false value of the redraw_gui parameter, the interface elements will not be redrawn.
        With the specified false value of the resize_gui parameter, the interface will not be resized.
        """

        if redraw_gui:
            self.window.fill(self.color(self.background))
            self.draw_elements()

        if resize_gui:
            self.window = self.component('display').set_mode(self.dimensions, self.flags)

            if isinstance(self.drawn_layout, Layout):
                self.drawn_layout.resize(*self.dimensions)

        if self.has_flag(self.OPENGL) or self.has_flag(self.DOUBLEBUF):
            self.component('display').flip()
        else:
            self.component('display').update()

    def close(self):
        self.reset_elements()
        self.component('display').quit()

    def _set_element_states(self, element_name, element):
        path = 'resources/element_states.json'

        if not self.app.exists(path):
            return

        element_state_name = element_name['group'] if element_name['group'] else element_name['name']
        with open(self.app.path(path), "r") as element_states:
            states = json.load(element_states)

        for state in states:
            state_name = None

            if element_state_name in state['name']:
                state_name = state['name'].replace(element_state_name, '').strip('.')

            if element_name['name'] in state['name']:
                state_name = state['name'].replace(element_name['name'], '').strip('.')

            if state_name:
                element.set_state(state_name, state['state'])

    def _register_components(self):
        self.COMPONENTS = {
            "display": pygame.display,
            "drawer": pygame.draw,
            "event": pygame.event,
            "image": pygame.image,
            "key": pygame.key,
            "mouse": pygame.mouse,
            "time": pygame.time,
            "transform": pygame.transform,
        }


class Layout:
    """ Gui interface layout.

    You can use this abstract layout to create your own interface layouts for showing it when you need.
    Layout should implement three methods. The First method it's elements,
    that returns list of parameters sequence for GameGui add method. Second method should contain
    dispatch event callings. And the last method it's resize method that will be called when window are resized.
    """

    gui: GameGui = None
    app: App = None

    x, y, width, height = 0, 0, 800, 450

    _elements = []

    def __init__(self, gui):
        self.gui = gui
        self.app = gui.app

        self.x, self.y, self.width, self.height = self.gui.window.get_rect()

    def drawn_elements(self):
        return self._elements

    def draw(self):
        self.gui.reset_elements()

        for element in self.elements():
            element_name = Element.parse_name(element[0])

            self.gui.add(*element)
            self._elements.append(element_name['name'])

        self.events()

        self.gui.drawn_layout = self

    @abc.abstractmethod
    def elements(self):
        return []

    def events(self):
        pass

    def resize(self, width, height):
        self.width, self.height = self.gui.dimensions


# class Sprites(pygame.sprite.Group):
#     def __init__(self, *sprites):
#         super().__init__(*sprites)
#
#     pass
#
#
# class Sprite(pygame.sprite.Sprite):
#     def __init__(self):
#         pass


class Element:
    """ An interface element. """

    LEFT_CLICK_EVENT = 'lclick'
    MIDDLE_CLICK_EVENT = 'mclick'
    RIGHT_CLICK_EVENT = 'rclick'
    MOUSEMOTION_EVENT = 'mousemotion'

    EVENTS = [
        LEFT_CLICK_EVENT,
        MIDDLE_CLICK_EVENT,
        RIGHT_CLICK_EVENT,
        MOUSEMOTION_EVENT,
    ]

    _surface = None

    name = ''
    position = (0, 0)
    area = None
    flags = 0
    parent = 0

    states = {}

    inited = False
    need_change_hover_state = True

    def __init__(self, surface, name='', x=0, y=0, area=None, flags=0, parent=None):
        self._surface = surface
        self.name = name
        self.position = (x, y)
        self.area = area
        self.flags = flags
        self.parent = parent

        self.states = {}

        self.inited = True

    @staticmethod
    def parse_name(string):
        parsed = string.split(':')
        group = ''

        if len(parsed) < 2:
            name = parsed[0]
        else:
            group, name = parsed

        return {"group": group, "name": name}

    def surface(self):
        """ Returns parameter sequence for pygame.Surface blit method. """
        return self._surface, self.position, self.area, self.flags

    def get_rect(self):
        return self._surface.get_rect()

    def get_dimensions(self):
        return self.get_rect().width, self.get_rect().height

    def set_name(self, name):
        self.name = name

    def set_position(self, x, y):
        self.position = (x, y)

    def set_area(self, area):
        self.area = area

    def set_flags(self, flags):
        self.flags = flags

    def set_parent(self, parent):
        self.parent = parent

    def set_state(self, name, state):
        self.states[name] = state

    @abc.abstractmethod
    def change_state(self, app: App, event_type, event_name, *options):
        pass

    def on(self, event_name, app, *options):
        self._trigger('on', event_name, app, *options)

    def off(self, event_name, app, *options):
        self._trigger('off', event_name, app, *options)

    def _trigger(self, name, event_name, app: App, *options):
        self.change_state(app, name, event_name, *options)

        event_name = name + '_' + self.name + '_' + event_name
        if app.is_triggerable(event_name):
            app.trigger_event(event_name, *options)

    def _get_state(self, name):
        if name in self.states:
            return self.states[name]

        return {}


class Field(Element):
    """ A rectangle interface element. """

    def __init__(self, width, height, background=(0, 0, 0), alpha=255, name='', x=0, y=0, *args, **kwargs):
        super().__init__(pygame.Surface((width, height)), name, x, y, *args, **kwargs)

        self.set_background(background, alpha)

    def convert(self):
        return self._surface.convert()

    def convert_alpha(self):
        return self._surface.convert_alpha()

    def get_colorkey(self):
        return self._surface.get_colorkey()

    def get_alpha(self):
        return self._surface.get_alpha()

    def set_colorkey(self, color):
        self._surface.set_colorkey(color)

        return self

    def set_alpha(self, value, flags=0):
        self._surface.set_alpha(value, flags)

        return self

    def set_background(self, background, alpha=255):
        if type(background) is tuple or type(background) is list:
            self._surface.fill(background)
            self._surface.set_alpha(alpha)

            return self

        background = pygame.transform.scale(pygame.image.load(background), self.get_dimensions())

        self._surface.blit(background, (0, 0))
        self._surface.set_colorkey((0, 0, 0))
        self._surface.set_alpha(alpha)

        return self

    def change_state(self, app: App, event_type, event_name, *options, **state):
        pass


# class Circle(Element):
#     radius = 0
#     background = 0
#
#     def __init__(self, radius, background=(0, 0, 0), name='', x=0, y=0, *args, **kwargs):
#         super().__init__(pygame.Surface((radius * 2, radius * 2)), name, x, y, *args, **kwargs)
#
#         self.radius = radius
#         self.background = background
#
#         self.draw()
#
#     def set_radius(self, radius):
#         self.radius = radius
#
#     def set_background(self, background):
#         self.background = background
#
#     def redraw(self):
#         pygame.draw.circle(self._surface, self.background, (self.radius, self.radius), self.radius)
#         self._surface.set_colorkey((0, 0, 0))
#
#     draw = redraw
#
#     def change_state(self, app: App, event_type, event_name, *options, **state):
#         pass


class Text(Element):
    text = ''
    color = (0, 0, 0)
    fontsize = 15
    font: Font = None
    fontname = 'Arial'
    italic = False
    bold = False
    underline = False

    def __init__(self, text, color=(0, 0, 0), fontsize=15, font='Arial', italic=False, bold=False, underline=False):
        self.text = text
        self.color = color
        self.fontsize = fontsize
        self.fontname = font
        self.italic = italic
        self.bold = bold
        self.underline = underline

        self.font = pygame.font.SysFont(self.fontname, self.fontsize)

        self.font.set_italic(self.italic)
        self.font.set_bold(self.bold)
        self.font.set_underline(self.underline)

        super().__init__(self.font.render(self.text, 1, self.color))

    def change_state(self, app: App, event_type, event_name, *options, **state):
        pass


class Button(Field):
    text: Text = None,
    textalign = 'center'

    def __init__(self, text, *args, **kwargs):

        color, textalign, fontsize, font, italic, bold, underline \
            = (255, 255, 255), 'center', 15, 'Arial', False, False, False

        if 'color' in kwargs:
            color = kwargs['color']
            kwargs.pop('color')

        if 'textalign' in kwargs:
            textalign = kwargs['textalign']
            kwargs.pop('textalign')

        if 'fontsize' in kwargs:
            fontsize = kwargs['fontsize']
            kwargs.pop('fontsize')

        if 'font' in kwargs:
            font = kwargs['font']
            kwargs.pop('font')

        if 'italic' in kwargs:
            italic = kwargs['italic']
            kwargs.pop('italic')

        if 'bold' in kwargs:
            bold = kwargs['bold']
            kwargs.pop('bold')

        if 'underline' in kwargs:
            underline = kwargs['underline']
            kwargs.pop('underline')

        super().__init__(*args, **kwargs)
        self.set_text(text, color, textalign, fontsize, font, italic, bold, underline)

    def change_state(self, app: App, event_type, event_name, *options):
        if event_type != 'on':
            return

        state = self._get_state(event_name)

        if len(state) == 0:
            return

        text = self.text.text
        color = self.text.color
        textalign = self.textalign
        fontsize = self.text.fontsize
        font = self.text.fontname
        italic = self.text.italic
        bold = self.text.bold
        underline = self.text.underline
        width, height = self.get_dimensions()
        x, y = self.position

        if 'background' in state:
            background = state['background']

            if type(background) is not list:
                background = app.path(background)

            self.set_background(background)

        if 'text' in state:
            text = state['text']

        if 'color' in state:
            color = state['color']

        if 'textalign' in state:
            textalign = state['textalign']

        if 'fontsize' in state:
            fontsize = state['fontsize']

        if 'font' in state:
            font = state['font']

        if 'italic' in state:
            italic = state['italic']

        if 'bold' in state:
            bold = state['bold']

        if 'underline' in state:
            underline = state['underline']

        if 'width' in state:
            width = state['width']

        if 'height' in state:
            height = state['height']

        if 'position' in state:
            if state['position'][0] is not None:
                x = state['position'][0]

            if state['position'][1] is not None:
                y = state['position'][1]

        self._surface = pygame.transform.scale(self._surface, (width, height))

        self.set_position(x, y)
        self.set_text(text, color, textalign, fontsize, font, italic, bold, underline)

        self.need_change_hover_state = False

    def set_text(self, text, color=(255, 255, 255), textalign='center', fontsize=15, font='Arial', italic=False, bold=False,
                 underline=False):
        if type(text) is not Text:
            self.text = Text(text, color, fontsize, font, italic, bold, underline)
        else:
            self.text = text

        self.textalign = textalign
        textalign = self.textalign.split(':')

        if len(textalign) < 2:
            textalign, outset = textalign[0], 5
        else:
            textalign, outset = textalign[0], int(textalign[1])

        text_width, text_height = self.text.get_dimensions()
        width, height = self.get_dimensions()

        self.text.set_position(outset, height / 2 - text_height / 2)

        if textalign == 'center':
            self.text.set_position(width / 2 - text_width / 2, height / 2 - text_height / 2)

        if textalign == 'right':
            self.text.set_position(width - text_width + outset, height / 2 - text_height / 2)

        self._surface.blit(*self.text.surface())


class Image(Element):
    filename = ''
    image = None

    def __init__(self, filename, colorkey=(0, 0, 0), width=0, height=None, *args, **kwargs):
        self.filename = filename

        self.image = pygame.image.load(filename)
        self.scale(width, height)

        super().__init__(self.image, *args, **kwargs)

        self.set_colorkey(colorkey)

    def scale(self, width=0, height=None):
        need_transform = width > 0 and (type(height) is int and height > 0)

        if width > 0 and (type(height) is not int or height <= 0):
            w = self.image.get_rect().width
            h = self.image.get_rect().height
            k = width / w
            height = int(h * k)

            need_transform = True

        if width == 0 and (type(height) is int and height > 0):
            h = self.image.get_rect().height
            w = self.image.get_rect().width
            k = height / h
            width = int(w * k)

            need_transform = True

        if need_transform:
            self.image = pygame.transform.scale(self.image, (width, height))

    def fill(self, width, height):
        if height > self.image.get_rect().height:
            self.scale(height=height)

        if width > self.image.get_rect().width:
            self.scale(width)

        dimensions = self.image.get_rect()
        x = (width - dimensions.width) / 2
        y = (height - dimensions.height) / 2

        return self.image, x, y

    def convert(self):
        return self._surface.convert()

    def convert_alpha(self):
        return self._surface.convert_alpha()

    def get_colorkey(self):
        return self._surface.get_colorkey()

    def get_alpha(self):
        return self._surface.get_alpha()

    def set_colorkey(self, color):
        self._surface.set_colorkey(color)

        return self

    def set_alpha(self, value, flags=0):
        self._surface.set_alpha(value, flags)

        return self

    def change_state(self, app: App, event_type, event_name, *options):
        pass
