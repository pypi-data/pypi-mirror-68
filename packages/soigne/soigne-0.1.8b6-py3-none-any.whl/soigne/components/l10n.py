#!/usr/bin/env python
# coding=utf-8

from os import listdir as scan_languages_dir

import configparser


def __(phrase, *args):
    return Translation.translate(phrase, args)


class Language:
    DEFAULT = 'ru'

    _data = None

    name = ''
    locale = ''
    phrases = {}

    def __init__(self, locale, data):
        self.locale = locale
        self._data = data

        self.name = self._data['language']['name']

        self._load_phrases()

    def get_phrases(self):
        return self.phrases

    def _load_phrases(self):
        for phrase in self._data.items('phrases'):
            self.phrases[phrase[0]] = phrase[1]


class Translation:
    """ Translator class.

    Saves languages list, and phrases list of chosen language and
    translate needed phrases.
    """

    dir = ''
    languages = {}
    language = Language

    _parser = None

    def __init__(self, lang_dir, lang):
        self._parser = configparser.ConfigParser()

        self.dir = lang_dir

        self.load_languages()
        self.set_language(lang)

    def load_languages(self):
        for lang in scan_languages_dir(self.dir):
            self._load_language(lang)

    def set_language(self, lang):
        if lang not in self.languages:
            raise RuntimeError('Unknown language <' + lang + '>.')

        self.language = self.languages[lang]

    @staticmethod
    def translate(phrase, args):
        if phrase not in Translation.language.phrases:
            return phrase

        return Translation.language.phrases.get(phrase)

    def _load_language(self, lang):
        self._parser.read(self.dir + lang, 'utf-8')

        # Добавляем язык в переводчик.
        lang = lang.replace('.ini', '')
        self.languages[lang] = Language(lang, self._parser)
