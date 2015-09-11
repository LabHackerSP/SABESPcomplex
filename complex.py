#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__':
  import sys
  import cli
  import pygame
  import pygtext

  pygame.init()
  pygame.display.init()
  screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
  font = pygame.font.SysFont("monospace", 15)
  terminal = cli.Cli()

  sys.stdout = fp = pygtext.pygfile()
  terminal.stdout  = sys.stdout

  while True:
    # watch for QUIT events
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
      break
    # clear the image to black
    screen.fill((0,0,0))
    # show it on the screen
    fp.display(screen)
    pygame.display.flip()

