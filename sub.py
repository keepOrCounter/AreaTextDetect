import pynput,time,tkinter,screeninfo
from tkinter.font import Font
# import threading



class eventKeyboard():
    """
    pressed(key) is a internal function for key board listener, please do not
        invoke!
    NOTICE!!!  pressed(key) would check whether main program is down every 10 sec,
        to make it continous working, call activeFlagSet(newFlag=1) to reactive the working status.
        
    StartListener(): start the listener, also safe for any unterminate listener.
    terminate(): end the listener
    
    statusGet(): return listener status, 0 for initiated, 1 for started, 2 for specific keys were pressed,
        -1 for terminated.
    """
    def __init__(self) -> None:
        self.keyValue=-1
        self.timeIntervalStart=0
        self.timeIntervalEnd=0
        
        self.keysIntervalStart=0
        self.keysIntervalEnd=0
        
        self.activeFlag=-1
        self.keyPressed=pynput.keyboard.Listener(on_press=self.pressed)
        self.counter=0
        
        self.__status=0
        
    def pressed(self,key):
        # print("b")
        self.keysOkay=self.keysIntervalEnd-self.keysIntervalStart
        self.keysIntervalEnd=time.time()
        
        if str(type(key))=="<enum 'Key'>":
            if key.name=="alt_l":
                self.counter=1
                self.keysIntervalStart=time.time()
            else:
                self.counter=0
        else:
            self.keyValue=key.char
            if key.char=="z" and self.counter==1 and (0.0<=self.keysOkay<=1.0):
                self.__status=2
                return False
            else:
                self.counter=0
            # print(key.char=="z")
        
        self.timeIntervalEnd=time.time()
        
        if self.timeIntervalEnd-self.timeIntervalStart>10.0:
            # print("Times Up")
            if self.activeFlag==-1:
                self.__status=-1
                return False
            self.timeIntervalStart=time.time()
            self.activeFlag=-1
        
    def StartListener(self) -> None:
        if self.__status==-1 or self.__status==2:
            self.terminate()
            self.keyPressed=pynput.keyboard.Listener(on_press=self.pressed)
            
        self.__status=1
        self.keyPressed.start()
        self.timeIntervalStart=time.time()
            
    def terminate(self) -> None:
        self.keyPressed.stop()
        
    def keyGet(self) -> str:
        return self.keyValue
    
    def activeFlagSet(self,newFlag) -> None:
        self.activeFlag=newFlag
        
    def statusGet(self) -> str:
        return self.__status


