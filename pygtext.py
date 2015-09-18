# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame, string

#pygfile for pygame printing
#source: https://www.cs.unc.edu/~gb/blog/2007/11/16/python-file-like-object-for-use-with-print-in-pygame/
class Pygfile(object):
  def __init__(self, font=None, maxlength=-1, prompt_enable=True, parent=None):
    if font is None:
      font = pygame.font.SysFont('monospace', 10)
    self.font = font
    self.buff = []
    #self.restricted = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&\\\'()*+,-./:;<=>?@[\]^_`{|}~'
    self.prompt_enable = prompt_enable
    self.parent = parent
    
    inkey   = '123457890-=/;\'[]\\'
    shifted = '!@#$%&*()_+?:\"{}|'
    try:
      self.table = str.maketrans(inkey,shifted)
    except:
      self.table = string.maketrans(inkey,shifted)
    
  def write(self, text):
    self.buff.append(text)
    
  def flush(self):
    pass

  def _splitline(self, text, maxwidth):
    '''A helper to split lines so they will fit'''
    w,h = self.font.size(text)
    if w < maxwidth:
      return [ text ]
    n0 = 0
    n1 = len(text)
    while True:
      ng = (n0 + n1) // 2
      if ng == n0:
        break
      w,h = self.font.size(text[0:ng])
      if w < maxwidth:
        n0 = ng
      else:
        n1 = ng
    return [ text[0:ng] ] + self._splitline(text[ng:], maxwidth)
        

  def display(self, surf):
    '''Show the printed output on the given surface'''
    # get the size of the target surface
    w,h = surf.get_size()
    # join all the writes together into one string
    text = ''.join(self.buff)
    if self.prompt_enable: text = text + self.parent.terminal.makeprompt(self.parent.cursor_state)
    # and split it into lines
    lines = text.split('\n')
    # bust up any long lines into pieces that fit
    slines = []
    for line in lines:
      slines = slines + self._splitline(line, w)
    lines = slines
    # get the vertical space between lines
    ls = self.font.get_linesize()
    # compute the maximum number of lines that will fit
    nlines = h // ls
    # throw away lines that have scrolled off the display
    lines = lines[-nlines:]
    # render them to the surface
    sy = 0
    for line in lines:
      ts = self.font.render(line, True, (255,255,255), (0,0,0))
      surf.blit(ts, (0, sy))
      sy += ls

  def clear(self):
    '''Clear the buffer (and thus the display)'''
    self.buff = []

def shifted(char, table):
    return char.translate(table).upper()
