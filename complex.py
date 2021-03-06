#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame, string
import sys, os
# local
import cli, pygtext

# event constants
USEREVENT_BLINK_CURSOR = USEREVENT

class Game:
  def __init__(self):
    pygame.init()
    pygame.display.init()
    self.screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont('monospace', 18)
    pygame.key.set_repeat(200,50)
    sys.stdout = self.stdout = pygtext.Pygfile(font, parent=self)
    
    self.terminal = cli.Cli(self)
    self.cursor_state = True
    
    self.basedir = 'sabesp'
    self.curdir = ''
    os.chdir(self.basedir)
  
  def slowtext(self, text):
    self.stdout.prompt_enable = False
    for c in text:
      self.stdout.write(c)
      self.stdout.display(self.screen)
      pygame.display.flip()
      pygame.time.wait(20 if c != '.' else 500)
    self.stdout.prompt_enable = True

  def main(self, argv):
    cursor_state = True
    pygame.time.set_timer(USEREVENT_BLINK_CURSOR, 500)

    while True:
      # watch for events
      events = pygame.event.get()
      for event in events:
        if event.type == QUIT:
          return
        elif event.type == USEREVENT_BLINK_CURSOR:
          self.terminal.cursor = '_' if self.cursor_state else ' '
          self.cursor_state = not self.cursor_state
      self.terminal.updateinput(events)
      # clear the image to black
      self.screen.fill((0,0,0))
      # show it on the screen
      self.stdout.display(self.screen)
      pygame.display.flip()

if __name__ == '__main__':
  game = Game()
  game.main(sys.argv[1:])
