import pyautogui as gui
import time

a = 1
while a:
    time.sleep(2)
    x = 175
    y = 155
    for i in range(20):
        gui.click(x, y, button='left')
        y += 23
    gui.click(482, 112, button='left')
    time.sleep(1)
    gui.click(918, 602, button='left')
    time.sleep(1)
    gui.click(923, 112, button='left')
    a += 1
    if a == 10:
        break