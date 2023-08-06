# coding=utf-8 
import sys
from turtle import *  # @UnusedWildImport
import svgwrite
from svg_turtle import SvgTurtle

mmttnnbb_drawing = svgwrite.Drawing("test.svg", size=('500px', '500px'))
mmttnnbb_drawing.add(mmttnnbb_drawing.rect(fill='white', size=('100%', '100%')))
mmttnnbb_t = SvgTurtle(mmttnnbb_drawing)
Turtle._screen = mmttnnbb_t.screen
Turtle._pen = mmttnnbb_t

# your code #

mmttnnbb_drawing.save()