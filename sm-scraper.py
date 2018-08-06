import pyautogui
import keyboard
from time import sleep
import os

tlx = 242
tly = 137
sx = 1040
sy = 817
count = 100
storenum = '1954'
os.mkdir(storenum)
os.chdir(storenum)
filename = storenum + "-" + str(count) + ".png"
pyautogui.click(200, 15)
pyautogui.click(sx, sy)

pic = pyautogui.screenshot(region=(tlx, tly, 501, 689))
sleep(1)
pic.save(filename)

for i in range(19):
    count = count + 1
    filename = storenum + "-" + str(count) + ".png"
    pyautogui.click(sx, sy)
    pic = pyautogui.screenshot(region=(tlx, tly, 501, 689))
    sleep(1)
    pic.save(filename)
