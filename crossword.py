# -*- coding: UTF-8 -*-

import datetime, PyPDF2, io, os, time, ast, sys, traceback
import urllib.request
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

convert = {'66': '1504', '83': '1491', '67': '1489', '77': '1510',
           '68': '1490', '88': '1505', '74': '1495', '65': '1513',
           '71': '1506', '70': '1499', '82': '1512', '69': '1511',
           '80': '1508', '86': '1492', '84': '1488', '78': '1502',
           '75': '1500', '89': '1496', '188': '1514', '85': '1493',
           '90': '1494', '72': '1497', '79': '1502', '73': '1504',
           '186': '1508', '190': '1510', '76': '1499'}
SIDE = 30
xAnchor = 70
yAnchor = 90
WIDTH = 420
HEIGHT = 550

root = tk.Tk()
root.title('תשבץ')
root.withdraw()
root.geometry(str(WIDTH)+'x'+str(HEIGHT)+'+20+20')
root.focus_force()

r, c = 0, 0
while r <= 0:
    s = "הכנס מספר שורות בבקשה"
    # s = ' '.join(s.split(" ")[::-1])
    r = simpledialog.askinteger("rows number", s, initialvalue=15, maxvalue=25)
    if r is None:
        exit()
while c <= 0:
    s = "הכנס מספר עמודות בבקשה"
    # s = ' '.join(s.split(" ")[::-1])
    c = simpledialog.askinteger("columns number", s, initialvalue=11, maxvalue=25)
    if c is None:
        exit()
if r > 13:
    SIDE = 400 / r
root.deiconify()

lr = yAnchor + SIDE * r
lc = xAnchor + SIDE * c
cross = [[[1, 0, 0] for j in range(c)] for i in range(r)]
saved = ''


def get_center(row, clmn):
    x0 = xAnchor - 2 + SIDE * clmn
    y0 = yAnchor + 2 + SIDE * row
    return x0 + SIDE / 2, y0 + SIDE / 2


def get_corner(row, clmn):
    x2 = xAnchor - 5 + SIDE * (clmn + 1)
    y2 = yAnchor + 5 + SIDE * row
    return x2, y2


def get_pos(row, clmn):
    x0 = xAnchor + SIDE * clmn
    y0 = yAnchor + SIDE * row
    x1 = x0 + SIDE
    y1 = y0 + SIDE
    return x0, y0, x1, y1


def get_point(row, clmn):
    x = xAnchor + clmn * SIDE
    y = yAnchor + row * SIDE
    return x, y


def get_num_pos(num):
    for i in range(r):
        for j in range(c):
            if cross[i][j][1] == int(num):
                return i, j
    return i, 0


canv = tk.Canvas(root, width=WIDTH, height=HEIGHT)


def reset_square(row, clmn):
    canv.create_rectangle(get_pos(row, clmn), fill="white")
    cross[row][clmn][0] = 1
    cross[row][clmn][2] = 0
    n = cross[row][clmn][1]
    if n > 0:
        canv.create_text(get_corner(row, clmn), text=str(n), font=("Arial", "7", "bold"))


def Clear(flag=False):
    s = "?הנתונים יימחקו! האם להמשיך"
    if flag or messagebox.askyesno("Override?", s):
        for i in range(r):
            for j in range(c):
                if cross[i][j][0] > 0:
                    reset_square(i, j)


def Reset():
    s = "?התשבץ יימחק! האם להמשיך"
    if messagebox.askyesno("Override?", s):
        RunOnce()


def RunOnce():
    canv.create_rectangle(xAnchor, yAnchor, lc, lr, fill="white")
    cross[0][0][0] = 1
    cross[0][0][2] = 0
    for i in range(1, r):
        x = yAnchor + SIDE * i
        canv.create_line(xAnchor, x, lc, x)
        for j in range(c):
            cross[i][j][0] = 1
            cross[i][j][2] = 0
    for j in range(1, c):
        x = xAnchor + SIDE * j
        canv.create_line(x, yAnchor, x, lr)
        cross[0][j][0] = 1
        cross[0][j][2] = 0
    if lavan.get():
        pass  # draw letters and numbers here


