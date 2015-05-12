#!/usr/bin/env python
import os
import sys
import argparse
import ConfigParser


class argconfig(argparse.Action):

     config_file = 'config.ini' 
     config_section = ['default']
     config_path = [
                     os.getcwd(),                                   # current work dir
                     os.path.dirname( os.path.realpath(__file__)),  # installation dir
                   ]

     def __init__(self, **kwargs):
         argparse_keys = ['option_strings', 'dest', 'const', 'default', 'type', 'choices', 'required', 'help', 'metavar']
         super(argconfig, self).__init__( **{k: kwargs[k] for k in argparse_keys if k in kwargs.keys()} )

         # sections
         self.section = self.config_section

         _section = kwargs.get('section', None)

         if _section:
             self.section.append(_section)

         # default
         _default = self._get_default()

         if _default:
             self.default = _default


     def __call__(self, parser, namespace, values, option_string=None, **kwargs):
         setattr(namespace, self.dest, values)


     def _get_default(self):

         value_cfg = None

         update = False

         # loop on config paths
         for d in self.config_path:

             file_cfg = os.path.join( d, self.config_file )

             cp = ConfigParser.ConfigParser(allow_no_value=True)
             cp.read( file_cfg )

             # loop on sections
             for sec in self.section:

                try:
                   value_cfg = cp.get(sec, self.dest)
                   update = True
                except:
                   pass

             if update: break

         return value_cfg


     # path class method

     @classmethod
     def add_path(self, path):
         abs_path = os.path.normpath( os.path.abspath(path) )
         self.config_path.insert(0, abs_path)

     @classmethod
     def set_path(self, path):
         if not isinstance(path, list):
             path = [path]

         self.config_path = []
         for p in path:
             abs_path = os.path.normpath( os.path.abspath(p) )
             self.config_path.append( abs_path )

     @classmethod
     def get_path(self):
         return self.config_path

     # file class method

     @classmethod
     def set_file(self, file_name):
         self.config_file = file_name

     @classmethod
     def get_file(self):
         return self.config_file

     # section class method

     @classmethod
     def set_section(self, section):
         if not isinstance(section, list):
             section = [section]

         self.config_section = section

     @classmethod
     def get_section(self):
         return self.config_section


def main():

   # parse command line options
   parser = argparse.ArgumentParser(prog='argconfig',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

   #action.set_path(['path1', 'path2'])
   #action.add_path('path3')
   #action.set_section(['sec1', 'sec2'])

   argconfig.set_path('.')
   argconfig.set_section('argconfig')

   parser.add_argument('-a', dest = 'dest_a', help = 'help_a',
                       action = argconfig)
   parser.add_argument('-b', dest = 'dest_b', help = 'help_b', default = 'default_b',
                       action = argconfig)
   parser.add_argument('-c', dest = 'dest_c', help = 'help_c', default = 42, type=int,
                       action = argconfig)

   parser.add_argument('-x', dest = 'dest_x', help = 'help_x', default = 42, type=int,
                       #section = 'argconfig',
                       action = argconfig)

   parser.add_argument('-d', dest = 'dest_d', help = 'help_d', default = 'a string',
                       action = argconfig)

   args = parser.parse_args()

   print args



if __name__ == "__main__":
   main()
