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
    font = pygame.font.SysFont('monospace', 12)
    pygame.key.set_repeat(200,50)
    self.terminal = cli.Cli(self)

    sys.stdout = self.stdout = pygtext.Pygfile(font, parent=self)
    self.terminal.stdout = self.stdout
    self.stdout.prompt = os.getcwd() + '> '
    self.cursor_state = True
  
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

    #self.slowtext('hello player... this is a really long text. see you later..... bye now!\n')

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
