#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame, string
import sys, codecs  
# local
import cli, pygtext

# event constants
USEREVENT_BLINK_CURSOR = USEREVENT

def main(argv):
  pygame.init()
  pygame.display.init()
  screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
  font = pygame.font.SysFont('monospace', 12)
  pygame.key.set_repeat(200,50)
  terminal = cli.Cli()

  sys.stdout = fp = pygtext.pygfile(font)
  #sys.stdout = codecs.getwriter('utf8')(sys.stdout)
  terminal.stdout  = sys.stdout

  cursor_state = True
  pygame.time.set_timer(USEREVENT_BLINK_CURSOR, 500)
  while True:
    # watch for events
    events = pygame.event.get()
    for event in events:
      if event.type == QUIT:
        return
      elif event.type == KEYDOWN:
        if event.key == K_RETURN:
          # add input to buffer, send input to terminal, clear input
          fp.buff += [fp.prompt + fp.value, '\n']
          terminal.onecmd(fp.value)
          fp.value = ''
      elif event.type == USEREVENT_BLINK_CURSOR:
        fp.cursor = '_' if cursor_state else ' '
        cursor_state = not cursor_state
    fp.updateinput(events)
    # clear the image to black
    screen.fill((0,0,0))
    # show it on the screen
    fp.display(screen)
    pygame.display.flip()

if __name__ == '__main__':
  main(sys.argv[1:])
