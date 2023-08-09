import math
import copy

import openpyxl
import pandas as pd
import pynput
import screeninfo
import time
import tkinter
import pytesseract
from tkinter.font import Font
from mss import mss
from pynput.mouse import Controller, Button
import numpy as np
import pyautogui
import cv2
import paddleocr
import os
import re


class eventKeyboard():
    """
    pressed(key) is a internal function for key board listener, please do not
        invoke!
    NOTICE!!!  pressed(key) would check whether main program is down every 10 sec,
        to make it continous working, call activeFlagSet(newFlag=1) to reactive the working status.
        
    StartListener(): start the listener, also safe for any unterminate listener.
    terminate(): end the listener
    
    statusGet(): return listener status, 0 for initiated, 1 for started, >=2 for specific keys were pressed,
        -1 for terminated.
    """

    def __init__(self) -> None:

        self.keyValue = -1
        self.timeIntervalStart = 0
        self.timeIntervalEnd = 0

        self.keysIntervalStart = 0
        self.keysIntervalEnd = 0

        self.activeFlag = -1
        self.keyPressed = pynput.keyboard.Listener(on_press=self.pressed, on_release=self.released)
        self.counter = 0
        # self.shortcutThread = False

        self.__status = 0
        self.shortcutFlag = False
        self.recordKey = []
        self.recordedshortcut = {"Key.alt_lz": 2}  # Key.alt_lz is default shortcut

        self.keyboard_key_dict = {
            "\x01": ['ctrl', 'a'],
            "\x02": ['ctrl', 'b'],
            "\x03": ['ctrl', 'c'],
            "\x04": ['ctrl', 'd'],
            "\x05": ['ctrl', 'e'],
            "\x06": ['ctrl', 'f'],
            "\x07": ['ctrl', 'g'],
            "\x08": ['ctrl', 'h'],
            "\t": ['ctrl', 'i'],
            "\n": ['ctrl', 'j'],
            "\x0b": ['ctrl', 'k'],
            "\x0c": ['ctrl', 'l'],
            "\r": ['ctrl', 'm'],
            "\x0e": ['ctrl', 'n'],
            "\x0f": ['ctrl', 'o'],
            "\x10": ['ctrl', 'p'],
            "\x11": ['ctrl', 'q'],
            "\x12": ['ctrl', 'r'],
            "\x13": ['ctrl', 's'],
            "\x14": ['ctrl', 't'],
            "\x15": ['ctrl', 'u'],
            "\x16": ['ctrl', 'v'],
            "\x17": ['ctrl', 'w'],
            "\x18": ['ctrl', 'x'],
            "\x19": ['ctrl', 'y'],
            "\x1a": ['ctrl', 'z'],
            "\x1f": ['ctrl', 'shift', '-'],
            '<186>': ['ctrl', ';'],
            "<187>": ['ctrl', '='],
            "<189>": ['ctrl', '-'],
            "<192>": ['ctrl', '`'],
            "<222>": ['ctrl', r"'"],
            "<48>": ['ctrl', '0'],
            "<49>": ['ctrl', '1'],
            "<50>": ['ctrl', '2'],
            "<51>": ['ctrl', '3'],
            "<52>": ['ctrl', '4'],
            "<53>": ['ctrl', '5'],
            "<54>": ['ctrl', '6'],
            "<55>": ['ctrl', '7'],
            "<56>": ['ctrl', '8'],
            "<57>": ['ctrl', '9'],
            "~": ['shift', '`'],
            "!": ['shift', '1'],
            "@": ['shift', '2'],
            "#": ['shift', '3'],
            "$": ['shift', '4'],
            "%": ['shift', '5'],
            "^": ['shift', '6'],
            "*": ['shift', '7'],
            "(": ['shift', '8'],
            ")": ['shift', '9'],
            "_": ['shift', '-'],
            "+": ['shift', '='],
            ":": ['shift', ';'],
            "\'": ['shift', "'"],
            "<": ['shift', ","],
            "{": ['shift', "["],
            "}": ['shift', "]"],
            "|": ['shift', "\\"],
            "?": ['shift', "/"],
        }

    def pressed(self, key):
        try:
            self.recordKey.append("{}".format(key.char))
        except:
            self.recordKey.append("{}".format(key))
        # print(self.recordKey)

        if len(self.recordKey) == 2:
            # print("recordKey",self.recordKey[0])
            if self.recordKey[0] == "Key.ctrl_l" or self.recordKey[0] == "Key.ctrl_r":
                # print("---------------------")
                if self.recordKey[1] in self.keyboard_key_dict.keys():
                    # print(key)
                    # print("The recordKey is " + str(self.keyboard_key_dict[self.recordKey[1]]))
                    # print("Record the shortcut key.")
                    self.recordKey[1] = copy.copy(self.keyboard_key_dict[self.recordKey[1]][1])

            elif self.recordKey[0] == "Key.shift" or self.recordKey[0] == "Key.shift_r":
                # print("+++++++++++++++++++=")
                if self.recordKey[1] in self.keyboard_key_dict.keys():
                    # print("The recordKey is " + str(self.keyboard_key_dict[self.recordKey[1]]))
                    # print("Record the shortcut key.")
                    self.recordKey[1] = copy.copy(self.keyboard_key_dict[self.recordKey[1]][1])

            if self.shortcutFlag == False:
                # print("call target functions, not finished yet.")
                # else:
                #     # print(type(self.recordKey[0]))
                #     print("The recordKey is " + self.recordKey[0] + " + " + self.recordKey[1])
                #     print("Record the shortcut key.")
                #     print("sssssssssssssssssssssss")
                tem = self.recordKey[0] + self.recordKey[1]
                if tem in self.recordedshortcut.keys():
                    self.__status = self.recordedshortcut[tem]  # Change status if user triggered a shortcut

        if time.time() - self.timeIntervalStart > 10.0:
            if self.activeFlag == -1:  # check if main thread is active, if not, kill sub thread
                self.__status = -1
                return False
            else:
                self.activeFlag = -1
                self.timeIntervalStart = time.time()

    def released(self, key):
        try:
            tem = str(key.char)
        except:
            tem = str(key)

        if tem in self.keyboard_key_dict.keys():
            tem = self.keyboard_key_dict[tem][1]

        if self.shortcutFlag and len(self.recordKey) == 2:  # record shortcut
            if len(list(self.recordedshortcut.keys())) == 0:
                self.recordedshortcut[self.recordKey[0] + self.recordKey[1]] = 2
            else:
                if (self.recordKey[0] + self.recordKey[1]) not in self.recordedshortcut.keys():
                    self.recordedshortcut[self.recordKey[0] + self.recordKey[1]] = \
                        self.recordedshortcut[list(self.recordedshortcut.keys())[-1]] + 1
            # print(self.recordedshortcut)
            self.shortcutFlag = False

        # print("Released!!!",self.recordKey)
        # try:
        #     self.recordKey.remove("{}".format(key.char))
        # except:
        self.recordKey.remove("{}".format(tem))

        if time.time() - self.timeIntervalStart > 10.0:
            if self.activeFlag == -1:  # check if main thread is active, if not, kill sub thread
                self.__status = -1
                return False
            else:
                self.activeFlag = -1
                self.timeIntervalStart = time.time()
        # if key == pynput.keyboard.Key.esc: 
        #     return False

    def StartListener(self) -> None:

        if self.__status == -1:
            self.terminate()
            self.keyPressed = pynput.keyboard.Listener(on_press=self.pressed, on_release=self.released)

        self.__status = 1
        self.keyPressed.start()
        self.timeIntervalStart = time.time()
        self.begin = time.time() - 5

    def terminate(self) -> None:
        self.keyPressed.stop()

    def keyGet(self) -> str:
        return self.keyValue

    def activeFlagSet(self, flag) -> None:
        end = time.time()
        dif = end - self.begin
        if self.__status == -1:
            self.StartListener()
        elif dif >= 10.0:
            self.activeFlag = flag
            self.begin = time.time()

    def statusGet(self) -> int:
        result = self.__status
        if self.__status > 1:
            self.__status = 1

        return result


