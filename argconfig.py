#!/usr/bin/env python
import os
import sys
import inspect
import argparse
import configparser

import_file = inspect.stack()[1][1]


class argconfig(argparse.Action):

    config_file = "config.ini"
    config_section = ["default"]
    config_path = [
        os.getcwd(),  # current work dir
        os.path.dirname(os.path.realpath(__file__)),  # installation dir
        os.path.dirname(os.path.realpath(import_file)),  # caller's dir
    ]

    def __init__(self, **kwargs):

        argparse_keys = [
            "option_strings",
            "dest",
            "const",
            "default",
            "type",
            "choices",
            "required",
            "help",
            "metavar",
        ]
        _d = {"option_strings": None}
        _d.update({k: kwargs[k] for k in argparse_keys if k in list(kwargs.keys())})
        super(argconfig, self).__init__(**_d)

        # key to search in config file
        self.argkey = kwargs.get("argkey", self.dest)

        # sections
        self.section = []

        if "section" in kwargs:
            self.section.append(kwargs["section"])

        # default
        _default = self.get_default()

        if _default:
            self.default = _default

    def __call__(self, parser, namespace, values, option_string=None, **kwargs):
        setattr(namespace, self.dest, values)

    def get_default(self, _default=None):
        """Return default value from configuration file.
            Search for dest key in configuration sections of configuration files.
            Read configuration file from configuration paths.
            Return the first occurrence of dest key in the configuration files.
            But the last occurrence of dest key in the sections of the configuration file.
         """

        value_cfg = _default

        update = False

        _section = self.config_section
        if hasattr(self, "section"):
            _section += self.section

        # loop on config paths
        for file_cfg in self.get_file_list():

            cp = configparser.ConfigParser(allow_no_value=True)
            cp.read(file_cfg)

            # loop on sections
            for sec in _section:

                try:
                    value_cfg = cp.get(sec, self.argkey)
                    update = True
                except:
                    pass

            if update:
                break

        return value_cfg

    # path class method

    @classmethod
    def add_path(self, path):
        """Add path to configuration file paths.
            Prepend path to default list.
         """
        abs_path = os.path.normpath(os.path.abspath(path))
        self.config_path.insert(0, abs_path)

    @classmethod
    def set_path(self, path):
        """Set configuration file paths.
            Overwrite default list.
         """
        if not isinstance(path, list):
            path = [path]
        self.config_path = []
        for p in path:
            abs_path = os.path.normpath(os.path.abspath(p))
            self.config_path.append(abs_path)

    @classmethod
    def get_path(self):
        """Return configuration file paths."""
        return self.config_path

    # file class method

    @classmethod
    def set_file(self, file_name):
        """Set configuration file name.
            Overwrite default configuration file name.
         """
        self.config_file = file_name

    @classmethod
    def get_file(self):
        """Return configuration file name."""
        return self.config_file

    @classmethod
    def get_file_list(self):
        """Return list of configuration files."""
        l = []
        # loop on config paths
        for d in self.config_path:
            file_cfg = os.path.join(d, self.config_file)
            if os.path.isfile(file_cfg):
                l.append(file_cfg)
        return l

    # section class method

    @classmethod
    def set_section(self, section):
        """Set section.
            Overwrite default section.
         """
        if not isinstance(section, list):
            section = [section]
        self.config_section = section

    @classmethod
    def get_section(self):
        """Return section."""
        return self.config_section
