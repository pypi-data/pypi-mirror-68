import os
import colorama
from colorama import Fore
from colorama import Style

colorama.init()

def clear():
    os.system('cls')
    print(Style.RESET_ALL)

def printlocation(path, a, b, inp):
    clear()

    global globpath
    globpath = str(path)
    path = str(path)

    global globarr
    arr = os.listdir(path)
    globarr = arr

    global globinp
    globinp = inp

    global aa
    aa = a

    global bb
    bb = b

def txt(txt, color, confirm):
    global conf
    conf = confirm
    loop1 = str('false')
    while loop1 == str('false'):

        arr = globarr
        a = aa
        b = bb
        inp = globinp
        path = globpath

        for list in arr:3
            number = str(arr.index(list) +1)
            print(a + str(arr.index(list) +1) + b, end='')
            print("", list)

        if inp != "txt":
            print(Fore.RED + '[ERROR] ' + Fore.WHITE + 'To use'+ fore_color + ' FileSelector.txt(Txt, color)' + Fore.WHITE + ' you have to set usrinput to true in' + fore_color + ' FileSelector.PrintLocation(path, a, b, txt)' + Fore.WHITE)
            return
        user_color = color.upper()
        colorama.init()
        fore_color = eval(f"Fore.{user_color}")
        usrinput = input(fore_color + txt + Fore.WHITE +" ")

        if not usrinput.isdigit():
            clear()
            print(Fore.RED + "[ERROR]", fore_color + "<"+ usrinput +">" + Fore.WHITE + " Is not a valid input")
            continue

        if int(usrinput) > 0:
            if int(usrinput) < int(number) + 1:
                if str(confirm) == str('true'):
                    usrinput2 = input(Fore.WHITE + "You've picked " + fore_color + usrinput + Fore.WHITE + ' You Sure? Y/n > ' + fore_color +'')
                    if usrinput2 == str('Y'):
                        clear()

                    elif usrinput2 == str('n'):
                        clear()
                        continue
                    else:
                        clear()
                        print(Fore.RED + "[ERROR]", Fore.CYAN + "<"+ usrinput2 +">" + Fore.WHITE + " Is not a valid input")
                        continue
                else:
                    clear()

                if int(usrinput) < int(number) + 1:
                    filepath1 = arr[int(usrinput) - 1]
                    filepath1 = path +'/'+ filepath1
                    global filepath
                    filepath = filepath1
                    break
                    clear()

        clear()
        print(Fore.RED + "[ERROR]", Fore.CYAN + "<"+ usrinput +">" + Fore.WHITE + " Is not a valid input")
        continue

#def keyboard(up, down, select, reset, confirm):
#    loop1 = "true"
#    while loop1 == "true":
#        key = ord(getch())
#        if key == up:
#            print('up')
#        elif key == down:
#            print('down')
#        elif key == select:
#            print('sel')
#        elif key == reset:
#            print('res')
#        elif key == 27:
#            break

def output():
    filepath
