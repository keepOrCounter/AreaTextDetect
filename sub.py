# -*- coding: utf-8 -*-
import math
import copy
import openpyxl
import pandas as pd
import pynput
import screeninfo
import time
import tkinter
from tkinter.font import Font
from mss import mss
from pynput.mouse import Controller, Button
import numpy as np
import pyautogui
import cv2
from paddleocr import PaddleOCR
import os
import re
from sklearn.cluster import KMeans
from collections.abc import Iterable
from tkinter.messagebox import *
from tkinter import ttk, RIGHT, Y, LEFT
from sklearn.metrics import pairwise_distances as cdist

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
        self.keyPressed = pynput.keyboard.Listener(on_press = self.pressed, on_release = self.released)
        self.counter = 0
        # self.shortcutThread = False
        
        self.__status = 0
        self.shortcutFlag = False
        self.recordKey = []
        self.recordedshortcut = {"Key.alt_lz": 2} # Key.alt_lz is default shortcut

        self.keyboard_key_dict = {
    "\x01" : ['ctrl','a'],
    "\x02" : ['ctrl','b'],
    "\x03" : ['ctrl','c'],
    "\x04" : ['ctrl','d'],
    "\x05" : ['ctrl','e'],
    "\x06" : ['ctrl','f'],
    "\x07" : ['ctrl','g'],
    "\x08" : ['ctrl','h'],
    "\t"   : ['ctrl','i'],
    "\n"   : ['ctrl','j'],
    "\x0b" : ['ctrl','k'],
    "\x0c" : ['ctrl','l'],
    "\r"   : ['ctrl','m'],
    "\x0e" : ['ctrl','n'],
    "\x0f" : ['ctrl','o'],
    "\x10" : ['ctrl','p'],
    "\x11" : ['ctrl','q'],
    "\x12" : ['ctrl','r'],
    "\x13" : ['ctrl','s'],
    "\x14" : ['ctrl','t'],
    "\x15" : ['ctrl','u'],
    "\x16" : ['ctrl','v'],
    "\x17" : ['ctrl','w'],
    "\x18" : ['ctrl','x'],
    "\x19" : ['ctrl','y'],
    "\x1a" : ['ctrl','z'],
    "\x1f" : ['ctrl','shift','-'],
    '<186>'  : ['ctrl',';'],
    "<187>"  : ['ctrl','='],
    "<189>"  : ['ctrl','-'],
    "<192>"  : ['ctrl','`'],
    "<222>"  : ['ctrl',r"'"],
    "<48>"   : ['ctrl','0'],
    "<49>"   : ['ctrl','1'],
    "<50>"   : ['ctrl','2'],
    "<51>"   : ['ctrl','3'],
    "<52>"   : ['ctrl','4'],
    "<53>"   : ['ctrl','5'],
    "<54>"   : ['ctrl','6'],
    "<55>"   : ['ctrl','7'],
    "<56>"   : ['ctrl','8'],
    "<57>"   : ['ctrl','9'],
    "~"    : ['shift', '`'],
    "!"    : ['shift', '1'],
    "@"    : ['shift', '2'],
    "#"    : ['shift', '3'],
    "$"    : ['shift', '4'],
    "%"    : ['shift', '5'],
    "^"    : ['shift', '6'],
    "*"    : ['shift', '7'],
    "("    : ['shift', '8'],
    ")"    : ['shift', '9'],
    "_"    : ['shift', '-'],
    "+"    : ['shift', '='],
    ":"    : ['shift', ';'],
    "\'"   : ['shift', "'"],
    "<"    : ['shift', ","],
    "{"    : ['shift', "["],
    "}"    : ['shift', "]"],
    "|"    : ['shift', "\\"],
    "?"    : ['shift', "/"],
}

    def pressed(self,key):
        self.keyPressReset = time.time()
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
                        self.__status = self.recordedshortcut[tem] # Change status if user triggered a shortcut
        
        if time.time() - self.timeIntervalStart > 10.0:
            if self.activeFlag == -1: # check if main thread is active, if not, kill sub thread
                self.__status = -1
                return False
            else:
                self.activeFlag = -1
                self.timeIntervalStart = time.time()

    def released(self,key):
        self.keyPressReset = time.time()
        try:
            tem = str(key.char)
        except:
            tem = str(key)
            
        if tem in self.keyboard_key_dict.keys():
            tem=self.keyboard_key_dict[tem][1]
            
        if self.shortcutFlag and len(self.recordKey) == 2: # record shortcut
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
            if self.activeFlag == -1: # check if main thread is active, if not, kill sub thread
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
        self.keyPressReset = time.time()

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
        if time.time() - self.keyPressReset > 1.0:
            self.__status = 1
            
            return 1
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
        self.mouseClickReset = time.time()
        
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
        self.mouseClickReset = time.time()

    def terminate(self) -> None:
        self.mouseClicked.stop()
        self.mouseMove.stop()

    def mouseGet(self, side) -> int:
        if time.time() - self.mouseClickReset > 1.0:
            self.DetectedMouseXPos = -1
            self.DetectedMouseYPos = -1

            self.DetectedRightMouseXPos = -1
            self.DetectedRightMouseYPos = -1
            
            return -1, -1
        
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
            
    def restart(self):
        self.DetectedMouseXPos = -1
        self.DetectedMouseYPos = -1

        self.DetectedRightMouseXPos = -1
        self.DetectedRightMouseYPos = -1

        self.MotionMouseXPos = -1
        self.MotionMouseYPos = -1