class eventMouse():
    """
    clicked(x,y) and moving(x,y) are internal functions for key board listener, please do not
        invoke!
    NOTICE!!!  clicked(x,y) and moving(x,y) would check whether main program is down every 10 sec,
        to make it continous working, call activeFlagSet(newFlag=1) to reactive the working status.
        
    StartListener(): start the listeners.
    terminate(): end the listeners.
    
    mouseGet(): return the x,y coordinate for last time mouse clicked
    motionGet(): return the x,y coordinate for last time mouse moved
    """
    def __init__(self) -> None:
        self.timeIntervalStart=0
        self.timeIntervalEnd=0
        
        self.activeFlag1=-1
        self.activeFlag2=-1
        
        self.DetectedMouseXPos=-1
        self.DetectedMouseYPos=-1
        
        self.timeIntervalStartMotion=0
        self.timeIntervalEndMotion=0
        self.MotionMouseXPos=-1
        self.MotionMouseYPos=-1
        
        # keyPressed.stop()
        self.mouseClicked=pynput.mouse.Listener(on_click=self.clicked)
        self.mouseMove=pynput.mouse.Listener(on_move=self.moving)
        
        # mouseClicked.join()

    def moving(self, x,y):
        self.MotionMouseXPos=x
        self.MotionMouseYPos=y
        
        self.timeIntervalEndMotion=time.time()
        if self.timeIntervalEndMotion-self.timeIntervalStartMotion>10.0:
            print("Times Up")
            if self.activeFlag2==-1:
                print("exit")
                return False
            self.timeIntervalStartMotion=time.time()
            self.activeFlag2=-1

        
    def clicked(self, x, y, button, pressed):
        
        if pressed and button.name=="left":
            self.DetectedMouseXPos=x
            self.DetectedMouseYPos=y
            # print(self.DetectedMouseXPos,self.DetectedMouseYPos)
            
            
        self.timeIntervalEnd=time.time()
        # print(self.timeIntervalEnd-self.timeIntervalStart)
        if self.timeIntervalEnd-self.timeIntervalStart>10.0:
            # print("Times Up")
            if self.activeFlag1==-1:
                # print("exit")
                return False
            self.timeIntervalStart=time.time()
            self.activeFlag1=-1
            # if x==0 or y ==0:
            #     self.detectFlag=False
                # self.terminate()
            # return True


        # return True

    def StartListener(self) -> None:
        self.timeIntervalStart=time.time()
        self.mouseClicked.start()
        
        self.timeIntervalStartMotion=time.time()
        self.mouseMove.start()
        
    def terminate(self) -> None:
        self.mouseClicked.stop()
        self.mouseMove.stop()
        
    def mouseGet(self) -> int:
        return self.DetectedMouseXPos,self.DetectedMouseYPos
    
    def motionGet(self) -> int:
        return self.MotionMouseXPos,self.MotionMouseYPos
    
    def activeFlagSet(self,newFlag) -> None:
        self.activeFlag1=newFlag
        self.activeFlag2=newFlag
        
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
    def __init__(self,override=False,alpha=0.5,bgColor="black",screenShot=-1,\
        width=-1,height=-1,positionX=0,positionY=0,listener:eventMouse=None) -> None:
        # self.__timeList=[time.time(),0]
        self.listener=listener
        self.keyBoardInterrupt=eventKeyboard()
        self.screenShot=screenShot
        self.screen = screeninfo.get_monitors()[0]
        # print("22222222222222222222222333333333333333333333")
        self.mainPanelButtons=({"Recognition Area Record":[1100],"Setting":[1101],"next page":[1102]},)
        #Store the buttons on main Panel and their status ID
        self.currentButton:list[tkinter.Button]=[]
        self.currentLabel=[]
        self.currentOtherComponents=[]
        
        self.statusID=1000# globel status flag
        self.__subWindows=None# store windows created by event function Start()
        
        self.__rec=[]# store rectangle in canvas
        self.x=-10# store mouse click coordinations
        self.y=-10
        
        self.xRight=-1# store mouse move coordinations
        self.yRight=-1
        
        self.__loopTime=0# use to count the time, 0.1s every loop
        self.__counter=0# status id for drawer function
        
        self.__root = tkinter.Tk()
        self.windowSize={"root":[width,height],"screenShoter":[0,0]}# all type of window size
        
        self.width=width# current use width and height
        self.height=height
        self.bgColor=bgColor
        self.alpha=alpha

        if self.screenShot==1:
            self.__num=6
            self.canvasPlace()
            if width==-1:
                self.width=self.__root.winfo_screenwidth()
            if height==-1:
                self.height=self.__root.winfo_screenheight()
            
            # self.__root.overrideredirect(override)
            # self.__root.attributes("-alpha", alpha)
        elif self.screenShot==2:
            # temx=200*(1280/self.screen.width)
            # temy=70*(720/self.screen.height)
            # print(temx,temy)
            if width==-1:
                self.width=int(self.__root.winfo_screenwidth()/5)
            if height==-1:
                self.height=int(self.width*16/10)
            # print(self.width,self.height)
            self.layOutController()
            
        self.__root.overrideredirect(override)
        self.__root.attributes("-alpha", alpha)
            
        self.__root.geometry("{0}x{1}+{2}+{3}"\
            .format(self.width, self.height,positionX,positionY))
        self.__root.configure(bg=bgColor)
        self.__root.resizable(0,0)
        
        if self.listener!=None:
            self.listener.StartListener()
        if self.screenShot!=1:
            self.keyBoardInterrupt.StartListener()# listener to detect keyboard shortcut
        self.keeper()
        
        self.__root.mainloop()
        
    def layOutController(self,mode="root",view=0)->None:
        if mode=="root":
            buttonNum=len(self.mainPanelButtons[view].keys())
            counter=0
            for x in self.mainPanelButtons[view].keys():
                counter+=1
                tem=self.__lambdaCreater(self.mainPanelButtons[view][x][0])
                print(self.mainPanelButtons[view][x][0])
                self.currentButton.append(tkinter.Button(self.__root,text=x,command=tem))
                font=Font(font=self.currentButton[-1]["font"])# get font information
                lineHeight=font.metrics("linespace")# calculate hieght and weidth by font information
                lineWidth=font.measure(x)
                # print(lineHeight,lineWidth)
                # print()

                self.currentButton[-1].place(x=(self.width-lineWidth)/2,y=counter*self.height/(buttonNum+1)-lineHeight/2)
        else:
            pass
    
    def __lambdaCreater(self,x):# create lambda function for button, prevent shollow copy
        return lambda:self.Start(x)
    
    def screenShotCreation(self,alphaValue=0.5,bgColor="black")->None:
        """_summary_

        Args:
            alphaValue (int): the visibility of the screen shot window
            bgColor (str): allow for user to custom the back ground color
        """
        
        print(type(self.listener))
        self.__subWindows = tkinter.Toplevel()# set up sub window
        self.windowSize["root"]=[self.width,self.height]# back up the size of root window
        self.width = self.__subWindows.winfo_screenwidth()# make it large as the screen
        self.height = self.__subWindows.winfo_screenheight()
        
        self.__subWindows.overrideredirect(True)# remove tk default component(e.g. window close button)
        self.__subWindows.attributes("-alpha", alphaValue)
            
        self.__subWindows.geometry("{0}x{1}+{2}+{3}"\
            .format(self.width, self.height,0,0))
        self.__subWindows.configure(bg = bgColor)
        self.__num=6
        self.canvasPlace(target="sub")
        
        self.screenShot=1
        print("Screenshoter setted up")
        if self.listener==None:
            self.listener=eventMouse()
            self.listener.StartListener()
        
    def Start(self,status):
        print("111111111111111111111111")
        print(status)
        # print("Start:",self.statusID)
        if status==1100:# 
            self.screenShotCreation()
            # self.subWindows.append(windowsUI(True,0.5,"black",listener=mouseL,screenShot=3))
            # print("!!!!!!!!!!!!!!!!!!")
            self.__root.attributes("-alpha", 0)
            self.statusID=2000
            # print("Start:",self.statusID)

        
    def keeper(self) -> None:
        # print("ID:",self.screenShot)
        print("Status:",self.statusID)
        # print(self.__subWindows)
        if self.screenShot==1:
            if self.drawer()==1:
                self.__root.after(100, self.keeper)

        elif self.screenShot==2:# mian panel mode
            self.__root.after(100, self.keeper)

        # print(self.statusID==11)
        
        # print(self.keyBoardInterrupt.statusGet())
        if self.keyBoardInterrupt.statusGet()==2:
            # print("ssssssssssssssss",self.statusID)
            if self.statusID==2000:
                self.x=-10
                self.y=-10
                self.screenShot=2
                self.__root.attributes("-alpha", self.alpha)
                self.__subWindows.destroy()
                self.listener.terminate()
                self.listener=None
                self.keyBoardInterrupt.StartListener()
                self.statusID=1000


        
    def drawer(self)->int:
        print(self.__num)
        if self.listener!=None:
            if self.__loopTime>=90:
                self.listener.activeFlagSet(1)
                self.__loopTime=0
            self.__loopTime+=1
            
            if self.screenShot==1 and self.__num>0:
                temx,temy=self.listener.mouseGet()
                
                temx=(temx*self.width)/self.screen.width
                temy=(temy*self.height)/self.screen.height
                
                # print("call:",temx,temy)
                if self.x==-10 or self.y==-10:# prevent first click detection
                    self.x=-1
                    self.y=-1
                elif temx!=self.x or temy!=self.y:
                    print("click:",temx,temy)
                    self.x,self.y=temx,temy
                    self.__counter+=1
                    if self.__counter==1:
                        self.rectangleCreation(self.x,self.y,self.x,self.y,width=3)
                    else:
                        self.__counter=0
                
                if self.__counter==1:
                    temx,temy=self.listener.motionGet()
                    
                    temx=(temx*self.width)/self.screen.width
                    temy=(temy*self.height)/self.screen.height
                    
                    if (self.xRight==-1 and self.yRight==-1) \
                        or (temx!=self.xRight or temy!=self.yRight):

                        print("move:",temx,temy)
                        self.xRight,self.yRight=temx,temy
                        self.rectangleConfigure(self.x,self.y,self.xRight,self.yRight,width=3)
        
        if self.x==0 or self.y==0:
            self.listener.terminate()
            self.__root.destroy()
            return -1
        
        return 1
        
    def canvasPlace(self,positionX=0,positionY=0,highlightthickness=0,bgColor="black",target="root") -> None:

        if target=="sub":
            self.__canvas=tkinter.Canvas(self.__subWindows,highlightthickness=\
                highlightthickness,width=self.width, height=self.height,bg=bgColor)
        else:
            self.__canvas=tkinter.Canvas(self.__root,highlightthickness=\
                highlightthickness,width=self.width, height=self.height,bg=bgColor)
        self.__canvas.place(x=positionX,y=positionY)
        
    def rectangleCreation(self,positionX=0,positionY=0,rightX=0,rightY=0,outline="crimson",\
        width=0,dash=(1,1)) ->None:

        self.__rec.append(self.__canvas.create_rectangle(positionX,positionY,rightX,rightY,\
            outline=outline,width=width,dash=dash))
        print("coor:",self.__canvas.coords(self.__rec[-1]))
        
    def rectangleConfigure(self,positionX=0,positionY=0,rightX=0,rightY=0,outline="crimson",\
        width=0,index=-1,dash=(1,1)) ->None:

        self.__canvas.itemconfigure(self.__rec[index],outline=outline,width=width,\
            dash=dash)
        
        self.__canvas.coords(self.__rec[index],positionX,positionY,rightX,rightY)
        print("coorMoving:",self.__canvas.coords(self.__rec[-1]))
        
    # def closeWindow(self) -> None:
    #     self.__root.destroy()
        
    def getPositions(self)->list:
        
        return


if __name__=="__main__":
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
    wind=windowsUI(True,0.1,"black")
    # time.sleep(5)
    
    print("a")
