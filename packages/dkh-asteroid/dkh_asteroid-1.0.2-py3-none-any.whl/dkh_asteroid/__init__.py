# подключение библиотек
from tkinter import *
from time import sleep
from random import randint

# настройка окна
window = Tk()
window.title("Астероид 1.0")
image = Canvas(window, width=600, height=600, bg="#222235")
image.pack()

game = True
menu = True

moveLeft = False
moveRight = False

x = 300  # rocket
y = 500
speed =7

aX = [100, 300, 500]  # asteroid
aY = [100, -100, -300]
aSpeed = [15, 12, 9]

score = 0 # очки
try:
    record = int(open("data.txt", "r").readline())
except FileNotFoundError:
    record = 0

mX = 0  # mouse
mY = 0
mP = False # mousePress

stars = {
    "x": [randint(0,600) for i in range(500)],
    "y": [randint(0,600) for i in range(500)],
    "s": [randint(1,4) for i in range(500)]
}

# анализ клавиатуры
def keyDown(event):
    global moveLeft, moveRight, menu
    key = event.keycode
    print(key)
    if key == 113: moveLeft = True
    if key == 114: moveRight = True
    if key == 9: menu = True
def keyUp(event):
    global moveLeft, moveRight
    key = event.keycode
    if key == 113: moveLeft = False
    if key == 114: moveRight = False
def mouseMove(event):
    global mX, mY
    mX = event.x
    mY = event.y
def click(event):
    global mP
    mP = True

# связь клавиатуры с функциями
window.bind("<KeyPress>", keyDown)
window.bind("<KeyRelease>", keyUp)
window.bind("<Motion>", mouseMove)
window.bind("<Button-1>",   click)

# цикл анимации
while game:
    if not menu:
        # анализ действий
        if moveLeft: x -= speed
        if moveRight: x += speed
        if x < 50: x = 50
        if x > 550: x = 550
        for i in range(len(aX)):
            aY[i] += aSpeed[i] # двигает астероид вниз
            if aY[i] > 650: # перебрасывает астероид вверх
                aY[i] = -50
                aX[i] = randint(50, 550)
                score += 1
        # касание астероида и корабля
        for i in range(len(aX)):
            if aX[i]+50 > x-50 and aX[i]-50 < x+50 and aY[i]+50 > y-50 and aY[i]-50 < y+50:
                menu = True
                if score > record:
                    record = score
                    f = open("data.txt", "w")
                    f.write(str(record))
                    f.close()
                score = 0
                aY = -100
    # звёздочки
    for i in range(len(stars["x"])):
        stars["y"][i] += stars["s"][i]
        if stars["y"][i] > 600:
            stars["y"][i] = 0
            stars["x"][i] = randint(0, 600)
    # отрисовка
    image.delete("all")
    # звёздочки
    for i in range(len(stars["x"])):
        image.create_oval(stars["x"][i]-stars["s"][i],stars["y"][i]-stars["s"][i], stars["x"][i]+stars["s"][i],stars["y"][i]+stars["s"][i], fill="#ffffff", width=0)
    if not menu:
        # корабль
        color = "#f"+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+"00"
        image.create_polygon(x-30,y+randint(30,50), x-10,y+randint(30,50), x+10,y+150, x-50,y+150, fill=color)
        image.create_polygon(x+30,y+randint(30,50), x+10,y+randint(30,50), x-10,y+150, x+50,y+150, fill=color)
        image.create_polygon(x,y-50, x-50,y+50, x-10,y+40, x,y+50, x+10,y+40, x+50,y+50, fill='#aaaaaa')
        image.create_polygon(x,y-40, x-10,y-20, x,y-10, x+10,y-20, fill='#8888ff')
        image.create_polygon(x-20,y+20, x-10,y+30, x-10,y+50, x-30,y+50, x-30,y+30, fill='#888888')
        image.create_polygon(x+20,y+20, x+10,y+30, x+10,y+50, x+30,y+50, x+30,y+30, fill='#888888')
        image.create_polygon(x-10,y-10, x,y, x+10,y-10, x,y+40, fill='#999999')
        # астероид
        for i in range(len(aX)):
            image.create_oval(aX[i]-50, aY[i]-50, aX[i]+50, aY[i]+50, fill="#a83a00", width=0)
            image.create_oval(aX[i]-40, aY[i]-40, aX[i]+20, aY[i]-5, fill="#d17900", width=0)
        # очки
        image.create_text(90,570, text="ОЧКИ: "+str(score), fill="#ffffff", font="Verdana 20")
    else:
        if mX > 125 and mX < 475 and mY > 300 and mY < 400:
            image.create_rectangle(125,300, 475,400, width=5, outline="white", fill="white")
            image.create_text(300,350, text="ИГРАТЬ", justify=CENTER, fill="#222235", font="Verdana 40")
            if mP: menu = False
        else:
            image.create_rectangle(125,300, 475,400, width=5, outline="white")
            image.create_text(300,350, text="ИГРАТЬ", justify=CENTER, fill="white", font="Verdana 40")
            
        if mX > 125 and mX < 475 and mY > 450 and mY < 550:
            image.create_rectangle(125,450, 475,550, width=5, outline="white", fill="white")
            image.create_text(300,500, text="ВЫХОД", justify=CENTER, fill="#222235", font="Verdana 40")
            if mP: game = False
        else:
            image.create_rectangle(125,450, 475,550, width=5, outline="white")
            image.create_text(300,500, text="ВЫХОД", justify=CENTER, fill="white", font="Verdana 40")
            
        image.create_text(300,220, text="РЕКОРД: "+str(record), justify=CENTER, fill="white", font="Verdana 25")    
        image.create_text(300,130, text="АСТЕРОИД 1.0", justify=CENTER, fill="white", font="Verdana 50")
        mP = False
    image.update()
    sleep(0.01)
window.destroy()