class windowsUI():
    """
    class parameters:
        `override`: self defined tk windows, only set true when using screenShot mode or message box mode
        `alpha`: visibility of root window
        `bgColor`: background color, only root windows
        `screenShot`: mode flag, 1 for screenShot mode, 2 for main window mode, 3 for child windows on screenShot mode
        width,height: size of root window
        positionX,positionY: x,y for top left of window
        `listener`: mouse listener

        !!! Flag summary:
        `self.statusID`:
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
            "1100": record user behaviour
            "1103": Start up screen shot
            "2000": Screen shot mode
            "1010": behaviour recording panel
            "1020": click setting panel
            "1030-1099": choose available button
            "3000": show result
            "4000": execute command
            "5000": standby config
            "6000": loop config
    """

    def __init__(self, override=False, alpha=0.8, bgColor="black", screenShot=-1, \
                 width=-1, height=-1, positionX=0, positionY=0, listener: eventMouse = None) -> None:
        # self.__timeList=[time.time(),0]
        self.test = False # enable test code
        self.testNum = 3
        
        self.listener = eventMouse()
        self.keyBoardInterrupt = eventKeyboard()
        self.screenShot = screenShot
        self.screen = screeninfo.get_monitors()[0]
        # print("22222222222222222222222333333333333333333333")
        self.mainPanelButtons = ({"Recognition Area Record": [1100], "Execute Recorded": [1101],\
            "Setting": [1102], "next page": [1103], "testRecord": [1104]},
                {"Mouse Click": [1110], "Mouse Hold": [1111], "Mouse Move": [1112], \
                    "Scorlling": [1113],"Text Recognize": [1114], "Loop": [1115], \
                        "Standby": [1116],"Save record": [1117], "Back to home page": [1118]},
                {"Back to home page": [4100]}, 
                {"record by coordinate": [1120],"click on a button": [1121],"back": [1122]}, 
                {"back": [1130]}, {"wait by time counts": [5100], "wait until specific text show up": [5101], \
                    "wait until spcific icon or button show up(recommend)": [5102], "back": [5103]}, \
                {"confirm": [5110], "Cancel": [5111]}, {"back": [5120]}, {"Cancel": [6100]}, \
                {"a Piece of text": [6110], "list of text": [6111], "Cancel": [6112]}, \
                {"Cancel": [6120], "Set up new model": [6121]}, {"Cancel": [6300], \
                    "Set up new model": [6301]}) # 11
        self.mainPanelInput = ([],[],[],[],[],[],["Hours", "Minutes", "Seconds"],[],\
            ["Loop time(-1 for infinite loop and will only stop by user interrupt)"], \
                [],[],[]) # 11
        self.mainPanelLabel = ([],[],[],[],[],[],[],[],[],[],["Please choose one of model to \
find out text boxes"],["Please choose one of model to filter out error location"]) # 11
        
        self.description = {2010:"leftClick", 1131: "clickOnButton", 5110:"timeWait", 5121: "iconDetection", \
            6101:"loopController"}
        # Store the buttons on main Panel and their status ID
        self.currentButton: list[tkinter.Button] = []
        self.currentLabel = []
        self.currentInput: list[tkinter.Entry] = []
        
        self.currentButtonSubWin: list[tkinter.Button] = []
        self.currentLabelSubWin = []
        
        self.currentOtherComponents = []
        
        self.loopCounter = ([],[],[],[]) # index of loop back to, loop time, if finished loop

        self.statusID = 1000  # globel status flag
        self.__subWindows = None  # store windows created by event function Start()
        self.messageBox = None
        self.screenShotor = None

        self.__rec = []  # store rectangle in canvas
        self.recoredArea = [] # store recorded screen shot area
        self.textBoxes = [] # store recognized text boxes
        self.textAreUpperBound = self.screen.height
        self.textAreLowerBound = 0
        
        self.sequencialCommand = []
        
        self.x = -10  # store mouse click coordinations
        self.y = -10
        
        self.dbManagement = edit_excel()
        self.ocr = OCRController(self.dbManagement.currentPath, self.dbManagement.OCRModelDataLoader())

        self.testModelID = None
        self.testScrollingArea = {"top": 0, "left": 0, "width": 0, "height": 0}
        self.xRight = -1  # store mouse move coordinations
        self.yRight = -1

        # self.__loopTime = 0  # use to count the time, 0.1s every loop
        self.__counter = 0  # status id for drawer function
        self.counter = -1
        self.__root = tkinter.Tk()

        self.windowSize = {"root": [width, height, positionX, positionY], "screenShoter": \
            [0, 0, 0, 0], "record": [0,0,0,0]}  # all type of window size

        self.width = width  # current use width and height
        self.height = height
        self.bgColor = bgColor
        self.alpha = alpha

        
        self.scroller = None
        self.mylistBox = None
        
        # testButton = tkinter.Button(self.__root, text="tester")
        # font = Font(testButton["font"])  # get font information
        # self.grid = font.metrics("linespace")  # calculate hieght and weidth by font information
        # # lineWidth = font.measure(x)
        # testButton.destroy()
        self.positionX = positionX
        self.positionY = positionY
        
        self.IOController = mouse_control()
        self.userInteraction = UserBehaviourController(self.IOController, self.listener, self.ocr,\
            self.dbManagement, self)
        
        self.recordPointer = len(self.userInteraction.recoredBehaviours)
        self.executePointer = 0

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
                
            self.windowSize["root"][0] = self.width
            self.windowSize["root"][1] = self.height
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

    def layOutController(self, mode="root", view=0, lastmode = None, windows = "root") -> None:
        if windows == "root":
            counter = 0
            buttonNum = len(self.mainPanelButtons[view].keys())
            buttonNum += len(self.mainPanelInput[view])
            buttonNum += len(self.mainPanelLabel[view])
            buttonStatus = [tkinter.NORMAL, tkinter.DISABLED]
            buttonStatusSetup = []
            if mode == "root":
                self.widgetsCleaner(self.currentButton, self.currentLabel, self.currentButtonSubWin, \
                    self.currentLabelSubWin, self.scroller, self.mylistBox, self.currentInput)
                if self.__subWindows != None:
                    self.__subWindows.destroy()
                    self.__subWindows = None
                    
                self.width, self.height, self.positionX, self.positionY = self.windowSize[mode]


                self.__root.resizable(0, 0)

            elif mode == "record":
                self.widgetsCleaner(self.currentButton, self.currentLabel, self.currentInput)
                print(self.currentButton)
                # for x in range(len(self.currentButton)):
                #     self.currentButton[x].destroy()

                self.windowSize[lastmode] = []  # back up the size of root window
                self.windowSize[lastmode].append(self.width)
                self.windowSize[lastmode].append(self.height)
                self.windowSize[lastmode].append(self.positionX)
                self.windowSize[lastmode].append(self.positionY)

                self.width = int(self.__root.winfo_screenwidth() / 5)
                self.height = int(self.width * 2 / 1)
                self.positionX = 50
                self.positionY = 50


                self.__root.resizable(0, 0)

            elif mode == "executeList":
                self.widgetsCleaner(self.currentButton, self.currentLabel, self.currentInput)

                self.windowSize[lastmode] = []  # back up the size of last window
                self.windowSize[lastmode].append(self.width)
                self.windowSize[lastmode].append(self.height)
                self.windowSize[lastmode].append(self.positionX)
                self.windowSize[lastmode].append(self.positionY)

                self.width = int(self.__root.winfo_screenwidth() / 5)
                self.height = int(self.width * 2 / 1)
                self.positionX = 50
                self.positionY = 50
                
            elif mode == "clickRecord":
                self.widgetsCleaner(self.currentButton, self.currentLabel, self.currentInput)

                self.windowSize[lastmode] = []  # back up the size of last window
                self.windowSize[lastmode].append(self.width)
                self.windowSize[lastmode].append(self.height)
                self.windowSize[lastmode].append(self.positionX)
                self.windowSize[lastmode].append(self.positionY)

                self.width = int(self.__root.winfo_screenwidth() / 5)
                self.height = int(self.width * 2 / 1)
                self.positionX = 50
                self.positionY = 50
                
            elif mode == "UIClick":
                self.widgetsCleaner(self.currentButton, self.currentLabel, self.currentInput)

                self.windowSize[lastmode] = []  # back up the size of last window
                self.windowSize[lastmode].append(self.width)
                self.windowSize[lastmode].append(self.height)
                self.windowSize[lastmode].append(self.positionX)
                self.windowSize[lastmode].append(self.positionY)

                self.width = int(self.__root.winfo_screenwidth() / 5)
                self.height = int(self.width * 2 / 1)
                self.positionX = 50
                self.positionY = 50
                
            elif mode == "standbyConfig":
                self.widgetsCleaner(self.currentButton, self.currentLabel, self.currentInput)

                self.windowSize[lastmode] = []  # back up the size of last window
                self.windowSize[lastmode].append(self.width)
                self.windowSize[lastmode].append(self.height)
                self.windowSize[lastmode].append(self.positionX)
                self.windowSize[lastmode].append(self.positionY)

                self.width = int(self.__root.winfo_screenwidth() / 5)
                self.height = int(self.width * 2 / 1)
                self.positionX = 50
                self.positionY = 50
                
            elif mode == "timeWaitConfig":
                self.widgetsCleaner(self.currentButton, self.currentLabel, self.currentInput)

                self.windowSize[lastmode] = []  # back up the size of last window
                self.windowSize[lastmode].append(self.width)
                self.windowSize[lastmode].append(self.height)
                self.windowSize[lastmode].append(self.positionX)
                self.windowSize[lastmode].append(self.positionY)

                self.width = int(self.__root.winfo_screenwidth() / 5)
                self.height = int(self.width * 13 / 10)
                self.positionX = 50
                self.positionY = 50
                
                for x in self.mainPanelInput[view]:# place input box
                    counter += 1
                    entry_var = tkinter.StringVar()
                    entry_var.set(x)
                    self.currentInput.append(tkinter.Entry(self.__root,width=int(self.width/12),\
                        textvariable=entry_var))
                    font = Font(font=self.currentInput[-1]["font"])  # get font information
                    lineHeight = font.metrics("linespace")  # calculate hieght and weidth by font information
                    lineWidth = font.measure("  "*int(self.width/12))
                    print(self.width)
                    print(lineHeight, lineWidth)
                    # print(lineHeight,lineWidth)
                    # print()
                    #
                    self.currentInput[-1].place(x=(self.width - lineWidth) / 2,
                                                 y=counter * self.height / (buttonNum + 1) - lineHeight / 2)

            elif mode == "loopConfig":
                self.widgetsCleaner(self.currentButton, self.currentLabel, self.currentInput)

                self.windowSize[lastmode] = []  # back up the size of last window
                self.windowSize[lastmode].append(self.width)
                self.windowSize[lastmode].append(self.height)
                self.windowSize[lastmode].append(self.positionX)
                self.windowSize[lastmode].append(self.positionY)

                self.width = int(self.__root.winfo_screenwidth() / 5)
                self.height = int(self.width * 2 / 1)
                self.positionX = 50
                self.positionY = 50
                
                self.mainPanelButtons[view].clear()
                self.mainPanelButtons[view]["Cancel"] = [6100]
                
                buttonStatusSetup.append(0)
                for x in range(len(self.loopCounter)):
                    if len(self.loopCounter[x]) == 0:
                        self.mainPanelButtons[view]["Start Loop " + chr(65 + x)] = [6100 + x + 1]
                        buttonStatusSetup.append(0)
                    else:
                        if self.loopCounter[x][2]:
                            buttonStatusSetup.append(1)
                        else:
                            buttonStatusSetup.append(0)
                        self.mainPanelButtons[view]["Stop Loop " + chr(65 + x)] = [6100 + x + 1]
                buttonNum = len(self.mainPanelButtons[view].keys()) + len(self.mainPanelInput[view]) \
                    + len(self.mainPanelLabel[view])
                
                for x in self.mainPanelInput[view]:# place input box
                    counter += 1
                    entry_var = tkinter.StringVar()
                    entry_var.set(x)
                    self.currentInput.append(tkinter.Entry(self.__root,width=int(self.width/12),\
                        textvariable=entry_var))
                    font = Font(font=self.currentInput[-1]["font"])  # get font information
                    lineHeight = font.metrics("linespace")  # calculate hieght and weidth by font information
                    lineWidth = font.measure("  "*int(self.width/12))
                    print(self.width)
                    print(lineHeight, lineWidth)
                    # print(lineHeight,lineWidth)
                    # print()
                    #
                    self.currentInput[-1].place(x=(self.width - lineWidth) / 2,
                                                 y=counter * self.height / (buttonNum + 1) - lineHeight / 2)

            elif mode == "textRecognizeConfig":
                self.widgetsCleaner(self.currentButton, self.currentLabel, self.currentInput)

                self.windowSize[lastmode] = []  # back up the size of last window
                self.windowSize[lastmode].append(self.width)
                self.windowSize[lastmode].append(self.height)
                self.windowSize[lastmode].append(self.positionX)
                self.windowSize[lastmode].append(self.positionY)

                self.width = int(self.__root.winfo_screenwidth() / 5)
                self.height = int(self.width * 2 / 1)
                self.positionX = 50
                self.positionY = 50
                
            elif mode == "textBoxesModelling":
                self.widgetsCleaner(self.currentButton, self.currentLabel, self.currentInput)

                self.windowSize[lastmode] = []  # back up the size of last window
                self.windowSize[lastmode].append(self.width)
                self.windowSize[lastmode].append(self.height)
                self.windowSize[lastmode].append(self.positionX)
                self.windowSize[lastmode].append(self.positionY)

                self.width = int(self.__root.winfo_screenwidth() / 5)
                self.height = int(self.width * 2 / 1)
                self.positionX = 50
                self.positionY = 50
                
                for x in self.mainPanelLabel[view]:# place buttons
                    counter += 1
                    self.currentLabel.append(tkinter.Label(self.__root, text=x, fg="white", bg="black"))

                    font = Font(font=self.currentLabel[-1]["font"])  # get font information
                    lineHeight = font.metrics("linespace")  # calculate hieght and weidth by font information
                    lineWidth = font.measure(x)
                    # print(lineHeight,lineWidth)
                    # print()
#       
                    self.currentLabel[-1].place(x=(self.width - lineWidth) / 2,
                                                 y=counter * self.height / (buttonNum + 1) - lineHeight / 2)

            elif mode == "textSeeker":
                self.widgetsCleaner(self.currentButton, self.currentLabel, self.currentInput)

                self.windowSize[lastmode] = []  # back up the size of last window
                self.windowSize[lastmode].append(self.width)
                self.windowSize[lastmode].append(self.height)
                self.windowSize[lastmode].append(self.positionX)
                self.windowSize[lastmode].append(self.positionY)

                self.width = int(self.__root.winfo_screenwidth() / 5)
                self.height = int(self.width * 2 / 1)
                self.positionX = 50
                self.positionY = 50
                
                for x in self.mainPanelLabel[view]:# place buttons
                    counter += 1
                    self.currentLabel.append(tkinter.Label(self.__root, text=x, fg="white", bg="black"))

                    font = Font(font=self.currentLabel[-1]["font"])  # get font information
                    lineHeight = font.metrics("linespace")  # calculate hieght and weidth by font information
                    lineWidth = font.measure(x)
                    # print(lineHeight,lineWidth)
                    # print()
#       
                    self.currentLabel[-1].place(x=(self.width - lineWidth) / 2,
                                                 y=counter * self.height / (buttonNum + 1) - lineHeight / 2)


            self.__root.geometry("{0}x{1}+{2}+{3}" \
                .format(self.width, self.height, self.positionX, self.positionY))

            for x in self.mainPanelButtons[view].keys():# place buttons
                counter += 1
                tem = self.__lambdaCreater(self.mainPanelButtons[view][x][0])
                # print(self.mainPanelButtons[view][x][0])
                self.currentButton.append(tkinter.Button(self.__root, text=x, command=tem))
                if len(buttonStatusSetup) > 0:
                    # print(counter)
                    # print(buttonStatusSetup)
                    # print(len(self.mainPanelInput[view]))
                    # print(buttonStatusSetup[counter - len(self.mainPanelInput[view]) - 1])
                    self.currentButton[-1].config(state=buttonStatus[buttonStatusSetup[counter - len(self.mainPanelInput[view]) - 1]])
                    
                font = Font(font=self.currentButton[-1]["font"])  # get font information
                lineHeight = font.metrics("linespace")  # calculate hieght and weidth by font information
                lineWidth = font.measure(x)
                # print(lineHeight,lineWidth)
                # print()
