#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

#pygfile for pygame printing
#source: https://www.cs.unc.edu/~gb/blog/2007/11/16/python-file-like-object-for-use-with-print-in-pygame/
class pygfile(object):
    def __init__(self, font=None):
        if font is None:
            font = pygame.font.SysFont('monospace', 10)
        self.font = font
        self.buff = []
    
    def write(self, text):
        self.buff.append(text)

    def _splitline(self, text, maxwidth):
        '''A helper to split lines so they will fit'''
        w,h = self.font.size(text)
        if w < maxwidth:
            return [ text ]
        n0 = 0
        n1 = len(text)
        while True:
            ng = (n0 + n1) / 2
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
        nlines = h / ls
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
        
'''class pygame_print:
  def __init__(self, *args):
    self.y = 10
    self.font = font
    
  def write(self, text):
    label = self.font.render(text, 1, (255,255,255))
    screen.blit(label, (10, self.y))
    pygame.display.flip()
    self.y+=15'''