class eventMouse():
    """
    clicked(x,y) and moving(x,y) are internal functions for key board listener, please do not
        invoke!
    NOTICE!!!  clicked(x,y) and moving(x,y) would check whether main program is down every 10 sec,
        to make it continous working, call activeFlagSet(newFlag=1) to reactive the working status.
        
    StartListener(): start the listeners.
    terminate(): end the listeners.
    
    mouseGet(side): if side can be "left" or "right",return the x,y coordinate for last time mouse clicked

    motionGet(): return the x,y coordinate for last time mouse moved
    """

    def __init__(self) -> None:
        self.timeIntervalStart = 0
        self.timeIntervalEnd = 0

        self.activeFlag1 = -1
        self.activeFlag2 = -1

        self.__status1 = 0
        self.__status2 = 0

        self.DetectedMouseXPos = -1
        self.DetectedMouseYPos = -1

        self.DetectedRightMouseXPos = -1
        self.DetectedRightMouseYPos = -1

        self.timeIntervalStartMotion = 0
        self.timeIntervalEndMotion = 0
        self.MotionMouseXPos = -1
        self.MotionMouseYPos = -1

        # keyPressed.stop()
        self.mouseClicked = pynput.mouse.Listener(on_click=self.clicked)
        self.mouseMove = pynput.mouse.Listener(on_move=self.moving)

        # mouseClicked.join()

    def moving(self, x, y):
        self.MotionMouseXPos = x
        self.MotionMouseYPos = y

        self.timeIntervalEndMotion = time.time()
        if self.timeIntervalEndMotion - self.timeIntervalStartMotion > 10.0:
            # print("Times Up")
            if self.activeFlag2 == -1:
                # print("exit")
                self.__status2 = -1
                return False
            self.timeIntervalStartMotion = time.time()
            self.activeFlag2 = -1

    def clicked(self, x, y, button, pressed):

        if pressed and button.name == "left":
            self.DetectedMouseXPos = x
            self.DetectedMouseYPos = y
            # print(self.DetectedMouseXPos,self.DetectedMouseYPos)

        if pressed and button.name == "right":
            self.DetectedRightMouseXPos = x
            self.DetectedRightMouseYPos = y
            # print(self.DetectedRightMouseXPos,self.DetectedRightMouseYPos)

        self.timeIntervalEnd = time.time()

        # print(self.timeIntervalEnd-self.timeIntervalStart)
        if self.timeIntervalEnd - self.timeIntervalStart > 10.0:
            #             print("Times Up")
            if self.activeFlag1 == -1:
                #                 print("exit")
                self.__status1 = -1
                return False
            self.timeIntervalStart = time.time()
            self.activeFlag1 = -1
            # if x==0 or y ==0:
            #     self.detectFlag=False
            # self.terminate()
            # return True

        # return True

    def StartListener(self) -> None:

        if self.__status1 == -1 or self.__status2 == -1:
            self.terminate()
            self.mouseClicked = pynput.mouse.Listener(on_click=self.clicked)
            self.mouseMove = pynput.mouse.Listener(on_move=self.moving)

        self.timeIntervalStart = time.time()
        self.mouseClicked.start()

        self.timeIntervalStartMotion = time.time()
        self.mouseMove.start()

        self.begin = time.time() - 5

    def terminate(self) -> None:
        self.mouseClicked.stop()
        self.mouseMove.stop()

    def mouseGet(self, side) -> int:
        if side == "left":
            return self.DetectedMouseXPos, self.DetectedMouseYPos
        elif side == "right":
            return self.DetectedRightMouseXPos, self.DetectedRightMouseYPos

    def motionGet(self) -> int:
        return self.MotionMouseXPos, self.MotionMouseYPos

    def activeFlagSet(self, newFlag) -> None:
        end = time.time()
        dif = end - self.begin

        if self.__status1 == -1 or self.__status2 == -1:
            self.StartListener()
        elif dif >= 10:
            self.activeFlag1 = newFlag  # 检测点击的flag
            self.activeFlag2 = newFlag  # 检测移动的flag
            self.begin = time.time()