#   
                self.currentButton[-1].place(x=(self.width - lineWidth) / 2,
                                             y=counter * self.height / (buttonNum + 1) - lineHeight / 2)


    def __lambdaCreater(self, x):  # create lambda function for button, prevent shollow copy
        return lambda: self.Start(x)

    def subWindowCreater(self, width, height, lastMode = "root", x = 100, y = 100, \
        listener = "None", alphaValue = 0.8, bgColor = "black", scrollBar = False, backup = True):
        
        self.__subWindows = tkinter.Toplevel()  # set up sub window
        self.__subWindows.title("recorded operations")
        if backup:
            self.windowSize[lastMode] = []  # back up the size of last window
            self.windowSize[lastMode].append(self.width)
            self.windowSize[lastMode].append(self.height)
            self.windowSize[lastMode].append(self.positionX)
            self.windowSize[lastMode].append(self.positionY)
        
        self.width = width
        self.height = height
        self.positionX = x
        self.positionY = y

        self.__subWindows.attributes("-alpha", alphaValue)

        self.__subWindows.geometry("{0}x{1}+{2}+{3}" \
                                   .format(self.width, self.height, x, y))
        self.__subWindows.configure(bg=bgColor)

        if scrollBar:
            self.scroller = ttk.Scrollbar(self.__subWindows)  #设置窗口滚动条
            self.scroller.pack(side = RIGHT, fill = Y)  #设置窗口滚动条位置
            
            self.mylistBox = tkinter.Listbox(self.__subWindows, yscrollcommand = self.scroller.set, \
                width=self.width, bg = bgColor, fg = "white")  #创建列表框

            
            self.mylistBox.pack( side = LEFT , fill="both")  
            self.scroller.config( command = self.mylistBox.yview )  
        
        if listener == "mouse" and self.listener != None:
            self.listener = eventMouse()
            self.listener.StartListener()

        self.__subWindows.resizable(0, 0)

    def screenShotCreation(self, alphaValue=0.5, bgColor="black") -> None:
        """_summary_

        Args:
            alphaValue (int): the visibility of the screen shot window
            bgColor (str): allow for user to custom the back ground color
        """
        self.screenShotor = tkinter.Toplevel()  # set up sub window
        self.windowSize["root"] = []  # back up the size of root window
        self.windowSize["root"].append(self.width)
        self.windowSize["root"].append(self.height)
        self.windowSize["root"].append(self.positionX)
        self.windowSize["root"].append(self.positionY)
        
        self.width = self.screenShotor.winfo_screenwidth()  # make it large as the screen
        self.height = self.screenShotor.winfo_screenheight()

        self.screenShotor.overrideredirect(True)  # remove tk default component(e.g. window close button)
        self.screenShotor.attributes("-alpha", alphaValue)

        self.screenShotor.geometry("{0}x{1}+{2}+{3}" \
                                   .format(self.width, self.height, 0, 0))
        self.screenShotor.configure(bg=bgColor)
        self.__num = 6
        self.canvasPlace(target="sub")

        self.listener.restart()
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
            self.loopCounter = ([],[],[],[])
            self.recordPointer = len(self.userInteraction.recoredBehaviours)
            print(self.recordPointer)
            print(self.userInteraction.recoredBehaviours)
            self.layOutController("record", 1, "root")
            if self.__subWindows == None:
                self.subWindowCreater(int(self.__root.winfo_screenwidth() / 6), int(self.width * 2 / 1),\
                    x = int(self.__root.winfo_screenwidth() - self.__root.winfo_screenwidth() / 5), \
                        y = 50, scrollBar = True, backup = False)
            self.statusID = 1010
            
        elif status == 1101:
            # print(self.mainPanelButtons)
            self.layOutController("executeList", 2, "root")
            self.statusID = 4000
            
        elif status == 1104:
            self.screenShotCreation()
            # self.subWindows.append(windowsUI(True,0.5,"black",listener=mouseL,screenShot=3))
            # print("!!!!!!!!!!!!!!!!!!")
            self.__root.attributes("-alpha", 0)
            if self.__subWindows != None:
                self.__subWindows.attributes("-alpha", 0)
            self.statusID = -1000
            # print("Start:",self.statusID)
            
        elif status == 1110:
            self.layOutController("clickRecord", 3, "record")
            self.statusID = 1020
            
        elif status == 1114:
            self.layOutController("textRecognizeConfig", 9, "record")
            self.statusID = 6010
            
        elif status == 1115:
            self.layOutController("loopConfig", 8, "record")
            self.statusID = 6000
            
        elif status == 1116:
            self.layOutController("standbyConfig", 5, "record")
            self.statusID = 5000
            
        elif status == 1117:
            self.recordPointer = len(self.userInteraction.recoredBehaviours)
            self.userInteraction.oldPointer = len(self.userInteraction.recoredBehaviours)
            if len(self.mainPanelButtons[2].keys()) == 1: # add button to execute panel
                self.mainPanelButtons[2]["1"] = [4101]
            else:
                self.mainPanelButtons[2][str(int(list(self.mainPanelButtons[2].keys())[-1]) + 1)] = \
                    [self.mainPanelButtons[2][list(self.mainPanelButtons[2].keys())[-1]][0] + 1]
            print(self.mainPanelButtons)
                
            self.layOutController(lastmode = "record")
            self.messageBox = showinfo("RseMessager", "operation recorded!")
            self.statusID = 1000
            
        elif status == 1118:
            self.userInteraction.delRecord()
            self.recordPointer = len(self.userInteraction.recoredBehaviours)
            
            self.layOutController(lastmode = "record")
            self.statusID = 1000
            
        elif status == 1120:
            self.messageBox = showinfo("RseMessager", "Please click what you would like us to\
click after pressing 'ok'. This message could be close in setting panel.")
            self.__root.attributes("-alpha", 0)
            if self.__subWindows != None:
                self.__subWindows.attributes("-alpha", 0)
            self.listener.restart()
            self.statusID = 2010
            
        elif status == 1121:
            fileList = self.dbManagement.UIImageList()
            # print(fileList)
            self.mainPanelButtons[4].clear()
            self.mainPanelButtons[4]["back"] = [1130]
            for x in range(len(fileList)):
                self.mainPanelButtons[4]["button. "+fileList[x]] = [1130 + x +1]
            self.layOutController("UIClick", 4, "clickRecord")
            self.statusID = 1030
            
        elif status == 1122:
            self.layOutController("record", 1, "clickRecord")
            self.statusID = 1010
            
        elif status == 1130:
            self.layOutController("clickRecord", 3, "UIClick")
            self.statusID = 1020
            
        elif 2000>status >= 1131:
            fileName = list(self.mainPanelButtons[4].keys())[status % 1130][8:]
            image = cv2.imread(self.dbManagement.currentPath + "\\UI\\" + fileName, flags=1)
            print(self.dbManagement.currentPath + "\\UI\\" + fileName)
            self.userInteraction.actionRecord(self.description[1131],\
                (image, (0,0,self.screen.width, self.screen.height)), self.recordPointer)
            self.shownListManagement("add", self.description[1131]+": " + fileName)
            
        elif status == 4100:
            self.layOutController(lastmode = "record")
            self.statusID = 1000
            
        elif 4200> status >= 4101:
            self.counter = -1
            self.executePointer = 0
            self.loopCounter = ([],[],[],[])
            self.statusID = 4200 + (status % 4100)
            
        elif status == 5100:
            self.layOutController("timeWaitConfig", 6, "standbyConfig")
            self.statusID = 5010
            
        elif status == 5102:
            fileList = self.dbManagement.UIImageList()
            # print(fileList)
            self.mainPanelButtons[7].clear()
            self.mainPanelButtons[7]["back"] = [5120]
            for x in range(len(fileList)):
                self.mainPanelButtons[7]["button. "+fileList[x]] = [5120 + x +1]
            self.layOutController("UIClick", 7, "standbyConfig")
            self.statusID = 5020
            
        elif status == 5103:
            self.layOutController("record", 1, "standbyConfig")
            self.statusID = 1010
            
        elif status == 5110:
            counter = 0
            for x in range(len(self.currentInput)):
                tem = self.currentInput[x].get()
                if tem.isdigit():
                    counter += int(tem)*60**(2-x)
            self.userInteraction.actionRecord(self.description[status],\
                (counter,), self.recordPointer)
            self.shownListManagement("add", self.description[status]+": " + str(counter) + "s")
            self.layOutController("standbyConfig", 5, "timeWaitConfig")
            self.statusID = 5000
            
        elif status == 5111:
            self.layOutController("standbyConfig", 5, "timeWaitConfig")
            self.statusID = 5000
            
        elif status == 5120:
            self.layOutController("standbyConfig", 5, "UIClick")
            self.statusID = 5000
            
        elif 6000 > status >=5121:
            fileName = list(self.mainPanelButtons[7].keys())[status % 5120][8:]
            image = cv2.imread(self.dbManagement.currentPath + "\\UI\\" + fileName, flags=1)
            self.userInteraction.actionRecord(self.description[5121],\
                (image, (0,0,self.screen.width, self.screen.height)), self.recordPointer)
            self.shownListManagement("add", self.description[5121]+": " + fileName)
        
        elif status == 6100:
            self.layOutController("record", 1, "loopConfig")
            self.statusID = 1010
        
        elif 6104 >= status >=6101:
            if len(self.loopCounter[status % 6101]) < 3:
                tem = self.currentInput[0].get()
                if tem.isdigit():
                    counter = int(tem)

                    self.loopCounter[status % 6101].clear()
                    if self.recordPointer >= len(self.userInteraction.recoredBehaviours):
                        self.loopCounter[status % 6101].append(0)
                    else:
                        self.loopCounter[status % 6101].append(len(self.userInteraction.recoredBehaviours\
                            [self.recordPointer]))
                        
                    self.loopCounter[status % 6101].append(counter)
                    self.loopCounter[status % 6101].append(False)

                    self.shownListManagement("add", "Loop " + chr(65 + status % 6101)+ " Start")
                    self.layOutController("record", 1, "loopConfig")
                    self.statusID = 1010
                else:
                    self.messageBox = showinfo("RseMessager", "Please provide an integer")
            else:
                self.loopCounter[status % 6101][2] = True
                
                self.userInteraction.actionRecord(self.description[6101],\
                    (self.loopCounter[status % 6101][0], self.loopCounter[status % 6101][1], \
                        status % 6101), self.recordPointer)
                self.shownListManagement("add", "Loop " + chr(65 + status % 6101)+ " Stop at "\
                    + str(self.loopCounter[status % 6101][1]) + " times")
                self.layOutController("record", 1, "loopConfig")
                self.statusID = 1010
        
        elif status == 6111:
            self.messageBox = askquestion("RseMessager", "We need to set this up by following 3 steps:\n\
1. choose or build up a model to find text boxes.\n2. choose or build up a model to make sure target\
text are included by recognization area.\n3. test the result.\n Would you like to continue?")
            print(self.messageBox)
            if self.messageBox == "yes":
                for x in range(len(list(self.ocr.modelID))):
                    self.mainPanelButtons[10][str(self.ocr.modelID[x])] = [self.mainPanelButtons[10]\
                        [list(self.mainPanelButtons[10].keys())[-1]][0] + 1]

                self.layOutController("textBoxesModelling", 10, "record")
                self.statusID = 6020
                
        elif 6200 > status >=6122:
            self.testModelID = status % 6122
            self.messageBox = showinfo("RseMessager", "Text boxes recognize model has been ready,\
we would need to test this model worked with your circumstance. Please tell us \
to area of the list after pressing 'ok'.(Press key 'alt+z' finish the step)")
            self.screenShotCreation()
            # self.subWindows.append(windowsUI(True,0.5,"black",listener=mouseL,screenShot=3))
            # print("!!!!!!!!!!!!!!!!!!")
            self.__root.attributes("-alpha", 0)
            if self.__subWindows != None:
                self.__subWindows.attributes("-alpha", 0)
            self.statusID = 2000
        
        elif status == 6200:
            for x in range(len(list(self.ocr.modelID))):
                self.mainPanelButtons[11][str(self.ocr.modelID[x])] = [self.mainPanelButtons[11]\
                    [list(self.mainPanelButtons[11].keys())[-1]][0] + 1]
            self.layOutController("textSeeker", 11, "textBoxesModelling")
            self.statusID = 6201
            
        elif status == 6202:
            pass
            
        elif 6400 > status >= 6302:
            self.testModelID = status % 6302
            self.messageBox = showinfo("RseMessager", "Error location filtering model has been ready,\
we would need to test this model worked with your circumstance. Please tell us arbitrary area \
the model would determine if this cut any text(you could test multiple area at the same time). \
(Press key 'alt+z' finish the step)")
            self.screenShotCreation()
            # self.subWindows.append(windowsUI(True,0.5,"black",listener=mouseL,screenShot=3))
            # print("!!!!!!!!!!!!!!!!!!")
            self.__root.attributes("-alpha", 0)
            if self.__subWindows != None:
                self.__subWindows.attributes("-alpha", 0)
            self.statusID = 2001
            
        elif status == 6400:
            pass

    def keeper(self) -> None:
        # print("ID:",self.screenShot)
        print("Status:", self.statusID)
        self.keyBoardInterrupt.activeFlagSet(1)
        self.listener.activeFlagSet(1)
        self.eventAction() # check any action need to take
        
        if self.screenShot == 1:
            if self.drawer() == 1:
                self.__root.after(100, self.keeper)

        else:  # mian panel mode
            self.__root.after(100, self.keeper)

        self.tester()

            
    def tester(self):
        if self.statusID == -1000:
            if self.keyBoardInterrupt.statusGet() == 2:
                # print("ssssssssssssssss",self.statusID)
                self.x = -10
                self.y = -10
                self.screenShot = 2

                for x in self.__rec:
                    transformed = self.transform(x)
                    # if self.counter == 0:
                    #     self.textAreUpperBound = min(transformed["top"] , self.textAreUpperBound)
                    #     self.textAreLowerBound = max(transformed["top"] + transformed["height"],\
                    #         self.textAreLowerBound)
                    # print(self.textAreUpperBound, self.textAreLowerBound)
                    
                    self.recoredArea.append(transformed)
                    print(transformed)
                self.widgetsCleaner(self.__canvas, self.screenShotor)
                self.__rec.clear()
                self.width, self.height, self.positionX, self.positionY = self.windowSize["root"]
                
                self.statusID = -1
            
        if len(self.recoredArea) > 0 and self.testNum == 0 and self.test: # test
            tem = self.recoredArea.pop()
            # text=self.ocr.areTextTransfer(tem)
            # textBoxes = self.ocr.textboxSeekerTrainer(tem, 50)
            self.textBoxes = self.ocr.textboxSeekerPredictor(tem, 3, 0)
            self.statusID = 3000
            self.screenShotCreation()
            counter = 0
            self.testNum = 2
            for x in self.textBoxes:
                leftX = (x["left"] * self.width) / self.screen.width  # 转换相对坐标。
                leftY = (x["top"] * self.height) / self.screen.height
                
                rightX = ((x["left"] + x["width"]) * self.width) / self.screen.width  # 转换相对坐标。
                rightY = ((x["top"] + x["height"]) * self.height) / self.screen.height
                if counter == 0:
                    self.rectangleCreation(leftX, leftY, rightX, rightY, "crimson")
                elif counter == 1:
                    self.rectangleCreation(leftX, leftY, rightX, rightY, "blue")
                else:
                    self.rectangleCreation(leftX, leftY, rightX, rightY, "green")
                counter += 1
                if counter % 3 == 0:
                    counter = 0
            print(self.recoredArea)
            # self.dbManagement.OCRModelDataSaver(self.ocr.centroids,\
            #     self.ocr.data, self.ocr.modelID, self.ocr.relativeDistance)
            
        elif len(self.recoredArea) > 0 and self.testNum == 1 and self.test: # test
            
            tem = copy.deepcopy(self.recoredArea)
            # text=self.ocr.areTextTransfer(tem)
            # textBoxes = self.ocr.textboxSeekerTrainer(tem, 50)
            # textBoxes = self.ocr.textboxSeekerPredictor(tem, 50, 0)
            self.ocr.textLocationTrainer(tem, {"top": 0, "left": 0, "width": \
                self.screen.width, "height": self.screen.height})
            
            # self.ocr.textLocationPredictor(tem, {"top": 0, "left": 0, "width": \
            #     self.screen.width, "height": self.screen.height}, 1)
            
            self.testNum = 100
            self.recoredArea.clear()
            # self.statusID = 3000
            # self.screenShotCreation()
            # counter = 0
            # for x in textBoxes:
            #     leftX = (x["left"] * self.width) / self.screen.width  # 转换相对坐标。
            #     leftY = (x["top"] * self.height) / self.screen.height
                
            #     rightX = ((x["left"] + x["width"]) * self.width) / self.screen.width  # 转换相对坐标。
            #     rightY = ((x["top"] + x["height"]) * self.height) / self.screen.height
            #     if counter == 0:
            #         self.rectangleCreation(leftX, leftY, rightX, rightY, "crimson")
            #     elif counter == 1:
            #         self.rectangleCreation(leftX, leftY, rightX, rightY, "blue")
            #     else:
            #         self.rectangleCreation(leftX, leftY, rightX, rightY, "green")
            #     counter += 1
            #     if counter % 3 == 0:
            #         counter = 0
            # print(self.recoredArea)
            # self.dbManagement.OCRModelDataSaver(self.ocr.centroids,\
            #     self.ocr.data, self.ocr.modelID, self.ocr.relativeDistance)
            
        elif len(self.recoredArea) > 0 and self.testNum == 100 and self.test:
            
            tem = copy.deepcopy(self.recoredArea)
            # text=self.ocr.areTextTransfer(tem)
            # textBoxes = self.ocr.textboxSeekerTrainer(tem, 50)
            # textBoxes = self.ocr.textboxSeekerPredictor(tem, 50, 0)
            # self.ocr.textLocationTrainer(tem, {"top": 0, "left": 0, "width": \
            #     self.screen.width, "height": self.screen.height})
            
            self.ocr.textLocationPredictor(tem, {"top": 0, "left": 0, "width": \
                self.screen.width, "height": self.screen.height}, 1)
            
            self.testNum = 100
            self.recoredArea.clear()
            
        elif len(self.recoredArea) > 0 and self.testNum == 2 and self.test:
            result = []
            for x in self.textBoxes:
                tem = copy.deepcopy(self.recoredArea)
                if len(self.ocr.relativeDistance[1]) == 0:
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    result += self.ocr.textSeeker(tem, copy.deepcopy(x), {"top": 0, "left": 0, "width": \
                        self.screen.width, "height": self.screen.height}, 1, "train", \
                            self.textAreLowerBound - self.textAreUpperBound, self.textAreUpperBound, \
                                self.textAreLowerBound)
                else:
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    result += self.ocr.textSeeker(tem, copy.deepcopy(x), {"top": 0, "left": 0, "width": \
                        self.screen.width, "height": self.screen.height}, 1, "predict")
            # text=self.ocr.areTextTransfer(tem)
            # textBoxes = self.ocr.textboxSeekerTrainer(tem, 50)
            # textBoxes = self.ocr.textboxSeekerPredictor(tem, 50, 0)
            # self.ocr.textLocationTrainer(tem, {"top": 0, "left": 0, "width": \
            #     self.screen.width, "height": self.screen.height})
            self.statusID = 3000
            self.screenShotCreation()
            counter = 0
            print(result)
            for x in result:
                leftX = (x["left"] * self.width) / self.screen.width  # 转换相对坐标。
                leftY = (x["top"] * self.height) / self.screen.height
                
                rightX = ((x["left"] + x["width"]) * self.width) / self.screen.width  # 转换相对坐标。
                rightY = ((x["top"] + x["height"]) * self.height) / self.screen.height
                if counter == 0:
                    self.rectangleCreation(leftX, leftY, rightX, rightY, "crimson")
                elif counter == 1:
                    self.rectangleCreation(leftX, leftY, rightX, rightY, "blue")
                else:
                    self.rectangleCreation(leftX, leftY, rightX, rightY, "green")
                counter += 1
                if counter % 3 == 0:
                    counter = 0
            self.ocr.textLocationPredictor(tem, {"top": 0, "left": 0, "width": \
                self.screen.width, "height": self.screen.height}, 1)
            
            # self.testNum = 100
            self.recoredArea.clear()
            
        elif len(self.recoredArea) > 0 and self.testNum == 3 and self.test: # test
            print("----------------------")
            tem = self.recoredArea.pop()
            text = self.ocr.areTextTransfer(tem, textPosition= [{"top": 1058, "left": 1771, \
                "width": 78, "height": 20}], match = True)
            # textBoxes = self.ocr.textboxSeekerTrainer(tem, 50)

            # print(text)
            
    def eventAction(self) -> None:

        if self.statusID == 2000:
            if self.keyBoardInterrupt.statusGet() == 2:
                # print("ssssssssssssssss",self.statusID)
                self.x = -10
                self.y = -10
                self.screenShot = 2

                for x in self.__rec:
                    transformed = self.transform(x)
                    # if self.counter == 0:
                    #     self.textAreUpperBound = min(transformed["top"] , self.textAreUpperBound)
                    #     self.textAreLowerBound = max(transformed["top"] + transformed["height"],\
                    #         self.textAreLowerBound)
                    # print(self.textAreUpperBound, self.textAreLowerBound)
                    
                    self.recoredArea.append(transformed)
                    print(transformed)
                self.widgetsCleaner(self.__canvas, self.screenShotor)
                self.__rec.clear()
                self.width, self.height, self.positionX, self.positionY = self.windowSize["root"]
                # self.__root.attributes("-alpha", self.alpha)
                # if self.__subWindows != None:
                #     self.__subWindows.attributes("-alpha", self.alpha)
                # self.counter += 1
                
                self.statusID = -1
                self.messageBox = showinfo("RseMessager", "Please check if the result looks \
correct, please also clear the target area to ensure model could catch the right area.(Press key 'alt+z' finish the step)")
                tem = self.recoredArea.pop() # Show result
                # text=self.ocr.areTextTransfer(tem)
                # textBoxes = self.ocr.textboxSeekerTrainer(tem, 50)
                textBoxesParam = (tem, 3, self.testModelID, True)
                self.sequencialCommand.append(copy.deepcopy(textBoxesParam))
                
                self.testScrollingArea = copy.deepcopy(tem)
                self.textBoxes = self.ocr.textboxSeekerPredictor(tem, 3, self.testModelID, True)
                self.screenShotCreation()
                counter = 0
                for x in self.textBoxes:
                    leftX = (x["left"] * self.width) / self.screen.width  # 转换相对坐标。
                    leftY = (x["top"] * self.height) / self.screen.height

                    rightX = ((x["left"] + x["width"]) * self.width) / self.screen.width  # 转换相对坐标。
                    rightY = ((x["top"] + x["height"]) * self.height) / self.screen.height
                    if counter == 0:
                        self.rectangleCreation(leftX, leftY, rightX, rightY, "crimson")
                    elif counter == 1:
                        self.rectangleCreation(leftX, leftY, rightX, rightY, "blue")
                    else:
                        self.rectangleCreation(leftX, leftY, rightX, rightY, "green")
                    counter += 1
                    if counter % 3 == 0:
                        counter = 0
                self.statusID = 3000
                
        elif self.statusID == 2001:
            if self.keyBoardInterrupt.statusGet() == 2:
                # print("ssssssssssssssss",self.statusID)
                self.x = -10
                self.y = -10
                self.screenShot = 2

                for x in self.__rec:
                    transformed = self.transform(x)
                    # if self.counter == 0:
                    #     self.textAreUpperBound = min(transformed["top"] , self.textAreUpperBound)
                    #     self.textAreLowerBound = max(transformed["top"] + transformed["height"],\
                    #         self.textAreLowerBound)
                    # print(self.textAreUpperBound, self.textAreLowerBound)
                    
                    self.recoredArea.append(transformed)
                    print(transformed)
                self.widgetsCleaner(self.__canvas, self.screenShotor)
                self.__rec.clear()
                self.width, self.height, self.positionX, self.positionY = self.windowSize["root"]
                
                self.statusID = -1
                tem = copy.deepcopy(self.recoredArea)
                
                textBoxesParam = (tem, {"top": 0, "left": 0, "width": \
                self.screen.width, "height": self.screen.height}, self.testModelID)
                
                self.sequencialCommand.append(copy.deepcopy(textBoxesParam))
                
                testResult = self.ocr.textLocationPredictor(tem, {"top": 0, "left": 0, "width": \
                self.screen.width, "height": self.screen.height}, self.testModelID)
                
                if testResult:
                    self.messageBox = askquestion("RseMessager", "Model determine the edges of target \
area do not cut any text, it is a safe target area. Is it correct?")
                else:
                    self.messageBox = askquestion("RseMessager", "Model determine the edges of target \
area cut some text. Is it correct?")
                
                if self.messageBox == "yes":
                    pass
                
                self.recoredArea.clear()
                
                self.messageBox = showinfo("RseMessager", "Almost done! The model would try to \
find out all target text, please tell us the target text of the first line.(Press key 'alt+z' finish the step)")
                
                self.screenShotCreation()
                self.counter = 0
                self.statusID = 2002
                
        elif self.statusID == 2002: # find out text
            if self.keyBoardInterrupt.statusGet() == 2:
                # print("ssssssssssssssss",self.statusID)
                self.x = -10
                self.y = -10
                self.screenShot = 2
                for x in self.__rec:
                    transformed = self.transform(x)
                    if self.counter == 0:
                        self.textAreUpperBound = min(transformed["top"] , self.textAreUpperBound)
                        self.textAreLowerBound = max(transformed["top"] + transformed["height"],\
                            self.textAreLowerBound)
                    print(self.textAreUpperBound, self.textAreLowerBound)
                    
                    self.recoredArea.append(transformed)
                
                self.widgetsCleaner(self.__canvas, self.screenShotor)
                self.__rec.clear()
                self.width, self.height, self.positionX, self.positionY = self.windowSize["root"]
                
                self.statusID = -1
                result = []
                textBoxesParam = (self.recoredArea, self.textBoxes, {"top": 0, "left": 0, "width": \
                    self.screen.width, "height": self.screen.height}, self.testModelID, "predict")
                
                self.sequencialCommand.append(copy.deepcopy(textBoxesParam))
                
                for x in self.textBoxes:
                    tem = copy.deepcopy(self.recoredArea)
                    if len(self.ocr.relativeDistance[self.testModelID]) == 0:
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                        result += self.ocr.textSeeker(tem, copy.deepcopy(x), {"top": 0, "left": 0, "width": \
                            self.screen.width, "height": self.screen.height}, self.testModelID, "train", \
                                self.textAreLowerBound - self.textAreUpperBound, self.textAreUpperBound, \
                                    self.textAreLowerBound)
                    else:
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                        result += self.ocr.textSeeker(tem, copy.deepcopy(x), {"top": 0, "left": 0, "width": \
                            self.screen.width, "height": self.screen.height}, self.testModelID, "predict")
                
                self.screenShotCreation()
                counter = 0
                for x in result:
                    leftX = (x["left"] * self.width) / self.screen.width  # 转换相对坐标。
                    leftY = (x["top"] * self.height) / self.screen.height

                    rightX = ((x["left"] + x["width"]) * self.width) / self.screen.width  # 转换相对坐标。
                    rightY = ((x["top"] + x["height"]) * self.height) / self.screen.height
                    if counter == 0:
                        self.rectangleCreation(leftX, leftY, rightX, rightY, "crimson")
                    elif counter == 1:
                        self.rectangleCreation(leftX, leftY, rightX, rightY, "blue")
                    else:
                        self.rectangleCreation(leftX, leftY, rightX, rightY, "green")
                    counter += 1
                    if counter % 3 == 0:
                        counter = 0
                        
                textMatched = self.ocr.areTextTransfer(self.testScrollingArea, result, True)
                print(textMatched)
                self.statusID = 3001
        elif self.statusID == 2010: # record click
            # print(self.userInteraction.recoredBehaviours)
            clickedX, clickedY = self.listener.mouseGet("left")
            if clickedX != -1 and clickedY != -1:
                print(clickedX, clickedY)
                self.userInteraction.actionRecord(self.description[self.statusID],\
                    (clickedX, clickedY), self.recordPointer)
                self.shownListManagement("add", self.description[self.statusID]+": "+\
                        str(clickedX)+","+str(clickedY))
                
                print(self.userInteraction.recoredBehaviours)
                self.__root.attributes("-alpha", self.alpha)
                if self.__subWindows != None:
                    self.__subWindows.attributes("-alpha", self.alpha)
                self.statusID = 1020
                
        elif self.statusID == 3000: # stop showing result
            if self.keyBoardInterrupt.statusGet() == 2:
                # print("ssssssssssssssss",self.statusID)
                self.x = -10
                self.y = -10
                self.screenShot = 2

                self.widgetsCleaner(self.__canvas, self.screenShotor)
                self.__rec.clear()
                self.recoredArea.clear()
                self.__root.attributes("-alpha", self.alpha)
                if self.__subWindows != None:
                    self.__subWindows.attributes("-alpha", self.alpha)
                
                self.statusID = 6200
                self.Start(6200)
                
        elif self.statusID == 3001: # stop showing result
            if self.keyBoardInterrupt.statusGet() == 2:
                # print("ssssssssssssssss",self.statusID)
                self.x = -10
                self.y = -10
                self.screenShot = 2

                self.widgetsCleaner(self.__canvas, self.screenShotor)
                self.__rec.clear()
                self.recoredArea.clear()
                self.__root.attributes("-alpha", self.alpha)
                if self.__subWindows != None:
                    self.__subWindows.attributes("-alpha", self.alpha)
                
                self.messageBox = askquestion("RseMessager", "Are the results correct?")
                
                if self.messageBox == "yes":
                    self.dbManagement.OCRModelDataSaver(self.ocr.centroids,\
                        self.ocr.data, self.ocr.modelID, self.ocr.relativeDistance)
                
                self.statusID = 6202
                self.Start(6202)
                
        elif 5000 > self.statusID >= 4201: # execute recorded command
            self.__root.attributes("-alpha", 0)
            if self.__subWindows != None:
                self.__subWindows.attributes("-alpha", 0)
                
            print(self.userInteraction.recoredBehaviours)
            print(len(self.userInteraction.recoredBehaviours[self.statusID % 4201]))
            print(self.executePointer)
            
            if len(self.userInteraction.recoredBehaviours) == 0 or self.executePointer >= \
                len(self.userInteraction.recoredBehaviours[self.statusID % 4201]):
                    
                self.__root.attributes("-alpha", self.alpha)
                if self.__subWindows != None:
                    self.__subWindows.attributes("-alpha", self.alpha)
                self.executePointer = 0
                self.loopCounter = ([],[],[],[])
                self.statusID = 4000
            else:
                command, param = self.userInteraction.actionExcute(self.statusID % 4201, self.executePointer)
                command(*param)
                self.executePointer += 1
                
            if self.keyBoardInterrupt.statusGet() == 2:
                self.__root.attributes("-alpha", self.alpha)
                if self.__subWindows != None:
                    self.__subWindows.attributes("-alpha", self.alpha)
                self.executePointer = 0
                self.loopCounter = ([],[],[],[])
                self.statusID = 4000
        
    
    def widgetsCleaner(self, *arrayLike:Iterable) -> None:
        for x in arrayLike:
            if isinstance(x, Iterable):
                for y in x:
                    if y != None:
                        y.destroy()
                x.clear()
            else:
                if x != None:
                    x.destroy()
    
    def shownListManagement(self, mode:str, newData:str, indexTo = -1):
        if mode == "add":
            if indexTo == -1:
                self.mylistBox.insert(tkinter.END, str(self.mylistBox.size() + 1)+". "+newData)
            else:
                self.mylistBox.insert(indexTo, newData)
        elif mode == "del":
            if indexTo == -1:
                self.mylistBox.delete(tkinter.END)
            else:
                self.mylistBox.delete(indexTo)
        
    def waitUntilIconDetected(self, image, region: tuple[int]):
        try:
            if not self.IOController.iconDetection(image, region):
                self.executePointer -= 1
        except Exception as e:
            print("error occured, wait for a moment and try again.")
            print(e)
            self.executePointer -= 1
            
    def timeWait(self, timeCount:int):
        if self.counter == -1:
            self.counter = time.time()
        if time.time() - self.counter < timeCount:
            self.executePointer -= 1
        else:
            self.counter = -1

    def loopController(self, loopBackTo:int, loopTime:int, loopID:int):
        print(self.loopCounter)
        if len(self.loopCounter[loopID]) == 0:
            self.loopCounter[loopID].append(loopTime)
        if self.loopCounter[loopID][0] > 0 or self.loopCounter[loopID][0] == -1:
            self.executePointer = copy.deepcopy(loopBackTo) - 1
            self.loopCounter[loopID][0] -= int(loopTime > 0)

    def drawer(self) -> int:
        if self.listener != None:


            if self.screenShot == 1 and self.__num > 0:  # 1是截图功能的id，number是多少个画了多少个矩形。
                temx, temy = self.listener.mouseGet("left")  # 鼠标的绝对坐标。

                temx = (temx * self.width) / self.screen.width  # 转换相对坐标。
                temy = (temy * self.height) / self.screen.height

                # print("call:",temx,temy)
                if self.x == -10 or self.y == -10:  # prevent first click detection
                    self.x = -1
                    self.y = -1
                elif (temx != self.x or temy != self.y) and (temx != -1 and temy != self.y):  # 防止长度和宽度为0的矩形。
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

        if self.x == 0 or self.y == 0:  # 紧急退出
            self.listener.terminate()
            self.__root.destroy()
            return -1

        return 1

    def canvasPlace(self, positionX=0, positionY=0, highlightthickness=0, bgColor="black", target="root") -> None:

        if target == "sub":
            self.__canvas = tkinter.Canvas(self.screenShotor, highlightthickness= \
                highlightthickness, width=self.width, height=self.height, bg=bgColor)
        else:
            self.__canvas = tkinter.Canvas(self.__root, highlightthickness= \
                highlightthickness, width=self.width, height=self.height, bg=bgColor)
        self.__canvas.place(x=positionX, y=positionY)

    def rectangleCreation(self, positionX=0, positionY=0, rightX=0, rightY=0, outline="crimson", \
                          width=3, dash=(1, 1)) -> None:

        self.__rec.append(self.__canvas.create_rectangle(positionX, positionY, rightX, rightY, \
                                                         outline=outline, width=width, dash=dash))
        print("coor:", self.__canvas.coords(self.__rec[-1]))

    def rectangleConfigure(self, positionX=0, positionY=0, rightX=0, rightY=0, outline="crimson", \
                           width=3, index=-1, dash=(1, 1)) -> None:

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
        
    def clickOnButton(self, image, region: tuple[int]) -> None:
        print(type(image))
        # image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        print(region)
        help_pos = pyautogui.locateOnScreen(image,confidence=0.7,region=region, minSearchTime = 1) #region中的参数为xy起始点，宽度和高度
        print("----------------")
        print(help_pos)
        if help_pos != None:
            # print(help_pos)
            goto_pos = pyautogui.center(help_pos) # 找到传回图片的中心点,并传回坐标
            self.move_and_press_mouse(goto_pos.x, goto_pos.y)
            print(goto_pos)
            
    def iconDetection(self, image, region: tuple[int]) -> bool:
        # image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        help_pos = pyautogui.locateOnScreen(image,confidence=0.7,region=region, minSearchTime = 1) #region中的参数为xy起始点，宽度和高度
        # print("----------------")
        # print(help_pos)
        if help_pos != None:
            return True
        else:
            return False


