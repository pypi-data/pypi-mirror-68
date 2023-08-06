"""
qtUtils:

utility functions that use PySide2
"""


import platform


from PySide2.QtCore import Qt
from PySide2.QtGui import QColor

from vsutillib.macos import isMacDarkMode

from .SvgColor import SvgColor


def checkColor(color, isDarkMode=False):

    if color is None:

        if isMacDarkMode() or isDarkMode:
            color = SvgColor.white
        else:
            color = SvgColor.black

    elif isMacDarkMode():

        if color == SvgColor.red:
            color = SvgColor.magenta
        elif color == SvgColor.darkgreen:
            color = SvgColor.green
        elif color == SvgColor.blue:
            color = SvgColor.cyan

    elif not isDarkMode:

        if color == SvgColor.cyan:
            color = SvgColor.dodgerblue
        elif color == QColor(42, 130, 218):
            color = SvgColor.dodgerblue

    return color


class LineOutput:

    Color = "color"
    ReplaceLine = "replaceLine"
    AppendLine = "appendLine"
    AppendEnd = "appendEnd"
