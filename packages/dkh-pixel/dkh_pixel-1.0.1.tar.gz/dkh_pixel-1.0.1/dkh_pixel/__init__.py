
import tkinter as tk
import time
   
class pixelImage:
    
    __data = []
    __x = 0
    __y = 0
    __n = 0
    
    def __init__(self, w, h):
        self.__width = w
        self.__height = h
    def addImg(self, dt):
        self.__data.append(dt)
    def nextSkin(self):
        self.__n += 1
        if self.__n >= len(self.__data): self.__n = 0
    def skin(self, nm):
        self.__n = nm
        if self.__n >= len(self.__data) or self.__n < 0:
            raise ValueError(str(nm) + ": неверный номер изображения.")
        
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self, inp):
        self.__x = inp
        
    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self, inp):
        self.__y = inp
        
    @property
    def width(self):
        return self.__width
    @width.setter
    def width(self, inp):
        self.__width = inp
        
    @property
    def height(self):
        return self.__height
    @height.setter
    def height(self, inp):
        self.__height = inp
        
    @property
    def data(self):
        return self.__data[self.__n]

__objects = []
__scene = {
    "window":   None,
    "image":    None,
    "width":    800,
    "height":   600,
    "step":     10,
    "color":    "white",
    "animTime": .1
}
__colors = ["white", "black", "red", "orange", "yello", "green", "lightblue", "blue", "violet", "gray"]

def animationTime(tm):
    global __scene
    __scene["animTime"] = tm

def createWindow(w, h, st, clr):
    global __scene, __colors
    __scene["window"] = tk.Tk()
    __scene["width"] = w
    __scene["height"] = h
    __scene["step"] = st
    __scene["color"] = clr
    __colors[0] = clr
    __scene["image"] = tk.Canvas(width=__scene["width"]*__scene["step"], height=__scene["height"]*__scene["step"], bg=__scene["color"])
    __scene["image"].pack()
    #__scene["window"].mainloop()
 
def createObject(w, h, dt):
    global __objects, __colors
    __objects.append(pixelImage(w, h))
    __objects[len(__objects)-1].addImg(dt)
    return __objects[len(__objects)-1]

def update():
    try:
        __scene["image"].delete("all")
        global  __objects
        for obj in __objects:
            for h in range(obj.height):
                for w in range(obj.width):
                    color = obj.data[h*obj.width + w]
                    if int(color) >= 0 and int(color) < 10: color = __colors[color]
                    # __scene["image"].create_rectangle(w+obj.x*__scene["step"], h+obj.y*__scene["step"], w+obj.x*__scene["step"]+__scene["step"], h+obj.y*__scene["step"]+__scene["step"], fill=color, width=0)
                    x = __scene["step"]*obj.x+w*__scene["step"]
                    y = __scene["step"]*obj.y+h*__scene["step"]
                    if x >= 0 and x <= __scene["width"]*__scene["step"] and y >= 0 and y <= __scene["height"]*__scene["step"]:
                        __scene["image"].create_rectangle(x, y, x+__scene["step"], y+__scene["step"], fill=color, width=0)
        __scene["image"].update()
        time.sleep(__scene["animTime"])
    except:
        exit()
