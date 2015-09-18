# -*- coding: utf-8 -*-

from pygame.locals import *
from cmd import Cmd
import argparse, sys, os
import pygame

class Cli(object):
  def __init__(self, parent=None):
    self.parent = parent
    sys.stdout = parent.stdout
    self.cmdbuf = []
    self.cmdbux_index = 0
    self.value = ''
    self.prompt = '> '
    self.value = ''
    self.shift = False
    self.ctrl = False
    #self.maxlength = maxlength
    print('TEST!')
    self.parent.slowtext('teeeeeeest\n')
    self.parser = Parser(self)
  
  def makeprompt(self, cursor):
    return self.prompt + self.value + ('_' if cursor else ' ')
  
  def parse(self, inp):
    spl = inp.split(' ')
    command = spl[0]
    args = spl[1:]
    try:
      function = getattr(self.parser, command)
    except:
      print('Comando não reconhecido')
    else:
      function(args)
  
  def updateinput(self, events):
    '''Update the input based on passed events'''
    for event in events:
      if event.type == KEYUP:
        if event.key == K_LSHIFT or event.key == K_RSHIFT: self.shift = False
        if event.key == K_LCTRL or event.key == K_RCTRL: self.ctrl = False
      if event.type == KEYDOWN:
        if event.key == K_RETURN:
          # add input to buffer, send input to terminal, clear input
          self.cmdbuf = [ self.value ] + self.cmdbuf
          self.cmdbuf_index = 0
          print(self.makeprompt(False))
          #self.terminal.onecmd(self.stdout.value)
          self.parse(self.value)
          self.value = ''
        elif event.key == K_UP:
          self.cmdbuf_index += 1 if self.cmdbuf_index < len(self.cmdbuf) else 0
          self.value = self.cmdbuf[self.cmdbuf_index - 1] if len(self.cmdbuf) > 0 else ''
        elif event.key == K_DOWN:
          self.cmdbuf_index -= 1 if self.cmdbuf_index > 0 else 0
          self.value = self.cmdbuf[self.cmdbuf_index - 1] if self.cmdbuf_index > 0 else ''
        elif event.key == K_BACKSPACE: self.value = self.value[:-1]
        elif event.key == K_LSHIFT or event.key == K_RSHIFT: self.shift = True
        elif event.key == K_LCTRL or event.key == K_RCTRL: self.ctrl = True
        if self.ctrl:
          # ctrl-c clears input line
          if event.key == K_c: self.value = ''
        elif not self.shift:
          if event.key in range(32,126): self.value += chr(event.key)
        elif self.shift:
          if event.key in range(32,126): self.value += shifted(chr(event.key), self.table)
    #if len(self.value) > self.maxlength and self.maxlength >= 0: self.value = self.value[:-1]
    
class Parser(object):
  def __init__(self, parent=None):
    self.parent = parent
    
  def exit(self):
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    
  def slowtext(self,args):
    self.parent.parent.slowtext(' '.join(args) + '\n')
  
  def cd(self,args):
    if os.path.isfile(args[0] + '/.pass'):
      with open(args[0] + '/.pass', 'r') as f:
        password = f.read()
      if len(inp) < 2 or args[1] != password:
        print('Senha incorreta!')
        return
    try:
      os.chdir(args[0])
    except:
      print('cd: O diretório \"%s\" não existe.' % args[0])
    else:
      self.prompt = os.getcwd() + '> '

class OldCli(Cmd):
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
    inp = line.split(' ')
    if os.path.isfile(line + '/.pass'):
      with open(line + '/.pass', 'r') as f:
        password = f.read()
      if len(inp) < 2 or inp[1] != password:
        print('Senha incorreta!')
        return
    try:
      os.chdir(inp[0])
    except:
      print('cd: O diretório \"%s\" não existe.' % line)
    else:
      self.stdout.prompt = os.getcwd() + '> '
    
  def do_shell(self, line):
    print(subprocess.check_output(line, shell=True).decode('utf-8'))

  def print_topics(self, header, cmds, cmdlen, maxcol):
    if header is not None:
      Cmd.print_topics(self, header, cmds, cmdlen, maxcol)
