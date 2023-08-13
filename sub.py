import math
import copy
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
from sklearn.cluster import KMeans
from collections.abc import Iterable
from tkinter.messagebox import *


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
            "3000": show result
            "3010": show message box and wait for user to choose
    """

    def __init__(self, override=False, alpha=0.8, bgColor="black", screenShot=-1, \
                 width=-1, height=-1, positionX=0, positionY=0, listener: eventMouse = None) -> None:
        # self.__timeList=[time.time(),0]
        self.test = False # enable test code
        self.testNum = 0
        
        self.listener = eventMouse()
        self.keyBoardInterrupt = eventKeyboard()
        self.screenShot = screenShot
        self.screen = screeninfo.get_monitors()[0]
        # print("22222222222222222222222333333333333333333333")
        self.mainPanelButtons = ({"Recognition Area Record": [1100], "Setting": [1101], "next page": [1102], "testRecord": [1103]},
                                {"Mouse Click": [1110], "Mouse Hold": [1111], "Mouse Move": [1112], "Scorlling": [1113],\
                                    "Text Recognize": [1114], "Loop": [1115], "Standby": [1116]})
        # Store the buttons on main Panel and their status ID
        self.currentButton: list[tkinter.Button] = []
        self.currentLabel = []
        self.currentOtherComponents = []

        self.statusID = 1000  # globel status flag
        self.__subWindows = None  # store windows created by event function Start()
        self.messageBox = None

        self.__rec = []  # store rectangle in canvas
        self.recoredArea = [] # store recorded screen shot area
        self.textBoxes = [] # store recognized text boxes
        self.textAreUpperBound = self.screen.height
        self.textAreLowerBound = 0
        
        
        self.x = -10  # store mouse click coordinations
        self.y = -10
        
        self.dbManagement = edit_excel()
        self.ocr = OCRController(self.dbManagement.currentPath, self.dbManagement.OCRModelDataLoader())

        self.xRight = -1  # store mouse move coordinations
        self.yRight = -1

        # self.__loopTime = 0  # use to count the time, 0.1s every loop
        self.__counter = 0  # status id for drawer function
        self.counter = 0
        self.__root = tkinter.Tk()
        self.windowSize = {"root": [width, height, positionX, positionY], "screenShoter": [0, 0, 0, 0]}  # all type of window size

        self.width = width  # current use width and height
        self.height = height
        self.bgColor = bgColor
        self.alpha = alpha
        
        self.positionX = positionX
        self.positionY = positionY
        
        IOController = mouse_control()
        self.userInteraction = UserBehaviourController(IOController, self.listener, self.ocr,\
            self.dbManagement)

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

    def layOutController(self, mode="root", view=0, lastmode = None) -> None:
        counter = 0
        buttonNum = len(self.mainPanelButtons[view].keys())
        if mode == "root":
            self.widgetsCleaner(self.currentButton, self.currentLabel)

        elif mode == "record":
            self.widgetsCleaner(self.currentButton, self.currentLabel)
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
            
            self.__root.geometry("{0}x{1}+{2}+{3}" \
                .format(self.width, self.height, self.positionX, self.positionY))
            
            self.__root.resizable(0, 0)
            
            
        for x in self.mainPanelButtons[view].keys():# place buttons
            counter += 1
            tem = self.__lambdaCreater(self.mainPanelButtons[view][x][0])
            print(self.mainPanelButtons[view][x][0])
            self.currentButton.append(tkinter.Button(self.__root, text=x, command=tem))
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

    def subWindowCreater(self, height, weight, lastMode = "root", x = 100, y = 100, \
        listener = "None", alphaValue = 0.8, bgColor = "black"):
        
        self.__subWindows = tkinter.Toplevel()  # set up sub window
        self.windowSize[lastMode] = []  # back up the size of last window
        self.windowSize[lastMode].append(self.width)
        self.windowSize[lastMode].append(self.height)
        self.windowSize[lastMode].append(self.positionX)
        self.windowSize[lastMode].append(self.positionY)
        
        self.width = weight
        self.height = height
        self.positionX = x
        self.positionY = y
        
        self.__subWindows.attributes("-alpha", alphaValue)

        self.__subWindows.geometry("{0}x{1}+{2}+{3}" \
                                   .format(self.width, self.height, x, y))
        self.__subWindows.configure(bg=bgColor)

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
        self.__subWindows = tkinter.Toplevel()  # set up sub window
        self.windowSize["root"] = []  # back up the size of root window
        self.windowSize["root"].append(self.width)
        self.windowSize["root"].append(self.height)
        self.windowSize["root"].append(self.positionX)
        self.windowSize["root"].append(self.positionY)
        
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
            self.statusID = 1010
            self.layOutController("record", 1, "root")
            
        elif status == 1103:
            self.screenShotCreation()
            # self.subWindows.append(windowsUI(True,0.5,"black",listener=mouseL,screenShot=3))
            # print("!!!!!!!!!!!!!!!!!!")
            self.__root.attributes("-alpha", 0)
            self.statusID = 2000
            # print("Start:",self.statusID)
            
        elif status == 1110:
            self.messageBox = showinfo("RseMessager", "Please click what you would like us to\
                click after pressing 'ok'. This message could be close in setting panel.")
            if self.listener == None:
                self.listener = eventMouse()
                self.listener.StartListener()
            self.statusID = 2010
        
        
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
            tem = self.recoredArea.pop()
            text = self.ocr.areTextTransfer(tem)
            # textBoxes = self.ocr.textboxSeekerTrainer(tem, 50)

            print(text)
            
    def eventAction(self) -> None:
        
        if self.statusID == 2000:
            if self.keyBoardInterrupt.statusGet() == 2:
                # print("ssssssssssssssss",self.statusID)
                self.x = -10
                self.y = -10
                self.screenShot = 2

                for x in self.__rec:
                    transformed = self.transform(x)
                    if self.counter == 1:
                        self.textAreUpperBound = min(transformed["top"] , self.textAreUpperBound)
                        self.textAreLowerBound = max(transformed["top"] + transformed["height"],\
                            self.textAreLowerBound)
                    print(self.textAreUpperBound, self.textAreLowerBound)
                    
                    self.recoredArea.append(transformed)
                    print(transformed)
                self.widgetsCleaner(self.__canvas, self.__subWindows)
                self.__rec.clear()
                self.__root.attributes("-alpha", self.alpha)
                self.counter += 1
                
                self.statusID = 1000
                
        elif self.statusID == 2010:
            clickedX, clickedY = self.listener.mouseGet("left")
            if clickedX != -1 and clickedY != -1:
                self.UserBehaviourController
                
        elif self.statusID == 3000:
            if self.keyBoardInterrupt.statusGet() == 2:
                # print("ssssssssssssssss",self.statusID)
                self.x = -10
                self.y = -10
                self.screenShot = 2

                self.widgetsCleaner(self.__canvas, self.__subWindows)
                self.__rec.clear()
                self.__root.attributes("-alpha", self.alpha)
                
                self.statusID = 1000
                
        elif self.statusID == 3010:
            pass
        
    
    def widgetsCleaner(self, *arrayLike:Iterable) -> None:
        for x in arrayLike:
            if isinstance(x, Iterable):
                for y in x:
                    y.destroy()
                x.clear()
            else:
                x.destroy()
    

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
        # print(self.modelLabels, self.centroids, self.data ,self.modelID, self.relativeDistance)
        
    def areTextTransfer(self, targetArea:dict) -> list[str]:
        screen = np.array(self.sct.grab(targetArea))
        image_rgb = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        
        result = self.ocr.ocr(image_rgb, cls=True)
        txts = []
        for x in result:
            # boxes = [line[0] for line in x]
            txts = [line[1][0] for line in x]
            # scores = [line[1][1] for line in x]
        # cv2.namedWindow("Hello", cv2.WINDOW_AUTOSIZE)
        # cv2.imshow("Hello", screen)
        # cv2.waitKey(0)
        # end1=time.time()

        # print(pytesseract.get_languages(config=''))
        # text = pytesseract.image_to_string(threshold_image, config=config)
        return txts
    
    def textboxSeekerTrainer(self, targetArea:dict, heightOfTarget:int) -> list[dict]:
        screen = np.array(self.sct.grab(targetArea))
        # print(screen.shape)
        # print(screen)
        gray_image = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # print(gray_image.shape)
        gray_image = np.array(gray_image, dtype = np.int32)
        # print(gray_image)
        # print("-----------------------")
        
        # patterns = np.apply_along_axis(self.__modeGetter, 1, gray_image) # modes of each row
        # # print(patterns)
        # # print(patterns.shape)
        # scaled_data = np.divide(patterns,255)
        
        # scaled_data = np.reshape(scaled_data, (-1, 1))
        # # print(scaled_data)
        # scaled_data = np.insert(scaled_data, 1, 0,axis=1)
        # # print(scaled_data)
        # # print(">>>>>>>>>>>>>>>>>>>>>>")
        
        # self.data = list(self.data)
        # self.data.append(scaled_data)
        # self.data = np.array(self.data, dtype = object)
        
        # self.kmeans = KMeans(n_clusters=2, random_state=0, max_iter=500)
        # self.kmeans.fit(scaled_data)
        
        # self.modelLabels = list(self.modelLabels)
        # self.modelLabels.append(self.kmeans.labels_)
        # self.modelLabels = np.array(self.modelLabels, dtype = object)

        # self.centroids = list(self.centroids)
        # self.centroids.append(self.kmeans.cluster_centers_)
        # self.centroids = np.array(self.centroids, dtype = object)
        # # print(self.centroids)
        # # print(self.modelLabels)
        # # class1 = np.where(self.modelLabels == 0)[0]
        # if self.modelID.shape[0] == 0:
        #     self.modelID = np.append(self.modelID, 0)
        # else:
        #     self.modelID = np.append(self.modelID, copy.deepcopy(self.modelID[-1]) + 1)
        
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
        # print(patterns[class1])
        # print("<<<<<<<<<<<<<<<")
        # print(patterns[class2])
        # new_samples = scaler.transform(new_data)  # Scale the new samples
        # predicted_labels = self.kmeans.predict(new_samples)

        
    def __modeGetter(self,npArray):
        counts = np.bincount(npArray)
        
        return np.argmax(counts)

    def textboxSeekerPredictor(self, targetArea:dict, heightOfTarget:int, modelID:int) -> list[dict]:
        screen = np.array(self.sct.grab(targetArea))
        # print(screen.shape)
        # print(screen)
        gray_image = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # print(gray_image.shape)
        gray_image = np.array(gray_image, dtype = np.int32)
        # print(gray_image)
        # print("-----------------------")
        # patterns = np.apply_along_axis(self.__modeGetter, 1, gray_image) # modes of each row
        # # print(patterns)
        # # print(patterns.shape)
        # scaled_data = np.divide(patterns,255)
        # scaled_data = np.reshape(scaled_data, (-1, 1))
        # # print(scaled_data)
        # scaled_data = np.insert(scaled_data, 1, 0,axis=1)
        
        # self.kmeans = KMeans(n_clusters=2, max_iter=500, init = self.centroids[modelID], n_init = 1)
        # self.kmeans.fit(self.data[modelID])
        # labels = self.kmeans.predict(scaled_data)
        labels = self.KMEANSPredictor(gray_image, modelID, 2, 500, 1)
        print(labels)
            
        class2 = np.where(labels == 1)[0]
        result = []
        self.temResult.clear()
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
        if len(result) == 0:
            result = copy.deepcopy(targetArea)
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
                        
                if counter == 0 and self.textLocationPredictor(textArea, screenArea, modelID):
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
                    
                if self.textLocationPredictor(textArea, screenArea, modelID) and counter == 0:
                    satisfyFlag.append(True)
                    break
                elif self.textLocationPredictor(adjustAreaUpper, screenArea, modelID) and counterUpper == 0:
                    satisfyFlag.append(True)
                    break
                elif self.textLocationPredictor(adjustAreaLower, screenArea, modelID) and counterLower == 0:
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
    def __init__(self) -> None:
        self.currentPath = os.getcwd()

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


class UserBehaviourController():
    def __init__(self, mouseCon:mouse_control, mouseDetect:eventMouse, OCRCon:OCRController, \
        dbManagement:edit_excel) -> None:
        
        self.recoredBehaviours = []
        self.behavioursInterpreter = {"leftClick":mouseCon.move_and_press_mouse}
        
        
        
    def actionRecord(self, action:str, param, actionID = -1, edit = -1):
        if actionID == -1 or actionID > self.recoredBehaviours:
            self.recoredBehaviours.append([])
            actionID = -1
        
        if edit == -1:
            self.recoredBehaviours[actionID].append((action, param))
            
        else:
            self.recoredBehaviours[actionID][edit] = (action, param)
        
    def actionExcute(self, actionID:int, step = -1):
        return self.behavioursInterpreter[self.recoredBehaviours[actionID][step][0]], \
            self.recoredBehaviours[actionID][step][1]
        


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
    ocr=OCRController(os.getcwd())
    text=ocr.textboxSeekerTrainer({"top": 0, "left": 0, "width": 1920, "height": 1080})
    # print(text)
