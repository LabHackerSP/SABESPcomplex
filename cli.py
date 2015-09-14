#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cmd import Cmd
import argparse
import pygame

class Cli(Cmd):
  undoc_header = None
  doc_header = "Comandos disponíveis"
  
  def do_hello(self, line):
    print "hi!"

  def do_EOF(self, line):
    return True
  
  def do_exit(self, line):
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    
  def emptyline(self):
    pass

  def print_topics(self, header, cmds, cmdlen, maxcol):
    if header is not None:
      Cmd.print_topics(self, header, cmds, cmdlen, maxcol)

'''
if __name__ == '__main__':
  print "blorp"
  Cli().cmdloop()
'''
