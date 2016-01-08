#!/usr/bin/env python
import os
import inspect
import argparse
import ConfigParser

__author__  = 'Sergio Orlandini'
__version__ = 'v0.2.0'

try:
    import_file = inspect.stack()[1][1]
except:
    import_file = __file__

class argconfig(argparse.Action):

     _config_file = 'config.ini'
     _config_section = ['default']
     _config_path = [
                      os.getcwd(),                                         # current work dir
                      os.path.dirname( os.path.realpath(__file__) ),       # installation dir
                      os.path.dirname( os.path.realpath( import_file ) ),  # caller's dir
                    ]

     def __init__(self, overwrite_default=True, verbose=False, **kwargs):

         argparse_keys = ['option_strings', 'dest', 'const', 'default', 'type', 'choices', 'required', 'help', 'metavar']
         _d = {'option_strings' : None}
         _d.update( {k: kwargs[k] for k in argparse_keys if k in kwargs.keys()} )
         super(argconfig, self).__init__( **_d )

         # key to search in config file
         self.argkey = kwargs.get('argkey', self.dest)

         # sections
         self.section = []

         if 'section' in kwargs:
            self.section.append( kwargs['section'] )

         # default
         _default = self.get_default()

         if _default and overwrite_default:
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

         _section = self._config_section
         if hasattr(self, 'section'):
            _section += self.section

         # loop on config paths
         for file_cfg in self.get_file_list():

             cp = ConfigParser.ConfigParser(allow_no_value=True)
             cp.read( file_cfg )

             # loop on sections
             for sec in _section:

                try:
                   value_cfg = cp.get(sec, self.argkey)
                   update = True
                except:
                   pass

             if update: break

         return value_cfg


     # path class method

     @classmethod
     def add_path(self, path):
         """Add path to configuration file paths.
            Prepend path to default list.
         """
         abs_path = os.path.normpath( os.path.abspath(path) )
         self._config_path.insert(0, abs_path)

     @classmethod
     def set_path(self, path):
         """Set configuration file paths.
            Overwrite default list.
         """
         if not isinstance(path, list):
             path = [path]
         self._config_path = []
         for p in path:
             abs_path = os.path.normpath( os.path.abspath(p) )
             self._config_path.append( abs_path )

     @classmethod
     def get_path(self):
         """Return configuration file paths."""
         return self._config_path

     # file class method

     @classmethod
     def set_file(self, file_name):
         """Set configuration file name.
            Overwrite default configuration file name.
         """
         self._config_file = file_name

     @classmethod
     def get_file(self):
         """Return configuration file name."""
         return self._config_file

     @classmethod
     def get_file_list(self):
         """Return list of configuration files."""
         l = []
         # loop on config paths
         for d in self._config_path:
            file_cfg = os.path.join( d, self._config_file )
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
         self._config_section = section

     @classmethod
     def get_section(self):
         """Return section."""
         return self._config_section

