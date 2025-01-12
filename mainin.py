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
from datetime import datetime
from waveshare_OLED import OLED_1in51
from PIL import Image, ImageDraw, ImageFont
logging.basicConfig(level=logging.DEBUG)

try:
    disp = OLED_1in51.OLED_1in51()

    logging.info("\r1.51inch OLED ")
    disp.Init()
    
    # Увеличьте яркость дисплея
    disp.SetContrast(255)  # Максимальная яркость
    
    logging.info("clear display")
    disp.clear()

    # Create a rotated image with higher resolution
    image1 = Image.new('1', (disp.height, disp.width), "WHITE")
    draw = ImageDraw.Draw(image1)
    
    # Используйте более крупный и четкий шрифт
    font1 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)  # Увеличен размер шрифта

    while True:
        current_time = datetime.now().strftime("%H:%M:%S")

        # Clear the display
        draw.rectangle((0, 0, disp.height, disp.width), fill="WHITE")

        # Get text size
        text_width, text_height = draw.textsize(current_time, font=font1)

        # Calculate position to center the text
        x = (disp.height - text_width) // 2
        y = (disp.width - text_height) // 2

        # Draw the rotated time with increased contrast
        draw.text((x, y), current_time, font=font1, fill=0)

        # Rotate the image
        rotated_image = image1.rotate(90, expand=True)

        # Display the rotated image
        disp.ShowImage(disp.getbuffer(rotated_image))

        time.sleep(1)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    disp.module_exit()
    exit()
