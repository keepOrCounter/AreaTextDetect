from tkinter import *
#Create an instance of tkinter frame
win = Tk()
#Set the geometry of Tkinter frame
win.geometry("700x250")

# Initialize a Canvas Object
canvas = Canvas(win, width= 500, height= 300)

# Draw an oval inside canvas object
c= canvas.create_oval(100,10,410,200, outline= "red", fill= "#adf123")
canvas.pack(expand= True, fill=BOTH)

#Get and Print the coordinates of the Oval
print("物体坐标为：", type(canvas.coords(c)))
win.mainloop()
