#! python3
'''
Display the mouse cursor's current position.
'''
import pyautogui as gui
print('Press Ctrl-C to quit.')
try:
    while True:
        x, y = gui.position()
        positionStr = 'X:' + str(x).rjust(4) + ' Y:' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\nDone.')
