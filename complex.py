#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import cli
import pygame

pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
font = pygame.font.SysFont("monospace", 15)

class pygame_print:
  def __init__(self, *args):
    self.y = 10
    self.font = font
    
  def write(self, text):
    label = self.font.render(text, 1, (255,255,255))
    screen.blit(label, (10, self.y))
    pygame.display.flip()
    self.y+=15

test = cli.Cli()

sys.stdout = pygame_print(sys.stdout)
test.stdout  = sys.stdout
test.cmdloop()