def Type(row, clmn, num="", t0=0):
    pos = str(row + 1) + "," + str(clmn + 1)
    lbl = tk.Label(root, bg='white', text=pos)
    lbl.place(x=200, y=515, width=40, height=15)

    def T(event, row=row, clmn=clmn, num=num, t0=t0):
        if cross[row][clmn][0] != 0:
            key = str(event.keycode)
            if key in convert:
                h = int(convert.get(key))
                reset_square(row, clmn)
                canv.create_text(get_center(row, clmn), text=chr(h), font=("Arial", "12"))
                cross[row][clmn][2] = h
                if direction.get() == 1:
                    if clmn > 0 and cross[row][clmn - 1][0] != 0:
                        Type(row, clmn - 1)
                if direction.get() == 2:
                    if row < r - 1 and cross[row + 1][clmn][0] != 0:
                        Type(row + 1, clmn)
            elif key >= '48' and key <= '57':
                if num == "":
                    t0 = time.perf_counter()
                    num = str(int(key) - 48)
                else:
                    if time.perf_counter() - t0 < 1:
                        num += str(int(key) - 48)
                    else:
                        num = str(int(key) - 48)
                        t0 = time.perf_counter()
                row, clmn = get_num_pos(num)
                if (row, clmn) != (r - 1, 0):
                    Type(row, clmn, num, t0)
            elif key == "9":
                row, clmn = get_num_pos(str(int(num) + 1))
            elif key == "32":
                direction.set(3 - direction.get())
                if (row, clmn) != (r - 1, c - 1):
                    Type(row, clmn, num)
            elif key == "46":
                if cross[row][clmn][2] > 0:
                    reset_square(row, clmn)
                    Type(row, clmn, num)
            elif key == "8":
                if (clmn == 0 or cross[row][clmn - 1][0] == 0) and direction.get() == 1 \
                        and cross[row][clmn][2] != 0:
                    reset_square(row, clmn)
                    Type(row, clmn)
                elif (row == r - 1 or cross[row + 1][clmn][0] == 0) and direction.get() == 2 \
                        and cross[row][clmn][2] != 0:
                    reset_square(row, clmn)
                    Type(row, clmn)
                else:
                    if direction.get() == 1 and clmn < c - 1:
                        if cross[row][clmn + 1][0] != 0:
                            reset_square(row, clmn + 1)
                            Type(row, clmn + 1)
                    if direction.get() == 2 and row > 0:
                        if cross[row - 1][clmn][0] != 0:
                            reset_square(row - 1, clmn)
                            Type(row - 1, clmn)

    canv.focus_set()
    canv.bind("<Key>", T)


def get_color(n):
    if n == 0:
        return "black"
    if n > 0:
        return "white"


def Click(event):
    if xAnchor <= event.x <= lc and yAnchor <= event.y <= lr:
        row = int((event.y - yAnchor) / SIDE)
        clmn = int((event.x - xAnchor) / SIDE)
        b = str(cross[row][clmn][0])
        n = str(cross[row][clmn][1])
        l = cross[row][clmn][2]
        pos = str(row + 1) + "," + str(clmn + 1) + "," + b + "," + n + "," + chr(l)
        lbl1 = tk.Label(root, bg='white', text=pos)
        lbl1.place(x=yAnchor, y=515, width=99, height=15)
        if blackState.get() < 3:
            flag = True
            cross[row][clmn][0] = 1 - cross[row][clmn][0]
            d = cross[row][clmn][0]
            cross[row][clmn][1] = 0
            cross[row][clmn][2] = 0
            canv.create_rectangle(get_pos(row, clmn), fill=get_color(d))
            if row == r - 1 - row and clmn == c - 1 - clmn:  # center cell
                flag = False
            if blackState.get() == 1 and flag:
                row = r - 1 - row
                clmn = c - 1 - clmn
                cross[row][clmn][0] = 1 - cross[row][clmn][0]
                d = cross[row][clmn][0]
                cross[row][clmn][1] = 0
                cross[row][clmn][2] = 0
                canv.create_rectangle(get_pos(row, clmn), fill=get_color(d))
        else:
            Type(row, clmn)