class windowsUI():
    """
    class parameters: 
        override: self defined tk windows, only set true when using screenShot mode or message box mode
        alpha: visibility of root window
        bgColor: background color, only root windows
        screenShot: mode flag, 1 for screenShot mode, 2 for main window mode, 3 for child windows on screenShot mode
        width,height: size of root window
        positionX,positionY: x,y for top left of window
        listener: mouse listener
        
        !!! Flag summary:
        self.statusID: 
            singel digit: the function ID for current view windows/panels
            ten digit: the view ID for current window/panel
            hundred digit: special digit repersent the main program status
            thousand digit: the ID of window/panel
            Example:
                1100:Start up screen shot
                    first "1" means root window
                    second "1" means the button has pressed and wait for event function to handle
                    first "0" means first view of root window
                    second "0" means the the button to Start up screen shot is on first view of root window
            
            detials:
            -1: standby flag
            "1100":Start up screen shot
            "2000":Screen shot mode
            
    """

    def __init__(self, override=False, alpha=0.5, bgColor="black", screenShot=-1, \
                 width=-1, height=-1, positionX=0, positionY=0, listener: eventMouse = None) -> None:
        # self.__timeList=[time.time(),0]
        self.listener = listener
        self.keyBoardInterrupt = eventKeyboard()
        self.screenShot = screenShot
        self.screen = screeninfo.get_monitors()[0]
        # print("22222222222222222222222333333333333333333333")
        self.mainPanelButtons = ({"Recognition Area Record": [1100], "Setting": [1101], "next page": [1102]},)
        # Store the buttons on main Panel and their status ID
        self.currentButton: list[tkinter.Button] = []
        self.currentLabel = []
        self.currentOtherComponents = []

        self.statusID = 1000  # globel status flag
        self.__subWindows = None  # store windows created by event function Start()

        self.__rec = []  # store rectangle in canvas
        self.recoredArea = []  # store recorded screen shot area
        self.x = -10  # store mouse click coordinations
        self.y = -10
        self.ocr = OCRController()

        self.xRight = -1  # store mouse move coordinations
        self.yRight = -1

        # self.__loopTime = 0  # use to count the time, 0.1s every loop
        self.__counter = 0  # status id for drawer function
        self.__root = tkinter.Tk()
        self.windowSize = {"root": [width, height], "screenShoter": [0, 0]}  # all type of window size

        self.width = width  # current use width and height
        self.height = height
        self.bgColor = bgColor
        self.alpha = alpha

        if self.screenShot == 1:
            self.__num = 6
            self.canvasPlace()

            if width == -1:
                self.width = self.__root.winfo_screenwidth()
            if height == -1:
                self.height = self.__root.winfo_screenheight()

            # self.__root.overrideredirect(override)
            # self.__root.attributes("-alpha", alpha)
        elif self.screenShot == 2:

            # temx=200*(1280/self.screen.width)
            # temy=70*(720/self.screen.height)
            # print(temx,temy)
            self.__root.title("Main panel")
            if width == -1:
                self.width = int(self.__root.winfo_screenwidth() / 5)
            if height == -1:
                self.height = int(self.width * 16 / 10)
            # print(self.width,self.height)
            self.layOutController()
        self.__root.overrideredirect(override)
        self.__root.attributes("-alpha", alpha)

        self.__root.geometry("{0}x{1}+{2}+{3}" \
                             .format(self.width, self.height, positionX, positionY))
        self.__root.configure(bg=bgColor)

        self.__root.resizable(0, 0)

        if self.listener != None:
            self.listener.StartListener()
        if self.screenShot != 1:
            self.keyBoardInterrupt.StartListener()  # listener to detect keyboard shortcut
        self.keeper()

        self.__root.mainloop()

    def layOutController(self, mode="root", view=0) -> None:
        if mode == "root":
            buttonNum = len(self.mainPanelButtons[view].keys())
            counter = 0
            for x in self.mainPanelButtons[view].keys():
                counter += 1
                tem = self.__lambdaCreater(self.mainPanelButtons[view][x][0])
                print(self.mainPanelButtons[view][x][0])
                self.currentButton.append(tkinter.Button(self.__root, text=x, command=tem))
                font = Font(font=self.currentButton[-1]["font"])  # get font information
                lineHeight = font.metrics("linespace")  # calculate hieght and weidth by font information
                lineWidth = font.measure(x)
                # print(lineHeight,lineWidth)
                # print()

                self.currentButton[-1].place(x=(self.width - lineWidth) / 2,
                                             y=counter * self.height / (buttonNum + 1) - lineHeight / 2)
        else:
            pass

    def __lambdaCreater(self, x):  # create lambda function for button, prevent shollow copy
        return lambda: self.Start(x)

    def screenShotCreation(self, alphaValue=0.5, bgColor="black") -> None:
        """_summary_

        Args:
            alphaValue (int): the visibility of the screen shot window
            bgColor (str): allow for user to custom the back ground color
        """

        print(type(self.listener))
        self.__subWindows = tkinter.Toplevel()  # set up sub window
        self.windowSize["root"] = [self.width, self.height]  # back up the size of root window
        self.width = self.__subWindows.winfo_screenwidth()  # make it large as the screen
        self.height = self.__subWindows.winfo_screenheight()

        self.__subWindows.overrideredirect(True)  # remove tk default component(e.g. window close button)
        self.__subWindows.attributes("-alpha", alphaValue)

        self.__subWindows.geometry("{0}x{1}+{2}+{3}" \
                                   .format(self.width, self.height, 0, 0))
        self.__subWindows.configure(bg=bgColor)
        self.__num = 6
        self.canvasPlace(target="sub")

        self.screenShot = 1
        print("Screenshoter setted up")
        if self.listener == None:
            self.listener = eventMouse()
            self.listener.StartListener()

    def Start(self, status):
        print("111111111111111111111111")
        print(status)
        # print("Start:",self.statusID)
        if status == 1100:  #
            self.screenShotCreation()
            # self.subWindows.append(windowsUI(True,0.5,"black",listener=mouseL,screenShot=3))
            # print("!!!!!!!!!!!!!!!!!!")
            self.__root.attributes("-alpha", 0)
            self.statusID = 2000
            # print("Start:",self.statusID)

    def keeper(self) -> None:
        # print("ID:",self.screenShot)
        print("Status:", self.statusID)
        self.keyBoardInterrupt.activeFlagSet(1)
        # print(self.__subWindows)
        if self.screenShot == 1:
            if self.drawer() == 1:
                self.__root.after(100, self.keeper)

        elif self.screenShot == 2:  # mian panel mode
            self.__root.after(100, self.keeper)

        # print(self.statusID==11)

        # print(self.keyBoardInterrupt.statusGet())
        if self.keyBoardInterrupt.statusGet() == 2:
            # print("ssssssssssssssss",self.statusID)
            if self.statusID == 2000:
                self.x = -10
                self.y = -10
                self.screenShot = 2
                self.__root.attributes("-alpha", self.alpha)

                for x in self.__rec:
                    self.recoredArea.append(self.transform(x))
                    print(self.transform(x))
                self.__rec.clear()
                self.__subWindows.destroy()
                self.listener.terminate()
                self.listener = None
                self.statusID = 1000

        if len(self.recoredArea) == 1:
            tem = self.recoredArea.pop()
            text = self.ocr.areTextTransfer(tem, r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789')
            text2 = self.ocr.areTextTransfer(tem, r'--oem 1 --psm 7')
            print(text)
            print(text2)
            print(self.recoredArea)

    def drawer(self) -> int:
        if self.listener != None:

            self.listener.activeFlagSet(1)

            if self.screenShot == 1 and self.__num > 0:  # 1是截图功能的id，number是多少个画了多少个矩形。
                temx, temy = self.listener.mouseGet("left")  # 鼠标的绝对坐标。

                temx = (temx * self.width) / self.screen.width  # 转换相对坐标。
                temy = (temy * self.height) / self.screen.height

                # print("call:",temx,temy)
                if self.x == -10 or self.y == -10:  # prevent first click detection
                    self.x = -1
                    self.y = -1
                elif temx != self.x or temy != self.y:  # 防止长度和宽度为0的矩形。
                    print("click:", temx, temy)
                    self.x, self.y = temx, temy
                    self.__counter += 1  # 初始是0，每点击一次加1。
                    if self.__counter == 1:  # 创捷一个新的正方形。
                        self.rectangleCreation(self.x, self.y, self.x, self.y, width=3)
                    else:
                        self.__counter = 0

                if self.__counter == 1:  # 正方形点击第一下该如何反应。
                    temx, temy = self.listener.motionGet()  # 检测鼠标移动坐标（绝对坐标）

                    temx = (temx * self.width) / self.screen.width  # 转换成相对坐标
                    temy = (temy * self.height) / self.screen.height

                    if (self.xRight == -1 and self.yRight == -1) \
                            or (temx != self.xRight or temy != self.yRight):  # xRight和yRight检测前一刻和后一刻一样不一样

                        print("move:", temx, temy)
                        self.xRight, self.yRight = temx, temy  # 鼠标当前位置
                        self.rectangleConfigure(self.x, self.y, self.xRight, self.yRight, width=3)  # 更新矩阵

        if self.x == 0 or self.y == 0:  # 退出
            self.listener.terminate()
            self.__root.destroy()
            return -1

        return 1

    def canvasPlace(self, positionX=0, positionY=0, highlightthickness=0, bgColor="black", target="root") -> None:

        if target == "sub":
            self.__canvas = tkinter.Canvas(self.__subWindows, highlightthickness= \
                highlightthickness, width=self.width, height=self.height, bg=bgColor)
        else:
            self.__canvas = tkinter.Canvas(self.__root, highlightthickness= \
                highlightthickness, width=self.width, height=self.height, bg=bgColor)
        self.__canvas.place(x=positionX, y=positionY)

    def rectangleCreation(self, positionX=0, positionY=0, rightX=0, rightY=0, outline="crimson", \
                          width=0, dash=(1, 1)) -> None:

        self.__rec.append(self.__canvas.create_rectangle(positionX, positionY, rightX, rightY, \
                                                         outline=outline, width=width, dash=dash))
        print("coor:", self.__canvas.coords(self.__rec[-1]))

    def rectangleConfigure(self, positionX=0, positionY=0, rightX=0, rightY=0, outline="crimson", \
                           width=0, index=-1, dash=(1, 1)) -> None:

        self.__canvas.itemconfigure(self.__rec[index], outline=outline, width=width, \
                                    dash=dash)

        self.__canvas.coords(self.__rec[index], positionX, positionY, rightX, rightY)
        print("coorMoving:", self.__canvas.coords(self.__rec[-1]))

        # self.__canvas.itemconfigure(self.__rec[index], outline=outline, width=width, \
        #                             dash=dash)

        # self.__canvas.coords(self.__rec[index], positionX, positionY, rightX, rightY)
        # print("coorMoving:", self.__canvas.coords(self.__rec[-1]))

    def transform(self, canvas_rectangle):  # 将画布上的相对坐标转换成屏幕的绝对坐标
        coords = self.__canvas.coords(canvas_rectangle)  # 得到矩阵的坐标
        tem_left_x = coords[0]
        tem_left_y = coords[1]
        tem_right_x = coords[2]
        tem_right_y = coords[3]

        tem_left_x = tem_left_x * self.screen.width / self.width  # 转换成绝对坐标
        tem_left_y = tem_left_y * self.screen.width / self.width
        tem_right_x = tem_right_x * self.screen.width / self.width
        tem_right_y = tem_right_y * self.screen.width / self.width

        monitor = {
            "top": int(tem_left_y),
            "left": int(tem_left_x),
            "width": int(tem_right_x - tem_left_x),
            "height": int(tem_right_y - tem_left_y)
        }

        return monitor


class mouse_control():
    def __init__(self):
        self.mouse = Controller()

    def move_and_press_mouse(self, x_position, y_position):
        self.mouse.position = (x_position, y_position)  # Move the mouse to the position
        time.sleep(0.1)
        self.mouse.press(Button.left)
        time.sleep(0.1)
        self.mouse.release(Button.left)

    def smooth(self, x_position, y_position, speed=150):
        position_xy = pyautogui.position()
        distance = math.sqrt(pow(x_position - position_xy[0], 2) + pow(y_position - position_xy[1], 2))
        print(distance)
        mouse_time = distance / speed
        print(mouse_time)
        pyautogui.moveTo(x_position, y_position, mouse_time)


class OCRController():
    def __init__(self) -> None:
        # pytesseract.pytesseract.tesseract_cmd = r""
        self.sct = mss()

    def areTextTransfer(self, targetArea: dict, config: str):
        screen = np.array(self.sct.grab(targetArea))

        gray_image = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

        # enhanced = cv2.convertScaleAbs(gray_image, alpha=3.0)

        threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        cv2.namedWindow("Hello", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Hello", threshold_image)
        cv2.waitKey(0)
        # end1=time.time()

        # print(pytesseract.get_languages(config=''))
        text = pytesseract.image_to_string(threshold_image, config=config)
        return text


class edit_excel():
    def __init__(self) -> None:
        self.currentPath = os.getcwd()
        self.title_list = []
        self.excel_name = ""

    def edit_excel(self, page_title, list_Title, list_Data, mod=0):
        try:
            if mod == 0:
                self.create_new_folder()
                self.create_new_excel(mod)
                self.create_and_import_sheet(page_title, list_Title, list_Data)
            elif mod ==1:
                self.create_new_folder()
                self.import_member_information()

        except Exception as e:
            self.open_and_close_txt(e)

    # 打开日志并且填入错误信息
    def open_and_close_txt(self, e):
        localDate = re.sub(r"[ :]+", "-", str(time.asctime(time.localtime(time.time()))))
        f3 = open("log.txt", "a")
        f3.write(localDate + ": " + str(e) + "\n")
        f3.close()

    # 创建文件夹（数据库）
    def create_new_folder(self):
        try:
            if not os.path.isdir(self.currentPath + "\\data"):
                os.makedirs(self.currentPath + "\\data")
                self.currentPath = self.currentPath + "\\data"
            else:
                self.currentPath = self.currentPath + "\\data"
        except Exception as e:
            self.open_and_close_txt(e)
            self.currentPath = self.currentPath + "\\data"

    # name是新excel的名字，请包含完整信息，比如“xxxx.xlsx”，mod默认为0
    def create_new_excel(self, mod=0):
        try:
            if mod == 0:
                current_timestamp = time.time()
                current_time = time.localtime(current_timestamp)
                # 提取当前月份
                current_month = current_time.tm_mon
                name = str(current_month) + "月_部落战.xlsx"
                file_path = os.path.join(self.currentPath, name)
                if os.path.exists(file_path):  # 判断该excel是否存在于这个文件夹中
                    self.excel_name = name
                    print("已经存在")
                else:
                    df = pd.DataFrame()
                    df.to_excel(file_path, index=False)
                    self.excel_name = name
            elif mod == 1:  # 这是成员信息，暂时没用到

                pass
        except Exception as e:
            self.open_and_close_txt(e)

    def create_and_import_sheet(self, page_title, list_Title, list_Data):
        try:
            file_path = os.path.join(self.currentPath, self.excel_name)
            # print(self.currentPath)
            print("excel name is: " + self.excel_name)

            start_column = 0
            start_column_letter = ""
            actual_page_title_row = 1  # page 的名字的行数
            actual_list_title_row = 2  # 数据的名字的行数

            wb = openpyxl.load_workbook(file_path)
            ws = wb.active
            if page_title[0] not in self.title_list:
                self.title_list.append(page_title[0])
                page_number = self.title_list.index(page_title[0])
                start_column = 7 * page_number + 1  # 开始列名的数字
                for i in range(0, len(list_Title)):
                    ws[openpyxl.utils.get_column_letter(start_column + i) + str(actual_page_title_row)] = page_title[0]
                    ws[openpyxl.utils.get_column_letter(start_column + i) + str(actual_list_title_row)] = list_Title[i]
            else:
                page_number = self.title_list.index((page_title[0]))
                start_column = 7 * page_number

            count = 1
            #  判断一行的第一个cell是否为空，如果不是则count加一
            while ws[
                openpyxl.utils.get_column_letter(start_column) + str(actual_list_title_row + count)].value is not None:

                # print(ws[openpyxl.utils.get_column_letter(start_column) + str(actual_list_title_row + count)].value)
                if ws[openpyxl.utils.get_column_letter(start_column) + str(actual_list_title_row + count)].value == \
                        list_Data[0]:
                    # print(count)
                    ws.insert_rows(actual_list_title_row + count)

                    break
                count = count + 1

            #  从这一行的第一个数值开始填写
            for i in range(0, len(list_Data)):
                ws[openpyxl.utils.get_column_letter(start_column + i) + str(actual_list_title_row + count)] \
                    = list_Data[i]

            title_column = 0
            while ws[openpyxl.utils.get_column_letter(1 + title_column * 7) + str(1)].value is not None:
                start_row = 1
                end_row = 1
                start_column = 1
                end_column = 7 + title_column * 7
                ws.merge_cells(start_row=start_row, end_row=end_row, start_column=start_column, end_column=end_column)
                title_column += 1
            wb.save(file_path)

        except Exception as e:
            self.open_and_close_txt(e)

    def import_member_information(self, name, label, join, recently_exit, difference,authentication):
        df = pd.read_excel(self.currentPath, "人员信息统计.xlsx")
        new_row = {'昵称': name, '标签': label, '加入': join, '最近退出':recently_exit,"差值":difference,"常驻认证T/F": authentication}
        df = df.append(new_row, ignore_index=True)
        df.to_excel("人员信息统计.xlsx")
    def merge_title_cell(self, excel):  # 所有完成之后，最后一步在合并单元格
        pass

if __name__ == "__main__":
    # startEvent=eventKeyboard()
    # startEvent.StartListener()
    # # x,y=startEvent.mouseGet()
    # # while x!=0 and y!=0:
    # #     time.sleep(0.1)
    # #     x,y=startEvent.mouseGet()
    # time.sleep(9)
    # startEvent.activeFlagSet(1)
    # time.sleep(9)
    # # startEvent.activeFlagSet(1)
    # # time.sleep(15)
    # startEvent.terminate()
    # wind = windowsUI(True, 0.1, "black")
    # # time.sleep(5)

    # print("a")
    # keyTest=eventKeyboard()
    # # keyTest.shortcutFlag=True
    # keyTest.StartListener()
    # time.sleep(10)
    # print(keyTest.statusGet())
    # keyTest.terminate()
    # con=mouse_control()
    # con.move_and_press_mouse(636,21)
    # con.smooth(1913,195,500)
    ocr = OCRController()
    text = ocr.areTextTransfer({"top": 398, "left": 482, "width": 50, "height": 50}, "chi_sim+eng",
                               r'--oem 3 --psm 6 -c tessedit_char_whitelist=#♡※✰')
    print(text)