class OCRController():
    def __init__(self, path, incodeFile) -> None:
        # pytesseract.pytesseract.tesseract_cmd = r""
        self.sct = mss()
        self.currentPath = path
        self.ocr = PaddleOCR(use_angle_cls = True, lang = "ch",
                rec_model_dir = self.currentPath + "\\inference\\ch_PP-OCRv4_rec_infer\\",
                cls_model_dir = self.currentPath + "\\inference\\ch_ppocr_mobile_v2.0_cls_infer\\",
                det_model_dir = self.currentPath + "\\inference\\ch_PP-OCRv4_det_infer\\") 

        # print(incodeFile)
        self.kmeans = None
        self.centroids, self.data ,self.modelID, self.relativeDistance = incodeFile
        self.centroids, self.data ,self.modelID = np.array(self.centroids), \
            np.array(self.data), np.array(self.modelID)
        self.temResult = []
        self.modelLabels = []
        self.relativeDistance = list(self.relativeDistance)
        
        self.screen = np.array([])
        
        arrivedResult = []
        # print(self.modelLabels, self.centroids, self.data ,self.modelID, self.relativeDistance)
        
    def __closest(self, a):
        return np.argmin(a)
    
    def __calculate_overlap(self, box1, box2):
        # Calculate the overlapping area between two text boxes
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])

        width = max(0, x2 - x1)
        height = max(0, y2 - y1)

        overlap_area = width * height
        return overlap_area
    
    def areTextTransfer(self, targetArea:dict, textPosition:list[dict] = [], match = False) -> list[str]:
        screen = np.array(self.sct.grab(targetArea))
        image_rgb = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

        result = self.ocr.ocr(image_rgb, cls=True)
        # print(result)
        txts = []
        for x in result:
            if match:
                boxes = [line[0] for line in x]
            txts = [line[1][0] for line in x]
            
        if match:
            print(boxes)
            print(textPosition)
            print(">>>>>>>>>>>>>>>>>>>>")
            matched_boxes = []

            for list_box in textPosition:
                max_overlap = 0
                matched_box = None

                for screen_box in range(len(boxes)):
                    tem = list_box.copy()
                    overlap_area = self.__calculate_overlap([tem["left"] - targetArea["left"], \
                        tem["top"] - targetArea["top"], tem["left"] - targetArea["left"] + tem["width"], \
                            tem["top"] - targetArea["top"] + tem["height"]], \
                            boxes[screen_box][0] + boxes[screen_box][2])
                    # print([tem["left"] - targetArea["left"], \
                    #     tem["top"] - targetArea["top"], tem["left"] - targetArea["left"] + tem["width"], \
                    #         tem["top"] - targetArea["top"] + tem["height"]], \
                    #         boxes[screen_box][0] + boxes[screen_box][2])
                    if overlap_area > max_overlap:
                        max_overlap = overlap_area
                        matched_box = screen_box

                if matched_box is not None:
                    matched_boxes.append(matched_box)
                else:
                    matched_boxes.append(0)
                    
            matched_boxes = np.array(matched_boxes, dtype = np.int32)
            targetText = np.array(txts)
            print(matched_boxes, targetText)
            print(targetText[matched_boxes])
            return list(targetText[matched_boxes])
        
        return txts
    
    def textboxSeekerTrainer(self, targetArea:dict, heightOfTarget:int) -> list[dict]:
        screen = np.array(self.sct.grab(targetArea))
        # print(screen.shape)
        # print(screen)
        gray_image = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # print(gray_image.shape)
        gray_image = np.array(gray_image, dtype = np.int32)
        
        self.KMEANSTrainer(gray_image, 2, 0, 500)
            
        class2 = np.where(self.modelLabels[-1] == 1)[0]
        result = []
        node = 0
        lastNode = 0
        for x in range(class2.shape[0]):
            if class2[x] > node:
                if node > (lastNode + 1):
                    tem=copy.deepcopy(targetArea)
                    tem["top"] = lastNode + targetArea["top"]
                    tem["height"] = node - lastNode
                    if heightOfTarget <= tem["height"]:
                        result.append(tem)
                    self.temResult.append(tem)
                    
                tem=copy.deepcopy(targetArea)
                tem["top"] = node + targetArea["top"]
                tem["height"] = class2[x] - node
                if heightOfTarget <= tem["height"]:
                    result.append(tem)
                self.temResult.append(tem)
                
                lastNode = copy.deepcopy(class2[x])
                node = copy.deepcopy(class2[x])
            node+=1
        self.temResult = copy.deepcopy(result)

        return result

        
    def __modeGetter(self,npArray):
        counts = np.bincount(npArray)
        
        return np.argmax(counts)

    def textboxSeekerPredictor(self, targetArea:dict, heightOfTarget:int, modelID:int, \
        meanThreshold = False) -> list[dict]:
        screen = np.array(self.sct.grab(targetArea))
        # print(screen.shape)
        # print(screen)
        gray_image = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # print(gray_image.shape)
        gray_image = np.array(gray_image, dtype = np.int32)
        
        labels = self.KMEANSPredictor(gray_image, modelID, 2, 500, 1)
        print(labels)
            
        class2 = np.where(labels == 1)[0]
        result = []
        self.temResult.clear()
        node = 0
        lastNode = 0
        heights = np.array([])
        for x in range(class2.shape[0]):
            if class2[x] > node:
                if node > (lastNode + 1):
                    tem=copy.deepcopy(targetArea)
                    tem["top"] = lastNode + targetArea["top"]
                    tem["height"] = node - lastNode

                    if heightOfTarget <= tem["height"]:
                        result.append(tem)
                    self.temResult.append(tem)
                    heights = np.append(heights, tem["height"])
                    
                tem=copy.deepcopy(targetArea)
                tem["top"] = node + targetArea["top"]
                tem["height"] = class2[x] - node
                if heightOfTarget <= tem["height"]:
                    result.append(tem)
                self.temResult.append(tem)
                heights = np.append(heights, tem["height"])

                lastNode = copy.deepcopy(class2[x])
                node = copy.deepcopy(class2[x])
            node+=1
        
        if meanThreshold:
            result = np.array(result)
            threshold = np.mean(heights)
            strongTextBoxes = np.where(heights > threshold)[0]
            heights = heights[strongTextBoxes]
            result = result[strongTextBoxes]
            inlier = np.where(heights < threshold * 2.5)[0]
            result = result[inlier]
            result = list(result)
            
        if len(result) == 0:
            result = [copy.deepcopy(targetArea)]
        # self.temResult = copy.deepcopy(result)


        return result
    
    def unexpectedResult(self, targetArea:dict, heightOfTarget:int):
        lastTextbox = None
        for x in range(len(self.temResult)):
            pass
            
    def textLocationTrainer(self, textArea:list[dict], screenArea:dict):
        screen = np.array(self.sct.grab(screenArea))
        # print(screen.shape)
        # print(screen)
        gray_image = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # print(gray_image.shape)
        gray_image = np.array(gray_image, dtype = np.int32)
        
        boundaryPixel = np.array([], dtype = np.int32)
        for x in range(len(textArea)):
            boundaryPixel = np.append(boundaryPixel, gray_image[textArea[x]["top"], textArea[x]["left"] : \
                textArea[x]["left"] + textArea[x]["width"]])
            
            boundaryPixel = np.append(boundaryPixel, gray_image[textArea[x]["top"] + textArea[x]["height"], \
                textArea[x]["left"] : textArea[x]["left"] + textArea[x]["width"]])
        
        self.KMEANSTrainer(boundaryPixel, 3, 1, 600, False)
        
    
    def textLocationPredictor(self, textArea:list[dict], screenArea:dict, modelID:int) -> bool:
        screen = np.array(self.sct.grab(screenArea))
        # print(screen.shape)
        # print(screen)
        gray_image = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # print(gray_image.shape)
        gray_image = np.array(gray_image, dtype = np.int32)
        
        
        boundaryPixel = np.array([], dtype = np.int32)
        for x in range(len(textArea)):
            boundaryPixel = gray_image[textArea[x]["top"], textArea[x]["left"] : \
                textArea[x]["left"] + textArea[x]["width"]].copy()
            
            labelsUpper = self.KMEANSPredictor(boundaryPixel, modelID, 3, 600, 1,\
                False, x == 0)
            print(labelsUpper)
            labelsUpper = np.diff(labelsUpper)
            if np.where(labelsUpper == self.__get_mode(labelsUpper))[0].shape[0]\
                < labelsUpper.shape[0] - 2:
                return False
            
            
            boundaryPixel = gray_image[textArea[x]["top"] + textArea[x]["height"], \
                textArea[x]["left"] : textArea[x]["left"] + textArea[x]["width"]].copy()
            
            labelsLower = self.KMEANSPredictor(boundaryPixel, modelID, 3, 600, 1,\
                False, False)
            print(labelsLower)
            labelsLower = np.diff(labelsLower)
            if np.where(labelsLower == self.__get_mode(labelsLower))[0].shape[0] < labelsLower.shape[0] - 2:
                return False

        return True
        
        
    def __get_mode(self, Kdarray:np.ndarray):
        # Flatten the array into a 1-dimensional array
        flattened_array = np.ravel(Kdarray)

        # Get the unique values and their counts
        unique_values, counts = np.unique(flattened_array, return_counts=True)

        # Find the index of the maximum count
        max_count_index = np.argmax(counts)

        # Get the mode value(s) from the unique values array
        mode_value = unique_values[max_count_index]

        return mode_value

        
    def textSeeker(self, textArea:list[dict], textboxArea:dict, screenArea:dict, modelID:int, \
        mode = "train", textHeight = -1, upper = -1, lower = -1):
        if mode == "train":
            print(textboxArea, textHeight)
            print(screenArea)
            result = []
            for y in range(0, textboxArea["height"] - textHeight, 2):
                print(y)
                counter = 0
                result = []
                temRelativeDis = []
                for x in range(len(textArea)):
                    if y == 0:
                        textArea[x]["top"] = textArea[x]["top"] - (upper - textboxArea["top"])
                    else:
                        textArea[x]["top"] += 2
                    print(textArea[x])
                        
                    temRelativeDis.append(textArea[x]["top"] - textboxArea["top"])
                        
                    tem = self.areTextTransfer(textArea[x])
                    print(tem)
                    print("---------------------------")
                    if len(tem) > 0:
                        result.append(tem[0])
                    else:
                        counter += 1
                        result.append(None)
                        
                if counter < len(result) and self.textLocationPredictor(textArea, screenArea, modelID):
                    self.relativeDistance[modelID].append(temRelativeDis)
                    break
            print(result, "<<<<<<<<<<<<<<<<<<<<<<")
            # return result
            return textArea
        else:
            satisfyFlag = []
            trainList = []
            result = []
            resultUpper = []
            resultLower = []
            if textHeight == -1 or upper == -1 or lower == -1:
                upper = 90000
                lower = 0
            for y in range(len(self.relativeDistance[modelID])):
                result = []
                resultUpper = []
                resultLower = []
                counter = 0
                counterUpper = 0
                counterLower = 0
                adjustAreaLower = []
                adjustAreaUpper = []
                for x in range(len(textArea)):
                    if y == 0:
                        trainList.append(textArea[x].copy())
                        if textHeight == -1:
                            upper = min(textArea[x]["top"], upper)
                            lower = max(textArea[x]["top"] + textArea[x]["height"], lower)
                    textArea[x]["top"] = self.relativeDistance[modelID][y][x] + textboxArea["top"]
                    adjustAreaLower.append(textArea[x].copy())
                    adjustAreaLower[-1]["top"] += 2
                    adjustAreaUpper.append(textArea[x].copy())
                    adjustAreaUpper[-1]["top"] -= 2
                    

                    tem = self.areTextTransfer(adjustAreaUpper[-1])
                    print(tem)
                    if len(tem) > 0:
                        resultUpper.append(tem[0])
                    else:
                        counterUpper += 1
                        resultUpper.append(None)
                        
                    tem = self.areTextTransfer(textArea[x])
                    print(tem)
                    if len(tem) > 0:
                        result.append(tem[0])
                    else:
                        counter += 1
                        result.append(None)
                        
                        
                    tem = self.areTextTransfer(adjustAreaLower[x])
                    print(tem)
                    print("---------------------------")
                    if len(tem) > 0:
                        resultLower.append(tem[0])
                    else:
                        counterLower += 1
                        resultLower.append(None)
                        
                    
                if textHeight == -1:
                    textHeight = lower - upper
                    
                if self.textLocationPredictor(textArea, screenArea, modelID) and counter < len(result):
                    satisfyFlag.append(True)
                    break
                elif self.textLocationPredictor(adjustAreaUpper, screenArea, modelID) and counterUpper < len(resultUpper):
                    satisfyFlag.append(True)
                    break
                elif self.textLocationPredictor(adjustAreaLower, screenArea, modelID) and counterLower < len(resultLower):
                    satisfyFlag.append(True)
                    break
                else:
                    satisfyFlag.append(False)
                    
            print(satisfyFlag)
            if True in satisfyFlag:
                valid = satisfyFlag.index(True)
                if valid == 0:
                    # return result
                    print(result, "<<<<<<<<<<<<<<<<<<<<<<")
                    return textArea
                elif valid == 1:
                    # return resultUpper
                    print(resultUpper, "<<<<<<<<<<<<<<<<<<<<<<")
                    return adjustAreaUpper
                else:
                    # return resultLower
                    print(resultLower, "<<<<<<<<<<<<<<<<<<<<<<")
                    return adjustAreaLower
            else:
                return self.textSeeker(trainList, textboxArea, screenArea, modelID, "train", textHeight, upper, lower)

        
    def KMEANSTrainer(self, gray_image:np.ndarray, n_clusters = 2,random_state = 0, max_iter = 500, mode = True):
        
        if mode:
            patterns = np.apply_along_axis(self.__modeGetter, 1, gray_image) # modes of each row
        else:
            patterns = gray_image.copy()
        # print(patterns)
        # print(patterns.shape)
        scaled_data = np.divide(patterns,255)
        
        scaled_data = np.reshape(scaled_data, (-1, 1))
        # print(scaled_data)
        scaled_data = np.insert(scaled_data, 1, 0,axis=1)
        # print(scaled_data)
        # print(">>>>>>>>>>>>>>>>>>>>>>")
        
        self.data = list(self.data)
        self.data.append(scaled_data)
        # print(self.data)
        self.data = np.array(self.data, dtype = object)
        # print(">>>.....>>>>>>>")
        self.kmeans = KMeans(n_clusters = n_clusters, random_state = random_state, max_iter = max_iter)
        self.kmeans.fit(scaled_data)
        
        self.modelLabels = list(self.modelLabels)
        self.modelLabels.append(self.kmeans.labels_)
        # print(self.modelLabels)
        self.modelLabels = np.array(self.modelLabels, dtype = object)
        
        # print(">>>.....>>>>>>>")
        self.relativeDistance.append([])

        self.centroids = list(self.centroids)
        self.centroids.append(self.kmeans.cluster_centers_)
        # print(self.centroids)
        self.centroids = np.array(self.centroids, dtype = object)
        # print(self.centroids)
        # print(self.modelLabels)
        # class1 = np.where(self.modelLabels == 0)[0]
        if self.modelID.shape[0] == 0:
            self.modelID = np.append(self.modelID, 0)
        else:
            self.modelID = np.append(self.modelID, copy.deepcopy(self.modelID[-1]) + 1)
            
    def KMEANSPredictor(self, gray_image:np.ndarray, modelID:int, n_clusters = 2, max_iter = 500, n_init = 1, \
        mode = True, newModel = True) -> np.ndarray:
        
        if mode:
            patterns = np.apply_along_axis(self.__modeGetter, 1, gray_image) # modes of each row
        else:
            patterns = gray_image.copy()
        # print(patterns)
        # print(patterns.shape)
        scaled_data = np.divide(patterns,255)
        scaled_data = np.reshape(scaled_data, (-1, 1))
        # print(scaled_data)
        scaled_data = np.insert(scaled_data, 1, 0,axis=1)
        
        if newModel:
            self.kmeans = KMeans(n_clusters = n_clusters, max_iter = max_iter, init = self.centroids[modelID], \
                n_init = n_init)
            self.kmeans.fit(self.data[modelID])
        labels = self.kmeans.predict(scaled_data)
        
        return labels