def Numbering(flag=False):
    if blackState.get() < 3 or flag == True:
        for i in range(r):
            for j in range(c):
                cross[i][j][1] = 0
        if cross[0][0][0] > 0 and cross[1][0][0] > 0:
            cross[0][0][1] = 1
        if cross[0][c - 1][0] > 0 and (cross[0][c - 2][0] > 0 or \
                                       cross[1][c - 1][0] > 0):
            cross[0][c - 1][1] = 1
        if cross[r - 1][c - 1][0] > 0 and cross[r - 1][c - 2][0] > 0:
            cross[r - 1][c - 1][1] = 1
        for j in range(c - 2):
            j += 1
            if cross[0][j][0] > 0:
                if cross[0][j + 1][0] == 0 and cross[0][j - 1][0] > 0 \
                        or cross[1][j][0] > 0:
                    cross[0][j][1] = 1
            if cross[r - 1][j][0] > 0 and cross[r - 1][j - 1][0] > 0 \
                    and cross[r - 1][j + 1][0] == 0:
                cross[r - 1][j][1] = 1
        for i in range(r - 2):
            i += 1
            if cross[i][0][0] > 0 and cross[i + 1][0][0] > 0 \
                    and cross[i - 1][0][0] == 0:
                cross[i][0][1] = 1
            if cross[i][c - 1][0] > 0:
                if cross[i + 1][c - 1][0] > 0 and cross[i - 1][c - 1][0] == 0 \
                        or cross[i][c - 2][0] > 0:
                    cross[i][c - 1][1] = 1
        for i in range(r - 2):
            i += 1
            for j in range(c - 2):
                j += 1
                if cross[i][j][0] > 0:
                    if (cross[i][j - 1][0] > 0 and cross[i][j + 1][0] == 0) \
                            or (cross[i + 1][j][0] > 0 and cross[i - 1][j][0] == 0):
                        cross[i][j][1] = 1
        n = 1
        for i in range(r):
            for j in range(c):
                j = c - 1 - j
                if cross[i][j][0] > 0:
                    canv.create_rectangle(get_pos(i, j), fill="white")
                if cross[i][j][1] > 0:
                    canv.create_text(get_corner(i, j), text=str(n), font=("Arial", "7", "bold"))
                    cross[i][j][1] = n
                    n += 1
    else:
        s = "'המספור אינו אפשרי במצב 'כתיבה"
        messagebox.showinfo("ארעה שגיאה", s)


def ptrn(pattern, flag=True):
    if flag:
        Reset()
    blacks = (pattern.split(';')[0])[1:-1].split(',')
    letters = ast.literal_eval(pattern.split(';')[1])
    for b in (blacks):
        b = int(b)
        j = int(b % c)
        i = int((b - j) / c)
        canv.create_rectangle(get_pos(i, j), fill="black")
        cross[i][j][0] = 0
        cross[i][j][1] = 0
    if not lavan.get():
        Numbering(True)
    for k in letters.keys():
        j = int(k % c)
        i = int((k - j) / c)
        l = letters[k]
        canv.create_text(get_center(i, j), text=chr(l), font=("Arial", "12"))
        cross[i][j][2] = l


def loadPtrn():
    global saved
    names = []
    patterns = {}
    fpath = os.path.abspath(os.curdir) + '\\patterns.txt'
    if os.path.exists(fpath):
        f = open('patterns.txt', 'r')
        for l in f:
            name = l.split(';')[0]
            names.append(name)
            patterns[name] = l.split(';', 1)[1]
        f.close()
    else:
        s = "אין תבניות שמורות"
        messagebox.showinfo("שגיאה", s)
    s = "הכנס את שם התבנית בבקשה"
    # s = ' '.join(s.split(" ")[::-1])
    name = simpledialog.askstring("Load Pattern", s + '\n' + str(names))
    if name in names:
        saved = name
        Clear(True)
        ptrn(patterns[name], False)
    else:
        s = "תבנית אינה קיימת"
        messagebox.showinfo("Error", s)


def savePtrn():
    global saved
    bp = []
    lp = {}
    for i in range(r):
        for j in range(c):
            if cross[i][j][0] == 0:
                bp.append(i * c + j)
            else:
                l = cross[i][j][2]
                if l != 0:
                    lp[i * c + j] = l
    s = "אנא הכנס את שם התבנית באנגלית"
    wd = datetime.date.today().weekday()
    d = (datetime.date.today() - datetime.timedelta(days=(wd + 3) % 7)).strftime("%d.%m.%y")
    fpath = os.path.abspath(os.curdir) + '\\patterns.txt'
    if not os.path.exists(fpath):
        fw = open('patterns.txt', 'w')
        name = simpledialog.askstring("Save Pattern", s, parent=root)
        if name is None:
            return
        if name == 'done':
            name = str(d)
        l = name + ';' + str(bp) + ';' + str(lp) + '\n'
        fw.write(l)
        fw.close()
    else:
        fr = open('patterns.txt', 'r+')
        lines = fr.readlines()
        names = []
        for l in lines:
            names.append(l.split(';')[0])
        s = s + '\n' + str(names)
        name = simpledialog.askstring("Save Pattern", s, parent=root, show=saved)
        if name is None:
            return
        if name == 'done':
            name = str(d)
        l = name + ';' + str(bp) + ';' + str(lp) + '\n'
        if len(lines) != 0:
            new_lines = ""
            if name not in names:
                fa = open('patterns.txt', 'a')
                fa.write(l)
                fa.close()
            else:
                for line in lines:
                    if name == line.split(';')[0]:
                        line = l
                    new_lines += line
                fw = open('patterns.txt', 'w')
                fw.write(new_lines)
                fw.close()
        else:
            fr.write(l)
            fr.close()
    saved = name


