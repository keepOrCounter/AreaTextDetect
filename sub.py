import pynput,time,tkinter,screeninfo
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
        if self.__status==-1:
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
    
    mouseGet(side): if side can be "left" or "right",return the x,y coordinate for last time mouse clicked
    motionGet(): return the x,y coordinate for last time mouse moved
    """
    def __init__(self) -> None:
        self.timeIntervalStart=0
        self.timeIntervalEnd=0
        
        self.activeFlag1=-1
        self.activeFlag2=-1
        
        self.DetectedMouseXPos=-1
        self.DetectedMouseYPos=-1

        self.DetectedRightMouseXPos=-1
        self.DetectedRightMouseYPos=-1
        
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

        if pressed and button.name=="right":
            self.DetectedRightMouseXPos=x
            self.DetectedRightMouseYPos=y
            # print(self.DetectedRightMouseXPos,self.DetectedRightMouseYPos)
            
            
        self.timeIntervalEnd=time.time()
        # print(self.timeIntervalEnd-self.timeIntervalStart)
        if self.timeIntervalEnd-self.timeIntervalStart>10.0:
            print("Times Up")
            if self.activeFlag1==-1:
                print("exit")
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
        
    def mouseGet(self, side) -> int:
        if side == "left":
            return self.DetectedMouseXPos,self.DetectedMouseYPos
        elif side == "right":
            return self.DetectedRightMouseXPos,self.DetectedRightMouseYPos
    
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
        screenShot: mode flag, 1 for screenShot mode, 2 for main window mode, 3...
        width,height: size of root window
        positionX,positionY: x,y for top left of window
        listener: mouse listener
    """
    def __init__(self,override=False,alpha=0.5,bgColor="black",screenShot=-1,\
        width=-1,height=-1,positionX=0,positionY=0,listener=None) -> None:
        # self.__timeList=[time.time(),0]
        self.listener=listener
        self.keyBoardInterrupt=eventKeyboard()
        self.screenShot=screenShot
        self.screen = screeninfo.get_monitors()[0]

        
        self.__rec=[]
        self.x=-1
        self.y=-1
        
        self.xRight=-1
        self.yRight=-1
        
        self.__loopTime=0
        self.__counter=0
        self.__status=-1
        
        self.__root = tkinter.Tk()
        
        self.width=width
        self.height=height
        if width==-1:
            self.width=self.__root.winfo_screenwidth()
        if height==-1:
            self.height=self.__root.winfo_screenheight()

        if self.screenShot==1:
            self.__num=6
            self.canvasPlace()
            
            self.__root.overrideredirect(override)
            self.__root.attributes("-alpha", alpha)
        elif self.screenShot==2:
            temx=200*(1280/self.screen.width)
            temy=70*(720/self.screen.height)
            print(temx,temy)
            self.but=tkinter.Button(self.__root,text="Record!")

            print((self.width-temx)/2,(self.height-temy)/2)
            self.but.place(x=(self.width-temx)/2,y=(self.height-temy)/2)
            
        self.__root.geometry("{0}x{1}+{2}+{3}"\
            .format(self.width, self.height,positionX,positionY))
        self.__root.configure(bg=bgColor)
        
        if self.listener!=None:
            self.listener.StartListener()
        self.keyBoardInterrupt.StartListener()
        self.keeper()
        

        self.__root.mainloop()
        
    def Start(self,status):
        if status==10 and self.__status==-1:# Issue 1
            mouseL=eventMouse()
            wind=windowsUI(True,0.5,"black",listener=mouseL,screenShot=1)
            self.__status=10
            return wind

        
    def keeper(self) -> None:

        if self.screenShot==1:
            if self.drawer()==1:
                self.__root.after(100, self.keeper)
                
        if self.__status==10:
            self.__root.attributes("-alpha", 0)
            self.__status=11
            
        if self.keyBoardInterrupt.statusGet()==2:
            if self.__status==11:
                self.__root.attributes("-alpha", 1)
                self.__status=-1
                self.keyBoardInterrupt.StartListener()
        
    def drawer(self)->int:
        if self.listener!=None:
            if self.__loopTime>=90:
                self.listener.activeFlagSet(1)
                self.__loopTime=0
            self.__loopTime+=1
            
            if self.screenShot==1 and self.__num>0:
                temx,temy=self.listener.mouseGet("left")
                
                temx=(temx*self.width)/self.screen.width
                temy=(temy*self.height)/self.screen.height
                
                # print("call:",temx,temy)
                if temx!=self.x or temy!=self.y:
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
            self.closeWindow()
            return -1
        
        return 1
        
    def canvasPlace(self,positionX=0,positionY=0,highlightthickness=0,bgColor="black") -> None:


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
        
    def closeWindow(self) -> None:
        self.__root.destroy()


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
