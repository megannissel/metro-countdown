#!/usr/bin/env python
# Display a runtext with double-buffering.
from base import BaseLED
from rgbmatrix import graphics

import time

import wmata

class RunText(BaseLED):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        canvas, large_font, small_font = self._set_screen_params()

        while True:
            strings = wmata.get_relevant_info()
            canvas.Clear()
            if len(strings) < 1:
                time.sleep(50)
                continue
            top_line, top_time = strings[0]
            color = self._set_color(top_line)
            top_string = top_line + " " + (str(top_time))
            length = graphics.DrawText(canvas, small_font, 0,  7, color, top_string)
            if len(strings) > 1:
                bottom_line, bottom_time = strings[1]
                color = self._set_color(bottom_line)
                bottom_string = bottom_line + " " + (str(bottom_time))
                length = graphics.DrawText(canvas, small_font, 0,  15, color, bottom_string)

            canvas = self.matrix.SwapOnVSync(canvas)

            time.sleep(65)

    def _set_screen_params(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        large_font = graphics.Font()
        large_font.LoadFont("../../fonts/7x14.bdf")
        small_font = graphics.Font()
        small_font.LoadFont("../../fonts/6x10.bdf")
        return offscreen_canvas, large_font, small_font

    def _set_color(self, line):
        color_map = {
            'GR': (0, 255, 0),
            'YL': (255, 255, 0),
            'RD': (255, 0, 0),
            'BL': (0, 255, 255),
            'OR': (255, 140, 0),
            'SV': (192, 192, 192)
        }
        if line in color_map:
            r, g, b = color_map[line]
            color = graphics.Color(r, g, b)
        else:
            color = graphics.Color(255, 0, 255)
        return color

if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
