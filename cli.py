#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cmd
import argparse

class Cli(cmd.Cmd):
  intro = "Welcome to prompt"
  prompt = ">> "
  undoc_header = None
  doc_header = "Comandos disponíveis"
  
  def do_hello(self, line):
    print "hi!"

  def do_EOF(self, line):
    return True
    
  def emptyline(self):
    pass

  def print_topics(self, header, cmds, cmdlen, maxcol):
    if header is not None:
      cmd.Cmd.print_topics(self, header, cmds, cmdlen, maxcol)

'''
if __name__ == '__main__':
  print "blorp"
  Cli().cmdloop()
'''
