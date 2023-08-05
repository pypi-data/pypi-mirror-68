#!/usr/bin/env python
# coding=utf-8

from configparser import ConfigParser
from os import listdir


class Configs:
    _parser = None
    path = ''

    def __init__(self, path):
        self._parser = ConfigParser()
        self.path = path

    def _load_config(self, config):
        self._parser.read(self.path + config)

        for section in self._parser.sections():
            self.__setattr__(section, {})

            for option in self._parser.items(section):
                self.__getattribute__(section)[option[0]] = option[1]

    def read(self):
        for config in listdir(self.path):
            self._load_config(config)

        return self
