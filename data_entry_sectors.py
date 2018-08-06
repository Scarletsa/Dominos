import pyautogui
import keyboard
import pandas as pd
import sys
from time import sleep

def main(store):
    pyautogui.PAUSE = 1
    horpx = 281
    vertpx = 119
    sectors_filename = 'Sectors_'+str(store)+'.csv'
    streets_filename = 'Streets_'+str(store)+'.csv'
    df1 = pd.read_csv(sectors_filename)
    df2 = pd.read_csv(streets_filename)
    df = pd.merge(df1, df2, on='street name', how='outer')
    df = df.dropna().drop_duplicates()
    df = df.sort_values(by=['sector', 'street name', 'starting', 'ending'])
    print(df)
    rows = len(df.index)
    for index, row in df.iterrows():
        sector, sn, starting, ending, parity, down = row

        sn = sn.replace("E ", "").replace("N ", "").replace("S ", "").replace("W ", "") # .replace("East", "").replace("South", "").replace("West", "")
        pyautogui.click(horpx, vertpx)
        sleep(0.5)
        pyautogui.click(horpx - 76, vertpx + 45)
        print(str(index) + "/" + str(rows))
        print(str(sector))
        keyboard.write(str(sector))
        sleep(0.5)
        keyboard.press_and_release('tab')
        sleep(0.5)
        print(sn)
        if ('7 Pines' in sn):
            print('r')
            keyboard.write('r')
            sleep(0.5)
        elif ('Broadway Ave (Brooklyn Park' in sn):
            print('v')
            keyboard.write('v')
            sleep(0.5)
        elif ('River Rd (Brooklyn Park' in sn):
            print('v')
            keyboard.write('v')
            sleep(0.5)
        elif ('River Rd (Champlin' in sn):
            print('v')
            keyboard.write('v')
            sleep(0.5)
        elif ('Oaks Dr' in sn):
            print('m')
            keyboard.write('m')
            sleep(0.5)
        elif ('Pond Trail' in sn):
            print('r')
            keyboard.write('r')
            sleep(0.5)
        # if (sn[0].isdigit()):
        #     sleep(0.5)
        # if (sn[0] == 'E'):
        #     print('d')
        #     keyboard.write('d')
        #     sleep(0.5)
        # elif (sn[0] == 'M'):
        #     print('l')
        #     keyboard.write('l')
        #     sleep(0.5)
        elif (sn[0] == 'N'):
            print('m')
            keyboard.write('m')
            sleep(0.5)
        elif (sn[0] == 'S'):
            print('r')
            keyboard.write('r')
            sleep(0.5)
        elif (sn[0] == 'W'):
            print('v')
            keyboard.write('v')
            sleep(0.5)
        else:
            print(sn[0])
            keyboard.write(sn[0])
            sleep(0.5)
        print(int(down))
        for i in range(int(down)):
            keyboard.press_and_release('down')
            sleep(0.5)
        keyboard.press_and_release('tab')
        sleep(0.5)
        print(int(starting))
        keyboard.write(str(int(starting)))
        sleep(0.5)
        keyboard.press_and_release('tab')
        sleep(0.5)
        print(int(ending))
        keyboard.write(str(int(ending)))
        sleep(0.5)
        keyboard.press_and_release('tab')
        sleep(0.5)
        print(int(parity))
        for i in range(int(parity)):
            keyboard.press_and_release('down')
            sleep(0.5)

    pyautogui.click(horpx - 76, vertpx + 45)

if __name__ == "__main__":
    main(sys.argv[1])
