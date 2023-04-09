import pynput,time,tkinter
# import threading


class eventKeyboard():
    def __init__(self) -> None:
        self.keyValue=-1
        self.timeIntervalStart=0
        self.timeIntervalEnd=0
        self.activeFlag=-1
        self.keyPressed=pynput.keyboard.Listener(on_press=self.pressed)
        
    def pressed(self,key):
        # print("b")
        
        if str(type(key))=="<enum 'Key'>":
            if key.name=="alt_l":
                self.keyValue=key.name
                print(key.name)
        else:
            self.keyValue=key.char
            print(key.char=="z")
        
        self.timeIntervalEnd=time.time()
        
        if self.timeIntervalEnd-self.timeIntervalStart>10.0:
            print("Times Up")
            if self.activeFlag==-1:
                print("Exit")
                return False
            self.timeIntervalStart=time.time()
            self.activeFlag=-1
        
    def StartListener(self) -> None:
        self.keyPressed.start()
        self.timeIntervalStart=time.time()
            
    def terminate(self) -> None:
        self.keyPressed.stop()
        
    def keyGet(self) -> str:
        return self.keyValue
    
    def activeFlagSet(self,newFlag) -> None:
        self.activeFlag=newFlag


class eventMouse():
    def __init__(self) -> None:
        self.timeIntervalStart=0
        self.timeIntervalEnd=0
        self.activeFlag=-1
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
            if self.activeFlag==-1:
                print("exit")
                return False
            self.timeIntervalStartMotion=time.time()
            self.activeFlag=-1

        
    def clicked(self, x, y, button, pressed):
        
        if pressed and button.name=="left":
            self.DetectedMouseXPos=x
            self.DetectedMouseYPos=y
            print(self.DetectedMouseXPos,self.DetectedMouseYPos)
            
            
        self.timeIntervalEnd=time.time()
        # print(self.timeIntervalEnd-self.timeIntervalStart)
        if self.timeIntervalEnd-self.timeIntervalStart>10.0:
            print("Times Up")
            if self.activeFlag==-1:
                print("exit")
                return False
            self.timeIntervalStart=time.time()
            self.activeFlag=-1
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
        self.activeFlag=newFlag
        
class windowsUI():
    def __init__(self,override=False,alpha=0.1,bgColor="black",screenShot=-1,\
        width=-1,height=-1,positionX=0,positionY=0,listener=None) -> None:
        # self.__timeList=[time.time(),0]
        self.__counter=0
        if screenShot==0:
            self.__num=6
        
        self.__root = tkinter.Tk()
        self.__root.overrideredirect(override)
        self.__root.attributes("-alpha", alpha)
        if width==-1:
            width=self.__root.winfo_screenwidth()
        if height==-1:
            height=self.__root.winfo_screenheight()
            
        self.__root.geometry("{0}x{1}+{2}+{3}"\
            .format(width, height,positionX,positionY))
        self.__root.configure(bg=bgColor)
        
        self.keeper(listener,screenShot)
        self.__root.mainloop()
        
    def keeper(self,listener,screenShot) -> None:
        # self.__counter+=1
        # self.__timeList[self.__counter%2]=time.time()
        # print(self.__timeList[self.__counter%2]-self.__timeList[(self.__counter-1)%2])
        
        # print("101010")
        # if self.__counter>10:
        #     self.closeWindow()
        # else:
        if listener!=None:
            temx,temy=listener.mouseGet()
            if (self.x==-1 and self.y==-1) or (temx!=self.x or temy!=self.y):
                self.x,self.y=temx,temy
                self.__counter+=1

        self.__root.after(1000, self.keeper)
        
    def canvasPlace(self,width=-1,height=-1,positionX=0,positionY=0) -> None:
        if width==-1:
            width=self.__root.winfo_screenwidth()
        if height==-1:
            height=self.__root.winfo_screenheight()
        self.__canvas=tkinter.Canvas(self.__root,highlightthickness=0,width=width, height=height)
        self.__canvas.place(positionX,positionY)
        
    def rectangleCreation(self,positionX=0,positionY=0,rightX=0,rightY=0,outline="red",\
        width=0) ->None:
        self.__rec=[]
        self.__rec.append(self.__canvas.create_rectangle(positionX,positionY,rightX,rightY,\
            outline='red',width=width))
        
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
