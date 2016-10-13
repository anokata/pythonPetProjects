import tkinter as Tkinter
import random
import math

class Bubble(object):
    def __init__(self, canvas, x, y, death_size=25, color='green',
            grow_speed=0.2):
        self.x = x
        self.y = y
        self.radius = 5
        self.death_size = death_size
        self.grow_speed = grow_speed
        self.canvas = canvas

        self.bubble = self.canvas.create_oval(fill='white', outline=color,
            width=2, *self._bubble_coords())

    def _bubble_coords(self):
        r = self.radius
        return (self.x - r, self.y - r, self.x + r, self.y + r)

    def go(self, to_remove):
        if self.radius >= self.death_size:
            to_remove.append(self)
            self.canvas.delete(self.bubble)

    def update_drawing(self, to_remove):
        growth = math.log(self.radius) * self.grow_speed
        self.radius += growth
        self.canvas.coords(self.bubble, *self._bubble_coords())
        self.go(to_remove)


class BubbleCanvas(Tkinter.Canvas):
    def __init__(self, master, *args, **kwargs):
        Tkinter.Canvas.__init__(self, master, *args, **kwargs)
        self.bubbles = []
        self.to_remove = []
        self.last_pos = (-1, -1)

        self.bind('<Motion>', self.on_motion)
        self.bind('<ButtonRelease-1>', self.on_left_up)
        self.bind('<ButtonRelease-3>', self.on_right_up)

    def draw(self):
        for bubble in self.bubbles:
            bubble.update_drawing(self.to_remove)
        while self.to_remove:
            self.bubbles.remove(self.to_remove.pop())

    def on_motion(self, event):
        x, y = event.x, event.y
        motion_score = abs(x - self.last_pos[0]) + abs(y - self.last_pos[1])
        self.last_pos = (x, y)
        if random.randint(0, motion_score) > 5:
            self.bubbles.append(Bubble(self, x, y))
            if random.randint(0, 100) == 0:
                self.bubbles.append(Bubble(self, x, y, color='purple',
                     death_size=100, grow_speed=0.5))

    def on_left_up(self, event):
        self.bubbles.append(Bubble(self, event.x, event.y, color='yellow',
            death_size=50, grow_speed=0.1))

    def on_right_up(self, event):
        self.bubbles.append(Bubble(self, event.x, event.y, color='blue',
            death_size=80, grow_speed=0.6))


class BubbleFrame(Tkinter.Frame):
    def __init__(self, title):
        Tkinter.Frame.__init__(self)
        self.master.title(title)

        self.canvas = BubbleCanvas(self, background='white')
        self.canvas.pack(expand=True, fill='both')
        self.after(20, self.on_timer)

    def on_timer(self):
        self.canvas.draw()
        self.after(20, self.on_timer)


root = Tkinter.Tk()
frame = BubbleFrame("Bubbles!")
frame.pack(expand=True, fill='both')
root.mainloop()
