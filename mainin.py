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

def draw_text_with_outline(draw, text, position, font, text_color, outline_color):
    x, y = position
    # Рисуем обводку
    for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
        draw.text((x+dx, y+dy), text, font=font, fill=outline_color)
    
    # Рисуем основной текст
    draw.text((x, y), text, font=font, fill=text_color)

try:
    disp = OLED_1in51.OLED_1in51()

    logging.info("\r1.51inch OLED ")
    disp.Init()
    
    # Увеличьте контраст
    disp.contrast(200)
    
    logging.info("clear display")
    disp.clear()

    # Create a rotated image
    image1 = Image.new('1', (disp.height, disp.width), "BLACK")
    draw = ImageDraw.Draw(image1)
    font1 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)  # Увеличенный размер шрифта

    while True:
        current_time = datetime.now().strftime("%H:%M:%S")

        # Очистка дисплея
        draw.rectangle((0, 0, disp.height, disp.width), fill="BLACK")

        # Получение размера текста
        text_width, text_height = draw.textsize(current_time, font=font1)

        # Расчет позиции для центрирования
        x = (disp.height - text_width) // 2
        y = (disp.width - text_height) // 2

        # Рисование текста с обводкой
        draw_text_with_outline(draw, current_time, (x, y), font1, "WHITE", "BLACK")

        # Поворот изображения
        rotated_image = image1.rotate(90, expand=True)

        # Отображение повернутого изображения
        disp.ShowImage(disp.getbuffer(rotated_image))

        time.sleep(1)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    disp.module_exit()
    exit()
