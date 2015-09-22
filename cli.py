# -*- coding: utf-8 -*-

from pygame.locals import *
from cmd import Cmd
import argparse, sys, os, subprocess
import pygame

class Cli(object):
  def __init__(self, parent=None):
    self.parent = parent
    sys.stdout = parent.stdout
    self.cmdbuf = []
    self.cmdbuf_index = 0
    self.prompt = '> '
    self.value = ''
    self.shift = False
    self.ctrl = False
    self.parser = Parser(self)
    
    inkey   = '123457890-=/;\'[]\\'
    shifted = '!@#$%&*()_+?:\"{}|'
    try:
      self.table = str.maketrans(inkey,shifted)
    except:
      self.table = string.maketrans(inkey,shifted)
  
  def makeprompt(self, cursor):
    return self.makepath() + self.prompt + self.value + ('_' if cursor else ' ')
    
  def makepath(self, path='', absolute=False):
    return os.path.normpath(os.path.join(os.getcwd() if absolute else '', self.parent.curdir, path))
    
  def chpath(self, path):
    self.parent.curdir = os.path.normpath(os.path.join(self.parent.curdir, path))
  
  def parse(self, inp):
    spl = inp.split(' ')
    command = spl[0]
    args = spl[1:]
    if command == '': command = 'emptyline'
    else: command = 'do_' + command
    try:
      function = getattr(self.parser, command)
    except:
      #print('Comando não reconhecido')
      function = getattr(self.parser, 'shell')
      function(inp)
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
          if event.key in range(32,126): self.value += chr(event.key).translate(self.table).upper()
    #if len(self.value) > self.maxlength and self.maxlength >= 0: self.value = self.value[:-1]
    
class Parser(object):
  def __init__(self, parent=None):
    self.parent = parent
  
  def do_exit(self, args):
    pygame.event.post(pygame.event.Event(pygame.QUIT))
  
  #slowtext
  #isso é mais pra debug, tirar no jogo final
  def do_slowtext(self, args):
    self.parent.parent.slowtext(' '.join(args) + '\n')
  
  #change directory
  #checa por .pass dentro do diretório para 'senha'
  def do_cd(self, args):
    if len(args) < 1:
      #implementar cd sem argumento
      return
    cdpath = self.parent.makepath(args[0])
    passfile = os.path.join(cdpath, '.pass')
    if os.path.isfile(passfile):
      with open(passfile, 'r') as f:
        password = f.read().split('\n')[0]
      if len(args) < 2 or args[1] != password:
        print('Senha incorreta!')
        return
    if os.path.isdir(cdpath) and os.path.dirname(os.path.relpath(cdpath,os.getcwd()))[0:2] != '..':
      self.parent.chpath(args[0])
    else:
      print('cd: O diretório \"%s\" não existe.' % args[0])
  
  def emptyline(self, args):
    pass
    
  def shell(self, line):
    try:
      output = subprocess.check_output(line, shell=True, timeout=2, stderr=subprocess.STDOUT, cwd=self.parent.makepath(absolute=True))
    except subprocess.CalledProcessError as exc:
      print(exc.output.decode('UTF-8'))
    else:
      print(output.decode('UTF-8'))
