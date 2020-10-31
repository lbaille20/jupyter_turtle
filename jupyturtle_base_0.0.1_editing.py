#!/usr/bin/env python
# coding: utf-8

# In[11]:


import matplotlib.pyplot as plt
import numpy as np
import time

TurtleScreen = None

turtle_heads = [
    (([0, -0.5, 1, -0.5, 0], [0, -3**0.5 / 2, 0, 3**0.5 / 2, 0]), (5, )),
    (([0, 0, 1, 0, 0], [0, -0.5, 0, 0.5, 0]), (5, ))
]
## _CFG from original _CFG turtle module
_CFG = {"width" : 0.5,               # Screen
        "height" : 0.75,
        "canvwidth" : 400,
        "canvheight": 300,
        "leftright": None,
        "topbottom": None,
        "mode": "standard",          # TurtleScreen
        "colormode": 1.0,
        "delay": 0.1,
        "undobuffersize": 1000,      # RawTurtle
        "shape": "classic",
        "pencolor" : "black",
        "fillcolor" : "black",
        "resizemode" : "noresize",
        "visible" : True,
        "language": "english",        # docstrings
        "exampleturtle": "turtle",
        "examplescreen": "screen",
        "title": "Python Turtle Graphics",
        "using_IDLE": False
       }

def rotate(X, Y, x0, y0, angle):
    Xn, Yn = [], []
    for x, y in zip(X, Y):
        x1 = x0 + np.cos(angle / 180 * np.pi) * (x - x0) - np.sin(angle / 180 * np.pi) * (y - y0) 
        y1 = y0 + np.sin(angle / 180 * np.pi) * (x - x0) + np.cos(angle / 180 * np.pi) * (y - y0)
        Xn.append(x1), Yn.append(y1)
    return Xn, Yn

def translate(X, Y, ux, uy):
    Xn, Yn = [], []
    for x, y in zip(X, Y):
        x1 = x + ux
        y1 = y + uy
        Xn.append(x1), Yn.append(y1)
    return Xn, Yn

def zoom(X, Y, f):
    return [f * x for x in X], [f * y for y in Y]

class TurtleSreen:
    def __init__(self):
        plt.ion()

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.xmin, self.xmax, self.ymin, self.ymax = -200, 200, -150, 150
        plt.title("Turtle playground",fontsize=10)
        plt.axis([self.xmin, self.xmax, self.ymin, self.ymax])

_Screen = None

class Turtle:
    def __init__(self):
        if _Screen == None:
            self.screen = TurtleSreen()
        else:
            self.screen = _Screen
        self._fig = self.screen.fig
        self._ax  = self.screen.ax
        self._pos = (0, 0)
        self._orient = 0
        self._head = turtle_heads[0][0]
        self._head_zoom = turtle_heads[0][1][0]
        self._tail = [([[0, 0], [0, 0]], ('black', '-', 1))]
        self._head_plot = plt.fill(zoom(turtle_heads[0][0][0], turtle_heads[0][0][1], turtle_heads[0][1][0])[0],
                               zoom(turtle_heads[0][0][0], turtle_heads[0][0][1], turtle_heads[0][1][0])[1],
                               color = 'black')[0]
        self._pendown = True
        self._visible = True
        self._pencolor = 'black'
        self._penstyle = '-'
        self._penwidth = 1
        self._fill = False
        self._fillcolor = 'black'
        self._fillpolygon = ''
    
    # methodes
    def forward(self, a):
        x0, y0 = self._pos
        x,  y  = a * np.cos(self._orient / 180 * np.pi) + x0, a * np.sin(self._orient / 180 * np.pi) + y0
        self._pos = x, y
        self.turtle_update(x0, y0, x, y)
    
    def goto(self, x, y):
        x0, y0 = self._pos
        self._pos = x, y
        self.turtle_update(x0, y0, x, y)

    def turtle_update(self, x0, y0, x, y):
        figure = self._fig
        self.tail_update(x0, y0, x, y)
        self.head_update()
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()
        time.sleep(_CFG['delay'])

    def tail_update(self, x0, y0, x, y):
        self._tail[-1][0][0].append(x)
        self._tail[-1][0][1].append(y)
        if self._pendown:
            plt.plot([x0, x], [y0, y],
                     linestyle=self._penstyle,
                     color=self._pencolor,
                     linewidth=self._penwidth)
    
    def head_update(self):
        x0, y0 = self._pos
        hx0, hy0 = self._head
        f = self._head_zoom
        hx, hy = zoom(hx0, hy0, f)
        Xn, Yn = translate(*rotate(hx, hy, 0, 0, self._orient), x0, y0)
        #t['head_plot'].set_xdata(Xn)
        #t['head_plot'].set_ydata(Yn)
        self._head_plot.set_color(self._pencolor)
        self._head_plot.set_visible(self._visible)
        self._head_plot.set_xy([[x, y] for x, y in zip(Xn, Yn)])

    def orient(self, alpha):
        self._orient = alpha
    
    def left(self, alpha):
        self._orient += alpha
        self.head_update()
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()
        time.sleep(_CFG['delay'])

    def show_turtle(self):
        self._visible = True
        self.head_update()

    def hide_turtle(self):
        self._visible = True
        self.head_update()
    
    def penup(self):
        self._pendown = False

    def pendown(self):
        self._pendown = True

    def pencolor(self, color):
        self._pencolor = color

    def fillcolor(self, color, pencolor=None):
        if pencolor == None:
            self._pencolor = color
        else:
            self._pencolor = pencolor
        self._fillcolor = color

    def begin_fill(self):
        self._fill = True
        x, y = self._pos
        self._tail.append(([[x, x], [y, y]], (self._pencolor, self._penstyle, self._penwidth)))

    def end_fill(self):
        self._fill = False
        Lx, Ly = self._tail[-1][0]
        x, y = self._pos
        plt.fill(Lx, Ly, color = self._fillcolor)
        self._tail.append(([[x, x], [y, y]], (self._pencolor, self._penstyle, self._penwidth)))

    def clearscreen(self):
        #https://stackoverflow.com/questions/8213522/when-to-use-cla-clf-or-close-for-clearing-a-plot-in-matplotlib
        #plt.clf() ## efface le plt.axis([])
        plt.cla()
        plt.title("Turtle playground",fontsize=10)
        plt.axis([self.screen.xmin, self.screen.xmax, self.screen.ymin, self.screen.ymax])
    
    def reset(self):
        self._pos = (0, 0)
        self._orient = 0
        self._head = turtle_heads[0][0]
        self._head_zoom = turtle_heads[0][1][0]
        self._tail = [([[0, 0], [0, 0]], ('black', '-', 1))]
        self._head_plot = plt.fill(zoom(turtle_heads[0][0][0], turtle_heads[0][0][1], turtle_heads[0][1][0])[0],
                               zoom(turtle_heads[0][0][0], turtle_heads[0][0][1], turtle_heads[0][1][0])[1],
                               color = 'black')[0]
        self._pendown = True
        self._visible = True
        self._pencolor = 'black'
        self._penstyle = '-'
        self._penwidth = 1
        self._fill = False
        self._fillcolor = 'black'
        self._fillpolygon = ''


# In[ ]:




