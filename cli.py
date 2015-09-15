# -*- coding: utf-8 -*-

from cmd import Cmd
import argparse, subprocess, os
import pygame

class Cli(Cmd):
  undoc_header = None
  doc_header = 'Comandos disponíveis'
  
  def __init__(self, parent=None):
    self.parent = parent
    Cmd.__init__(self)
    
  def do_hello(self, line):
    print('hi!\ntest')
  
  def do_exit(self, line):
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    
  def emptyline(self):
    pass
    
  def do_slowtext(self, line):
    self.parent.slowtext(line + '\n')
  
  def do_cd(self,line):
    try:
      os.chdir(line)
    except:
      print('cd: O diretório \"%s\" não existe.' % line)
    else:
      self.stdout.prompt = os.getcwd() + '> '
    
  def do_shell(self, line):
    print(subprocess.check_output(line, shell=True).decode('utf-8'))

  def print_topics(self, header, cmds, cmdlen, maxcol):
    if header is not None:
      Cmd.print_topics(self, header, cmds, cmdlen, maxcol)

'''
if __name__ == '__main__':
  print "blorp"
  Cli().cmdloop()
'''
