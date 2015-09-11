#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__':
  from pygame.locals import *
  import pygame, string
  import sys
  import cli
  import pygtext

  pygame.init()
  pygame.display.init()
  screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
  font = pygame.font.SysFont("monospace", 16)
  terminal = cli.Cli()

  sys.stdout = fp = pygtext.pygfile(font)
  terminal.stdout  = sys.stdout

  while True:
    # watch for QUIT events
    events = pygame.event.get()
    for event in events:
      if event.type == pygame.QUIT:
        break
      elif event.type == KEYDOWN:
        if event.key == K_RETURN:
          fp.buff += [fp.value, '\n']
          terminal.onecmd(fp.value)
          fp.value = ''
    fp.updateinput(events)
    # clear the image to black
    screen.fill((0,0,0))
    # show it on the screen
    fp.display(screen)
    pygame.display.flip()