class edit_excel():
    """
    1. read_npy(): 读取npy文件，npy文件内为每个page的title，请不要直接打开该文件进行修改。
    2. save_title(): 存入npy文件
    3. new_data_excel(page_title=[], list_Title=[], list_Data=[], member_list=[], mod=0): 进行模式选择
    默认模式为mod=0，即进行”x月_部落战.xlsx“的存入数据,只填写 page_title, list_Title, list_Data 这三个参数;
    当mod=1, 即进行"人员信息统计.xlsx"的存入数据的操作,只填写 member_list和 mod=1 。
    4. open_and_close_txt(): 该函数为try, except, 将报错信息填入txt中。
    5. create_new_folder(),create_new_excel(),create_and_import_sheet()已经集成到了new_data_excel()中，无需
    调用 (mod=0)。
    6. edit_sheet对部落战excel的操作, 未完成
    7. import_member_information(), 已经集成到new_data_excel()中,(mod=1)
    8. edit_member_information(information_edit), 对人员信息进行修改，只填入一个list，注意需要一一对应，并且其中标签
    元素不能被修改。
    9. search_member_information(label)，通过标签来搜索人员全部信息。



    """
    def __init__(self) -> None:
        self.currentPath = os.getcwd()
        self.title_list = []
        self.excel_name = ""
        self.path_now = ""

    def OCRModelDataSaver(self, centroids:np.ndarray, data:np.ndarray, \
        modelID:np.ndarray, relativeDistance:list) ->None :
        """
            `OtherInfo`: [clustersNumber, max_iteration]
        """
        print(centroids, data, modelID, relativeDistance)#, centroids, data, modelID, relativeDistance
        arr = np.array([list(centroids), list(data), list(modelID), list(relativeDistance)], dtype=object)
        
        np.save("textBoxesInfer.npy", arr, allow_pickle=True, fix_imports=True)
        
        print("saved:", arr)

    def OCRModelDataLoader(self) -> np.ndarray:
        file_path = os.path.join(self.currentPath, "textBoxesInfer.npy")

        if os.path.exists(file_path):
            inCodeFile = np.load("textBoxesInfer.npy", allow_pickle = True)

        else:
            inCodeFile = np.array([[], [], [], []], dtype = object)

        
        print("loaded:", inCodeFile)
        return inCodeFile
    
    def filT(self,tem)->bool:
        return os.path.isfile(self.currentPath+"\\UI\\"+tem)
    
    def UIImageList(self) -> list[str]:
        if not os.path.isdir(self.currentPath + "\\UI"):
            os.makedirs(self.currentPath + "\\UI")
            
        return list(filter(self.filT,os.listdir(self.currentPath+"\\UI")))

    def read_npy(self, path):
        if os.path.exists(path):

            the_title_list_np = np.load(path)
            the_title_list = list(the_title_list_np)
            return the_title_list
        else:
            the_title_list = []
            return the_title_list

    def save_title(self, title, path):
        title_np = np.array(title)
        np.save(path, title_np)

    def new_data_excel(self, page_title=[], list_Title=[], list_Data=[], member_list=[], mod=0):
        try:
            if mod == 0:
                self.create_new_folder()
                self.create_new_excel(0)
                self.create_and_import_sheet(page_title, list_Title, list_Data)
            elif mod == 1:
                self.create_new_folder()
                self.create_new_excel(1)
                self.import_member_information(member_list)
        except Exception as e:
            self.open_and_close_txt(e)

    # 打开日志并且填入错误信息
    def open_and_close_txt(self, e):
        localDate = re.sub(r"[ :]+", "-", str(time.asctime(time.localtime(time.time()))))
        f3 = open("log.txt", "a")
        f3.write(localDate + ": " + str(e) + "\n")
        f3.close()

    # 下面三个function要一起调用才是某月数据
    # 创建文件夹（数据库）
    def create_new_folder(self):
        try:
            if not os.path.isdir(self.currentPath + "\\data"):
                os.makedirs(self.currentPath + "\\data")
                self.path_now = self.currentPath + "\\data"
            else:
                self.path_now = self.currentPath + "\\data"
        except Exception as e:
            self.open_and_close_txt(e)


    # name是新excel的名字，请包含完整信息，比如“xxxx.xlsx”，mod默认为0
    def create_new_excel(self, mod=0):
        try:
            if mod == 0:
                current_timestamp = time.time()
                current_time = time.localtime(current_timestamp)
                # 提取当前月份
                current_month = current_time.tm_mon
                name = str(current_month) + "月_部落战.xlsx"
                file_path = os.path.join(self.path_now, name)
                if os.path.exists(file_path):  # 判断该excel是否存在于这个文件夹中
                    self.excel_name = name
                    print("已经存在")
                else:
                    df = pd.DataFrame()
                    df.to_excel(file_path, index=False)
                    self.excel_name = name
            elif mod == 1:
                name = "人员信息统计.xlsx"
                file_path = os.path.join(self.path_now, name)
                if os.path.exists(file_path):  # 判断该excel是否存在于这个文件夹中
                    self.excel_name = name
                    print("已经存在")
                else:
                    workbook = openpyxl.Workbook()
                    sheet = workbook.active
                    sheet['A1'] = '昵称'
                    sheet['B1'] = '标签'
                    sheet['C1'] = '加入'
                    sheet['D1'] = '最近退出'
                    sheet['E1'] = '差值'
                    sheet['F1'] = '常驻认证T/F'
                    workbook.save(file_path)
                    self.excel_name = name
        except Exception as e:
            self.open_and_close_txt(e)

    # 导入数据
    def create_and_import_sheet(self, page_title, list_Title, list_Data):
        try:
            file_path = os.path.join(self.path_now, self.excel_name)
            npy_path = os.path.join(self.path_now, self.excel_name + ".npy")
            print("excel name is: " + self.excel_name)
            self.title_list = self.read_npy(npy_path)

            start_column = 0
            start_column_letter = ""
            actual_page_title_row = 1  # page 的名字的行数
            actual_list_title_row = 2  # 数据的名字的行数

            wb = openpyxl.load_workbook(file_path)  # 展开合并单元格
            ws = wb.active

            if page_title[0] not in self.title_list:  # title_list是page的标题
                self.title_list.append(page_title[0])
                page_number = self.title_list.index(page_title[0])
                start_column = 7 * page_number + 1  # 开始列名的数字
                for i in range(0, len(list_Title)):
                    ws[openpyxl.utils.get_column_letter(start_column + i) + str(actual_page_title_row)] = page_title[0]
                    ws[openpyxl.utils.get_column_letter(start_column + i) + str(actual_list_title_row)] = list_Title[i]
            else:
                page_number = self.title_list.index((page_title[0]))
                start_column = 7 * page_number + 1
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
                # print(list_Data[i])
                ws[openpyxl.utils.get_column_letter(start_column + i) + str(actual_list_title_row + count)] \
                    = list_Data[i]
            title_column = 0
            while ws[openpyxl.utils.get_column_letter(1 + title_column * 7) + str(1)].value is not None:
                start_row = 1
                end_row = 1
                start_column = title_column * 7 + 1
                end_column = 7 + title_column * 7
                ws.merge_cells(start_row=start_row, end_row=end_row, start_column=start_column, end_column=end_column)

                title_column += 1
            wb.save(file_path)
            self.save_title(self.title_list, npy_path)
            wb.close()
        except Exception as e:
            self.open_and_close_txt(e)

    # 编辑数据，
    def edit_sheet(self, excel_name, page_title, list_Title, list_Data):
        try:
            file_path = os.getcwd() + "\\data\\" + excel_name[0]
            wb = openpyxl.load_workbook(file_path)
            ws = wb.active

            col_num = 0
            for column in ws.iter_cols(min_row=1, max_row=1):
                for cell in column:
                    if cell.value == page_title[0]:
                        col_num = cell.column
                        # print(f"The data is in column {col_num}")

            print(col_num)
            target_name = str(list_Data[1])
            the_row = 2
            for row in ws.iter_rows(min_row=2, values_only=True):
                if str(row[col_num]) == target_name:
                    i = col_num
                    for col, data in enumerate(list_Data, start=0):  # 修改整行数据
                        # print(1)
                        cell = ws.cell(row=the_row, column=i)
                        # print(2)
                        cell.value = data
                        i += 1

                    break  # 找到匹配行后跳出循环
                the_row += 1
            wb.save(file_path)
            wb.close()
        except Exception as e:
            self.open_and_close_txt(e)



    # 下面这个function和create_new_folder一起调用，是对人员信息的添加
    def import_member_information(self, member_list):
        try:
            print(member_list)
            name = os.path.join(self.path_now, self.excel_name)
            workbook = openpyxl.load_workbook(name)
            sheet = workbook.active
            new_row = sheet.max_row + 1
            for col, data in enumerate(member_list, start=1):
                sheet.cell(row=new_row, column=col, value=data)
            workbook.save(name)
            workbook.close()
        except Exception as e:
            self.open_and_close_txt(e)

    # 进行人员信息修改
    def edit_member_information(self, information_edit):
        # print(information_edit)
        try:
            path = os.getcwd() + "\\data\\人员信息统计.xlsx"
            workbook = openpyxl.load_workbook(path)
            sheet = workbook.active
            target_name = str(information_edit[1])
            # print(type(target_name))
            target_column = 2
            count = 2
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if str(row[target_column - 1]) == target_name:
                    i = 1
                    for col, data in enumerate(information_edit, start=0):  # 修改整行数据
                        cell = sheet.cell(row=count, column=i)
                        cell.value = data
                        i += 1
                    break  # 找到匹配行后跳出循环
                count += 1

            workbook.save(path)
            workbook.close()
        except Exception as e:
            self.open_and_close_txt(e)

    def search_member_information(self, label):
        try:
            path = os.getcwd() + "\\data\\人员信息统计.xlsx"
            workbook = openpyxl.load_workbook(path)
            sheet = workbook.active

            target_value = label
            target_column = "B"

            target_row = None
            for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=1, max_col=3):
                if row[1].value == target_value:
                    target_row = row[1].row
                    break
            if target_row is not None:
                row_data = [cell.value for cell in sheet[target_row]]
                workbook.close()
                return row_data
            else:
                print("Target value not found in the specified column.")
                workbook.close()
        except Exception as e:
            self.open_and_close_txt(e)

    def delete_member_information(self, label):
        try:
            path = os.getcwd() + "\\data\\人员信息统计.xlsx"
            workbook = openpyxl.load_workbook(path)
            sheet = workbook.active
            data_to_delete = label
            for row in sheet.iter_rows(min_row=2, min_col=2, max_col=2):
                for cell in row:
                    if cell.value == data_to_delete:
                        # 找到要删除的数据所在的行
                        sheet.delete_rows(cell.row)
                        break  # 删除完毕，结束查找
            workbook.save(path)
            workbook.close()
        except Exception as e:
            self.open_and_close_txt(e)
            
    def allMemberLabel(self):
        try:
            path = os.getcwd() + "\\data\\人员信息统计.xlsx"
            df = pd.read_excel(path)
            print(df)
            
            return list(df["标签"])
            
        except Exception as e:
            self.open_and_close_txt(e)
        
        

