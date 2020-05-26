import pyautogui as gui
import time

n = 1
position = []
try:
    while True:
        point = gui.position()
        if position:
            if point == position[-1]:
                position.append(point)
                if len(position) == 16:
                    gui.click(point[0], point[1], button='right')
                    position.clear()
                    n += 1
            else:
                position.clear()
        else:
            position.append(point)
        time.sleep(10)

except KeyboardInterrupt:
    print('Done.')
