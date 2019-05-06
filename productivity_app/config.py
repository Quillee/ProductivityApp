# PYTHON_ARGCOMPLETE_OK
# !/usr/bin/python

"""
    configuration

"""
from os import path
import sys
import base64
from _mssql import MssqlDatabaseException
from arghandler import subcmd, ArgumentHandler

from .lib.exc import ConfigurationError


class Settings:
    """ Settings that are used in the config.json file of the root dir
    """
    def __init__(self, *other_options, **config_settings):
        try:
            if other_options is not None and other_options != ():
                self.options = other_options
            if config_settings is not None and config_settings != {}:
                for name, setting in config_settings['config_settings'].items():
                    setattr(self, name, setting.replace('\n', ''))
        except KeyError as e:
            ## keyerror settingsect has __str__ property set to return the key that failed
            raise ConfigurationError(message='Config file incorrectly formatted. Problem near key %s' % e)

    def __str__(self):
        return '\n'.join(
            ['{setting_name}: {setting}'.format(setting_name=name, setting=setting)
                for name, setting in self.__dict__.items()])

    def __repr__(self):
        return "<Settings ({})>".format(', '.join(['%s: %s' % (name, setting) for name,
                                                   setting in self.__dict__.items()]))


class Config:
    """ Config handles overall management of configuration

    """
    _filename = 'config'

    def __init__(self, filename='config.json', *config_options, **config_settings):
        self.settings = Settings(config_options, config_settings)
        self.sql_auth = False
        self._filename = filename

    @property
    def filename(self):
        return self._filename

    @classmethod
    def read(cls, filename=None):
        """ reads config file and returns a config object with the specified params of the config file
            @Args:
                cls : class
                filename = None : full path to config. otherwise default will be used
            @Inpure: inpure function because it mutates state
            @Question: Should I return a new Config instance
           >>- >>= === === === === === ===  === === === === === ===  === === === === === === =<< -<<
        """
        if filename:
            cls._filename = filename
        try:
            with open(cls._filename, 'r') as config_file:
                setting_pair = config_file.readlines()
                full_settings = {}
                for setting_with_name in setting_pair:
                    setting_pair_list = setting_with_name.replace(' ', '').replace('\n', '').split(':')
                    if setting_pair_list[0][0] == '#':
                        continue
                    if setting_pair_list[0] == 'options':
                        ## in the case of options, save it as a list of additional options
                        ## remove the [ ] on the outsides of the list and then set the list to the 1st index
                        setting_pair_list[1] = setting_pair_list[1].replace('[', '').replace(']', '').split(',')
                    full_settings.update({setting_pair_list[0]: setting_pair_list[1]})
                cls.settings = Settings(config_settings=full_settings)
            return cls
        except IndexError:
            raise ConfigurationError(message=('Configuration file is not formatted correctly. Each setting must follow'
                                              ' the following format: "setting_name: setting". '
                                              'No extra whitespace allowed between settings'))

    @classmethod
    def write(cls):
        with open(cls._filename, 'w') as config_file:
            settings_with_details = []

            try:
                settings_with_details.append(', '.join(cls.settings.options))
            except AttributeError as e:
                pass

            for setting_name, choice in cls.settings.__dict__.items():
                settings_with_details.append('{}: {}'.format(setting_name, choice))
            config_file.write('\n'.join(settings_with_details))

    @staticmethod
    def b64_encode(string, key):
        encode_chars = []
        for i in range(len(string)):
            key_c = key[i % len(key)]
            encode_chars.append(chr(ord(string[i]) + ord(key_c) % 256))
        return base64.urlsafe_b64encode(''.join(encode_chars))

    @staticmethod
    def b64_decode(string, key):
        encode_chars = []
        for i in range(len(string)):
            key_c = key[i % len(key)]
            encode_chars.append(chr(ord(string[i]) - ord(key_c) % 256))
        return base64.b64decode(''.join(encode_chars))

    @staticmethod
    def generate_config(filename='config', *additional_options):
        config_obj = Config.read(filename)
        new_config = Config()
        new_config.settings = config_obj.settings
        return new_config

    def __repr__(self):
        return ("<Config (settings={settings}, "
                "filename={filename})>").format(settings=self.settings, filename=self._filename)