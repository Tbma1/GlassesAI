#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import time
import traceback
from datetime import datetime  # Import datetime module
from waveshare_OLED import OLED_1in51
from PIL import Image, ImageDraw, ImageFont
logging.basicConfig(level=logging.DEBUG)

try:
    disp = OLED_1in51.OLED_1in51()

    logging.info("\r1.51inch OLED ")
    # Initialize library.
    disp.Init()
    # Clear display.
    logging.info("clear display")
    disp.clear()

    # Create blank image for drawing.
    image1 = Image.new('1', (disp.width, disp.height), "WHITE")  # Use the correct width and height
    draw = ImageDraw.Draw(image1)
    font1 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)  # Increase font size

    while True:
        # Get the current time
        current_time = datetime.now().strftime("%H:%M:%S")

        # Clear the display
        draw.rectangle((0, 0, disp.width, disp.height), fill="WHITE")

        # Draw the time horizontally
        draw.text((0, 0), current_time, font=font1, fill=0)

        # Display the image
        disp.ShowImage(disp.getbuffer(image1))

        # Refresh the display every second
        time.sleep(1)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    disp.module_exit()
    exit()