class UserBehaviourController():
    def __init__(self, mouseCon:mouse_control, mouseDetect:eventMouse, OCRCon:OCRController, \
        dbManagement:edit_excel, mainCon:windowsUI) -> None:
        
        self.recoredBehaviours = []
        self.behavioursInterpreter = {"leftClick":mouseCon.move_and_press_mouse, "clickOnButton":\
            mouseCon.clickOnButton, "timeWait":mainCon.timeWait, "iconDetection": mainCon.waitUntilIconDetected,\
                "loopController":mainCon.loopController}
        self.oldPointer = len(self.recoredBehaviours)
        
        
    def actionRecord(self, action:str, param, actionID = -1, edit = -1):
        if actionID == -1 or actionID >= len(self.recoredBehaviours):
            self.recoredBehaviours.append([])
            actionID = -1
        
        if edit == -1:
            self.recoredBehaviours[actionID].append((action, param))
            
        else:
            self.recoredBehaviours[actionID][edit] = (action, param)
        
    def actionExcute(self, actionID:int, step = -1):
        if len(self.recoredBehaviours) > 0:
            return self.behavioursInterpreter[self.recoredBehaviours[actionID][step][0]], \
                self.recoredBehaviours[actionID][step][1]
        
        
    def delRecord(self, actionID = -1, newDataDel = True):
        if newDataDel:
            if len(self.recoredBehaviours) > 0 and len(self.recoredBehaviours) > self.oldPointer:
                self.recoredBehaviours.pop(actionID)
        else:
            if len(self.recoredBehaviours) > 0:
                self.recoredBehaviours.pop(actionID)


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
    # con.mouse.press(Button.left)
    # con.smooth(1913,195,500)
    # con.mouse.release(Button.left)
    # ocr=OCRController(os.getcwd())
    # text=ocr.textboxSeekerTrainer({"top": 0, "left": 0, "width": 1920, "height": 1080})
    # print(text)
    test = edit_excel()
    # test.new_data_excel(member_list = ["sk","#YHHJJK",000,1,1,"T"],mod=1)
    print(test.search_member_information("#YHHJJK"))
    # print(test.allMemberLabel())
