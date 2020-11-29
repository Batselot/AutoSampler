# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 23:45:58 2019

@author: SONY
"""
from tkinter import Tk, StringVar, Label,Entry
import tkinter
import numpy as np
import serial
import time
import threading 

top = tkinter.Tk()


canvas = tkinter.Canvas(top, bg="white", height=1000, width=1000)
liste=[]
liste2=[]
liste3=[]
liste4=[]
liste5=[]
liste6=[]
liste7=[]
yedekoutput=[]
ymindirection_list=[]
xmindirection_list=[]
stringlist=[]
X=[]
verynewlist_x=[]
verynewlist_y=[]
Compare_x=0
Compare_y=0
combined_list=[]
numbers_before_strlist=[]

a=0
for i in range(4):
    for ii in range(12):
        y=canvas.create_oval(10 + ii * 50, 10 + i * 100, 40 + ii * 50, 40 + i * 100, fill="blue", activefill="red")
        liste3.append(canvas.coords(y))
        if ii != 11:
            x=canvas.create_oval(25 + ii * 50, 60 + i * 100, 55 + ii * 50, 90 + i * 100, fill="blue", activefill="red")
            liste4.append(canvas.coords(x))

#
#def karşılaştırma():
#    numbers=[x for x in range(1,93,2)]
#    numbers=np.array(numbers)
#    A=np.array(liste3)
#    B=np.transpose(numbers)
#    #print(np.size(B))
#    print(B)
#    A[:,0]=(A[:,0]+A[:,2])/2
#    A[:,1]=(A[:,1]+A[:,3])/2  
#    A=np.delete(A,[2,3],1)
#    print(np.size(A))
#   # print(numbers)
#    #print(A)
#    
##    print(A)
##    B=np.array(liste4)
    
        
#    liste3[0]=liste3[0]+liste3[2]/2
    
def groups(glist, numPerGroup=2):
    result = []

    i = 0
    cur = []
    for item in glist:
        if not i < numPerGroup:
            result.append(cur)
            cur = []
            i = 0

        cur.append(item)
        i += 1

    if cur:
        result.append(cur)

    return result


def average(points):
    aver = [0, 0]

    for point in points:
        aver[0] += point[0]
        aver[1] += point[1]

    return aver[0] / len(points), aver[1] / len(points)

class RectTracker:

    def __init__(self, canvas):
        self.canvas = canvas
        self.item = None

    def draw(self, start, end, **opts): #seçim için oluşan rectanglei oluşuturuyor..
        """Draw the rectangle"""
        return self.canvas.create_rectangle(*(list(start) + list(end)), **opts)#this one makes us draw the rectangle

    def autodraw(self, **opts): #classın içindeki çizim fonksiyonu aşağıda autodraw fonksiyonuyla bunun çağrıyor.
        """Setup automatic drawing; supports command option"""
        self.start = None
        self.canvas.bind("<Button-1>", self.__update, '+')
        self.canvas.bind("<B1-Motion>", self.__update, '+')
        self.canvas.bind("<ButtonRelease-1>", self.__stop, '+')
#        self.canvas.bind("<Button-1>", mm.select)
#        self.canvas.bind("<Button-1>",find_enclosed(x1,y1,x2,y2))
        self._command = opts.pop('command', lambda *args: None)
        self.rectopts = opts

    def __update(self, event):
        if not self.start:
            self.start = [event.x, event.y]
            return

        if self.item is not None:
            self.canvas.delete(self.item)
        self.item = self.draw(self.start, (event.x, event.y), **self.rectopts)
        self._command(self.start, (event.x, event.y))

    def __stop(self, event):
        self.start = None
        self.canvas.delete(self.item)
        self.item = None

    def hit_test(self, start, end, tags=None, ignoretags=None, ignore=[]):
        """
        Check to see if there are items between the start and end
        """
        ignore = set(ignore)
        ignore.update([self.item])

        # first filter all of the items in the canvas
        if isinstance(tags, str):
            tags = [tags]

        if tags:
            tocheck = []
            for tag in tags:
                tocheck.extend(self.canvas.find_withtag(tag))
        else:
            tocheck = self.canvas.find_all()
        tocheck = [x for x in tocheck if x != self.item]
        if ignoretags:
            if not hasattr(ignoretags, '__iter__'):
                ignoretags = [ignoretags]
            tocheck = [x for x in tocheck if x not in self.canvas.find_withtag(it) for it in ignoretags]

        self.items = tocheck

        # then figure out the box
        xlow = min(start[0], end[0])
        xhigh = max(start[0], end[0])

        ylow = min(start[1], end[1])
        yhigh = max(start[1], end[1])

        items = []
        for item in tocheck:
            if item not in ignore:
                x, y = average(groups(self.canvas.coords(item)))
                if (xlow < x < xhigh) and (ylow < y < yhigh):
                    items.append(item)

        return items

def onDrag(start, end):#ondrag fonksiyonuyla kareyi oluşturduğunu görebiliriz.
    canvas.itemconfig('kirmizi',tags=('blue'))
    global x, y
    items = rect.hit_test(start, end) #recttrackeri kullanarak objelere deyip deymediğini test ediyor eğer objenin üstünden geçiyorsa boyuyor.
    for x in rect.items:
        if x not in items:
            canvas.itemconfig(x, fill='blue')
        else:
            canvas.itemconfig(x, fill='red')
            canvas.itemconfig(x,tags=('kirmizi'))
    liste.append(canvas.find_withtag('kirmizi'))
    liste7.append(canvas.coords(canvas.find_withtag('kirmizi')))
    
      #  liste.append(canv.find_withtag('kirmizi'))
    #soneleman=liste[-1]
rect=RectTracker(canvas)
rect.autodraw(fill="", width=2, command=onDrag)



def coordinates():
    output=[]
    output.clear()
    liste5.clear()
    tagliler=canvas.find_withtag('kirmizi')
    liste5.extend(tagliler)
    liste6.clear()
    for i in liste5:
        liste6.extend(canvas.coords(i))
    for i in range(0, len(liste6), 4):
        output.append((liste6[i] + liste6[i+2])/2) # center x
        output.append((liste6[i+1] + liste6[i+3])/2) # center y
    output=[int(i) for i in output]
    print(output)
    
def control():
    if len(liste)!=0: 
        X=liste[-1]
        print(X)
        size=len(liste[-1])
        omega=np.full((1,size),1)
        omega2=np.subtract(liste[-1],omega)
#        print(omega2) #birara fazla çalışıyordu düzgün çalıştığından bu kısma gerek yok 2den başlatıyordu nedense şimdi 1.maddeden başladığını görebiliyoruz.
    elif len(liste)==0:
        print("Lütfen geçerli bir hücre seçiniz")

def zamanyazdır():
    say_my_name=name.get()
    print(say_my_name)
    

def getstring():
    numbers_before_strlist.clear()
    combined_list.clear()
    stringlist.clear()
    output=[]
    outputx=[0,0,0,0]
    outputy=[0,0]
    sayi_x=0
    sayi_y=0
    verynewlist_x.clear()
    verynewlist_y.clear()
    outputx.clear()
    outputy.clear()
    output.clear()
    liste5.clear()
    tagliler=canvas.find_withtag('kirmizi')
    liste5.extend(tagliler)
    liste6.clear()
    for i in liste5:
        liste6.extend(canvas.coords(i))
    for i in range(0, len(liste6), 4):
        sayi_x=((liste6[i] + liste6[i+2])/2) # center x
        sayi_y=((liste6[i+1] + liste6[i+3])/2)#center y
        outputx.append(sayi_x)
        outputy.append(sayi_y)
  #  print(outputx)
    #print(outputy)
    for i in range(len(outputx)-1):
        if outputx[i]!=outputx[i+1]:
            newvalue_x=outputx[i+1]-outputx[i]
            verynewlist_x.append(newvalue_x)
    verynewlist_x.insert(0,outputx[0])
 #   print(verynewlist_x)#gönderilmekistenenxvaluelarıteklistede
    for i in range(len(outputy)-1):
        if outputy[i]!=outputy[i+1]:
            newvalue_y=outputy[i+1]-outputy[i]
            verynewlist_y.append(newvalue_y)
    verynewlist_y.insert(0,outputy[0])
#    print(verynewlist_y)#gönderilmekistenenyvaluelarıteklistede
    while (len(verynewlist_x)!=len(verynewlist_y)):
        if (verynewlist_x<verynewlist_y):
            verynewlist_x.append(0.0)
        elif(verynewlist_y<verynewlist_x):
            verynewlist_y.append(0.0)
        #print(verynewlist_x,verynewlist_y)
    
    for i in range(len(verynewlist_x)):
        combined_list.clear()
        combined_list.append(verynewlist_x[i])
        combined_list.append(verynewlist_y[i])
        x=name.get()
        x=float(x)
        biglist=[1,1,1,0,0,0]#1.komut verme,2.y motor(1'se normal yön),3.x motor,4.x step,5.y step,6. zaman
        biglist[5]=x*1000
        for i in range(0,len(combined_list),2):
            biglist[3]=combined_list[i]
            biglist[4]=combined_list[i+1]
            numbers_before_strlist.append(biglist)
            strbiglist=[str(i) for i in biglist]
            s=",".join(strbiglist)
            s="<"+s+">"
            stringlist.append(s)
        #print(stringlist[0])
        gönderme()      

def gönderme():
    tekrar=len(stringlist)
    yazilanlar=[]
#    arduino=serial.Serial("COM4",9600)
    arduino = serial.Serial(port='COM3',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)
    time.sleep(2)
    
    for ii in range(tekrar):
        arduino.write((str.encode(stringlist[ii])))
        arduino.flush()
        for i in range(6):
            x=arduino.readline()
            if x!='':
                yazilanlar.append(x)
            time.sleep(0.1)
        print(yazilanlar)
        # print(y)
        # final
#def gönderme():
#    tekrar=len(stringlist)
#    yazilanlar=[]
##    arduino=serial.Serial("COM4",9600)
#    arduino = serial.Serial(port='COM3',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)
#    time.sleep(2)
#    
#    for ii in range(tekrar):
#        arduino.write((str.encode(stringlist[ii])))
#        arduino.flush()
#        for i in range(6):
#            x=arduino.readline()
#            if x!='':
#                yazilanlar.append(x)
#            time.sleep(0.1)
#        print(yazilanlar)
#        # print(y)
#        # final
        
     

def close():
    arduino=serial.Serial("COM4",9600)
    time.sleep(3)
    hiz=0
    yon=1
    arduino.write(str.encode(str(hiz)+","+str(yon)))
    time.sleep(2)
    arduino.close()
    arduino=serial.Serial("COM4",9600)
    time.sleep(3)
    speed=0
    ev=2
    arduino.write(str.encode(str(hiz)+","+str(ev)))
    time.sleep(2)
    arduino.close()

b=tkinter.Button(canvas,text="Click me",command=threading.Thread(target=getstring).start())
b1=tkinter.Button(canvas,text="stop",command=coordinates)
b2=tkinter.Button(canvas,text="home",command=gönderme)
b.place(x=900,y=150)
b1.place(x=900,y=200)
b2.place(x=800,y=200)
name=StringVar()
entry_box= Entry(canvas,textvariable=name,width=10,bg="white").place(x=825,y=150)
 
        
        
canvas.pack()
top.mainloop()



if __name__ == '__main__':
    try:
        from tkinter import *
    except ImportError:
        from Tkinter import *

#if __name__ == '__main__':
#    try:
#        from tkinter import *
#    except ImportError:
#        from Tkinter import *

