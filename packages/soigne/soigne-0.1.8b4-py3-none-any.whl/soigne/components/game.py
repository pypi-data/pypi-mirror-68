#!/usr/bin/env python
# coding=utf-8

from pygame.constants import BUTTON_RIGHT, BUTTON_MIDDLE

from soigne.container import Component, Event
from soigne.gamegui import GameGui


class Game(Component):
    resources = 'resources/assets/'

    gui: GameGui = None

    pressed_keys = {}
    need_redraw_gui = True
    need_redraw_after_draw_gui = True
    need_resize_window = False
    stopped = True

    def __init__(self, app):
        super().__init__(app)

        self.app.register('event', 'game_initialization', Event('game_initialization'))
        self.app.register('event', 'game_gui_drawn', Event('game_gui_drawn'))

        self.app.dispatch('quit', on_quit)
        self.app.dispatch('mousebuttonup', on_mousebuttonup)
        self.app.dispatch('mousebuttondown', on_mousebuttondown)
        self.app.dispatch('videoresize', on_videoresize)

        self.resources = self.app.path(self.resources)

    def build(self):
        """ """
        self.gui = self.app.get('component', 'gui')

        self.gui.init()
        self.trigger_event('game_initialization', self)

        self.gui.draw(lambda *args: self.trigger_event('game_gui_drawn', self, *args))

        return self

    def start(self, handler: callable = None, *args):
        """ A method for starting a game event processing cycle.

        Updates the game window, event handlers.
        """

        gui_events = self.gui.component('event')

        self.stopped = False
        while not self.stopped:
            self.gui.component('time').Clock().tick(self.gui.FRAMES)

            self.pressed_keys = self.gui.component('key').get_pressed()

            if handler:
                handler(self, *args)

            for event in gui_events.get():
                if event.type not in self.gui.EVENTS:
                    continue

                self.trigger_event(self.gui.EVENTS[event.type], self, event)

            self.gui.update(self.need_redraw_gui, self.need_resize_window)
            self.need_redraw_gui = self.need_redraw_after_draw_gui
            self.need_resize_window = False

        self.gui.close()

    def stop(self):
        self.stopped = True


def on_quit(app, event, game, game_event):
    game.stopped = True


def _click(app, game, game_event):
    element = game.gui.element(None, *game_event.pos)
    if not element:
        return

    event_name = 'lclick'

    if game_event.button == BUTTON_RIGHT:
        event_name = 'rclick'
    elif game_event.button == BUTTON_MIDDLE:
        event_name = 'mclick'

    method = 'on'

    if game_event.type == 1026:
        method = 'off'

    event = element.__getattribute__(method)
    event(event_name, app, game, game_event)


def on_mousebuttonup(app, event, game: Game, game_event):
    _click(app, game, game_event)
    game.need_redraw_after_draw_gui = True


def on_mousebuttondown(app, event, game, game_event):
    _click(app, game, game_event)
    game.need_redraw_after_draw_gui = False


def on_videoresize(app, event, game: Game, game_event):
    game.gui.set_dimensions(*game_event.size)
    game.need_resize_window = True
