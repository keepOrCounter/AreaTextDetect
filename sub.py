import pynput,time
# import threading


class eventLis():
    def __init__(self) -> None:
        self.timeIntervalStart=0
        self.timeIntervalEnd=0
        self.detectFlag=-1
        self.DetectedMouseXPos=-1
        self.DetectedMouseYPos=-1
        self.keyValue=-1
        
        self.keyPressed=pynput.keyboard.Listener(on_press=self.pressed)
        
        # keyPressed.stop()
        self.mouseClicked=pynput.mouse.Listener(on_click=self.clicked)
        
        # mouseClicked.join()
        
    def clicked(self, x, y, button, pressed):
        
        if pressed and button.name=="left":
            self.DetectedMouseXPos=x
            self.DetectedMouseYPos=y
            print(self.DetectedMouseXPos,self.DetectedMouseYPos)
            # if x==0 or y ==0:
            #     self.detectFlag=False
                # self.terminate()
            # return True

    def pressed(self,key):
        self.keyValue=key
        if str(type(key))=="<enum 'Key'>":
            if key.name=="alt_l":
                print(key.name)
        else:
            print(key.char=="z")
        # return True

    def clickListener(self) -> None:
        self.keyPressed.start()
        self.mouseClicked.start()
        
    def terminate(self) -> None:
        self.keyPressed.stop()
        self.mouseClicked.stop()
        
    def mouseGet(self) -> int:
        return self.DetectedMouseXPos,self.DetectedMouseYPos

    def keyGet(self):
        return self.keyValue

if __name__=="__main__":
    startEvent=eventLis()
    startEvent.clickListener()
    x,y=startEvent.mouseGet()
    while x!=0 and y!=0:
        time.sleep(0.1)
        x,y=startEvent.mouseGet()
    startEvent.terminate()
    print("a")