def Mark():
    for i in range(r):
        for j in range(c):
            cross[i][j][1] = 0
    if lavan.get():
        for i in range(c):
            j = c - i
            canv.create_text(xAnchor + SIDE * (i + 0.5), yAnchor - SIDE / 2 + 3, text=str(j),
                             font=("Arial", "8", "bold"))
        for i in range(r):
            if i < 10:
                canv.create_text(xAnchor + SIDE * (c + 0.5), yAnchor + SIDE * (i + 0.5), text=chr(1488 + i),
                                 font=("Arial", "8", "bold"))
            elif i == 14:
                canv.create_text(xAnchor + SIDE * (c + 0.5), yAnchor + SIDE * (i + 0.5), text=chr(1496) + chr(1493),
                                 font=("Arial", "8", "bold"))
            elif i == 15:
                canv.create_text(xAnchor + SIDE * (c + 0.5), yAnchor + SIDE * (i + 0.5), text=chr(1496) + chr(1494),
                                 font=("Arial", "8", "bold"))
            elif i >= 10:
                canv.create_text(xAnchor + SIDE * (c + 0.5), yAnchor + SIDE * (i + 0.5), text=chr(1497) + chr(1478 + i),
                                 font=("Arial", "8", "bold"))
    else:
        canv.create_rectangle(xAnchor, yAnchor - SIDE / 2 - 3, xAnchor + SIDE * c, yAnchor - 2, fill="#f0f0f0", width=0)
        canv.create_rectangle(xAnchor + SIDE * c + 2, yAnchor, xAnchor + SIDE * (c + 1), yAnchor + SIDE * r,
                              fill="#f0f0f0", width=0)


'''מספור'''
s = u"\u05de\u05e1\u05e4\u05d5\u05e8"
btn_num = tk.Button(root, text=s, command=Numbering)
btn_num.place(x=5, y=15)
'''איפוס'''
s = u"\u05d0\u05d9\u05e4\u05d5\u05e1"
btn_reset = tk.Button(root, text=s, command=Reset)
btn_reset.place(x=5, y=50)
'''ניקוי'''
s = u"\u05e0\u05d9\u05e7\u05d5\u05d9"
btn_clear = tk.Button(root, text=s, command=Clear)
btn_clear.place(x=5, y=85)
'''תבניות'''
s = u"\u05ea\u05d1\u05e0\u05d9\u05d5\u05ea"
btn_load = tk.Button(root, text=s, command=loadPtrn)
btn_load.place(x=5, y=120)
'''שמירה'''
s = u"\u05e9\u05de\u05d9\u05e8\u05d4"
btn_save = tk.Button(root, text=s, command=savePtrn)
btn_save.place(x=5, y=155)
'''לבן'''
s = u"\u05dc\u05d1\u05df"
lavan = tk.IntVar()
halavan = tk.Checkbutton(root, text=s, variable=lavan, command=Mark)
halavan.place(x=5, y=190)
direction = tk.IntVar()
s = u"\u05d0\u05e4\u05e7\u05d9"
direct1 = tk.Radiobutton(root, text=s, variable=direction, value=1)
direct1.place(x=250, y=5)
s = u"\u05d0\u05e0\u05db\u05d9"
direct2 = tk.Radiobutton(root, text=s, variable=direction, value=2)
direct2.place(x=250, y=27)
direction.set(1)
blackState = tk.IntVar()
s = u"\u05e1\u05d9\u05de\u05d8\u05e8\u05d9\u05ea\u0020\u05d4\u05e9\u05d7\u05e8\u05d4"
s = ' '.join(s.split(" ")[::-1])  # reversing order of words
black1 = tk.Radiobutton(root, text=s, variable=blackState, value=1)
black1.place(x=100, y=5)
s = u"\u05e8\u05d2\u05d9\u05dc\u05d4\u0020\u05d4\u05e9\u05d7\u05e8\u05d4"
s = ' '.join(s.split(" ")[::-1])
black2 = tk.Radiobutton(root, text=s, variable=blackState, value=2)
black2.place(x=100, y=25)
s = u"\u05db\u05ea\u05d9\u05d1\u05d4"
black3 = tk.Radiobutton(root, text=s, variable=blackState, value=3)
black3.place(x=100, y=46)
blackState.set(3)
canv.bind("<Button-1>", Click)
canv.pack(fill=tk.BOTH, expand=1)
RunOnce()
tk.mainloop()
