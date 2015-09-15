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
    self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    font = pygame.font.SysFont('monospace', 12)
    pygame.key.set_repeat(200,50)
    self.terminal = cli.Cli(self)

    sys.stdout = self.stdout = pygtext.Pygfile(font)
    self.terminal.stdout  = self.stdout
    self.stdout.prompt = os.getcwd() + '> '
    self.terminal
  
  def slowtext(self, text):
    self.stdout.prompt_enable = False
    for c in text:
      self.stdout.write(c)
      pygame.time.wait(50)
      self.stdout.display(self.screen)
      pygame.display.flip()
    self.stdout.prompt_enable = True

  def main(self, argv):
    cursor_state = True
    pygame.time.set_timer(USEREVENT_BLINK_CURSOR, 500)

    self.slowtext('hello player!\n')

    while True:
      # watch for events
      events = pygame.event.get()
      for event in events:
        if event.type == QUIT:
          return
        elif event.type == KEYDOWN:
          if event.key == K_RETURN:
            # add input to buffer, send input to terminal, clear input
            self.stdout.buff += [self.stdout.prompt + self.stdout.value, '\n']
            self.terminal.onecmd(self.stdout.value)
            self.stdout.value = ''
        elif event.type == USEREVENT_BLINK_CURSOR:
          self.stdout.cursor = '_' if cursor_state else ' '
          cursor_state = not cursor_state
      self.stdout.updateinput(events)
      # clear the image to black
      self.screen.fill((0,0,0))
      # show it on the screen
      self.stdout.display(self.screen)
      pygame.display.flip()

if __name__ == '__main__':
  game = Game()
  game.main(sys.argv[1:])
