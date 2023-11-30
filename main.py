import math
import tkinter as tk


class MovingBall:
    def __init__(self, canvas, x1, y1, x2, y2, x3, y3, x, y, vx, vy):
        self.canvas = canvas
        self.x1 = x1 + 40
        self.y1 = y1 + 40
        self.x2 = x2
        self.y2 = y2 + 40
        self.x3 = x3 + 40
        self.y3 = y3
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = 5

        self.ball = self.canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r,
                                            fill="blue")

        self.canvas.create_line(self.x1, self.y1, self.x2, self.y2)
        self.canvas.create_line(self.x2, self.y2, self.x3, self.y3)
        self.canvas.create_line(self.x3, self.y3, self.x1, self.y1)

    def distance_to_segment(self, x, y, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:
            return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)
        t = ((x - x1) * dx + (y - y1) * dy) / (dx ** 2 + dy ** 2)
        if t < 0:
            return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)
        elif t > 1:
            return math.sqrt((x - x2) ** 2 + (y - y2) ** 2)
        else:
            xp = x1 + t * dx
            yp = y1 + t * dy
            return math.sqrt((x - xp) ** 2 + (y - yp) ** 2)

    def move_ball(self):
        d1 = self.distance_to_segment(self.x, self.y, self.x1, self.y1, self.x2, self.y2)
        d2 = self.distance_to_segment(self.x, self.y, self.x2, self.y2, self.x3, self.y3)
        d3 = self.distance_to_segment(self.x, self.y, self.x3, self.y3, self.x1, self.y1)
        if d1 < self.r or d2 < self.r or d3 < self.r:
            if d1 < self.r:
                nx, ny = self.y2 - self.y1, self.x1 - self.x2
            elif d2 < self.r:
                nx, ny = self.y3 - self.y2, self.x2 - self.x3
            else:
                nx, ny = self.y1 - self.y3, self.x3 - self.x1
            d = math.sqrt(nx ** 2 + ny ** 2)
            nx /= d
            ny /= d
            dot = self.vx * nx + self.vy * ny
            self.vx -= 2 * dot * nx
            self.vy -= 2 * dot * ny
        self.x += self.vx
        self.y += self.vy
        self.canvas.move(self.ball, self.vx, self.vy)
        self.canvas.update()
        self.canvas.after(30, self.move_ball)

    def clear_ball(self):
        self.canvas.delete('all')

    def set_speed(self):
        try:
            new_vx = float(self.entry_vx.get())
            new_vy = float(self.entry_vy.get())
            self.vx = new_vx
            self.vy = new_vy
        except ValueError:
            pass

    def set_initial_speed(self, initial_vx, initial_vy):
        self.entry_vx.insert(0, str(initial_vx))
        self.entry_vy.insert(0, str(initial_vy))

# Создание окна приложения
root = tk.Tk()
root.title("Движение шарика")

canvas = tk.Canvas(root, width=350, height=300, bd=0, highlightthickness=0)
canvas.pack()

# Создание шарика в треугольной области
x, y = 170, 150
vx, vy = 3, 0

ball = MovingBall(canvas, 40, 40, 260, 40, 150, 200, x, y, vx, vy)
ball.move_ball()

# Добавление элементов интерфейса для изменения скорости
frame = tk.Frame(root)
frame.pack()

label_vx = tk.Label(frame, text="Скорость по X:")
label_vx.grid(row=0, column=0)
entry_vx = tk.Entry(frame)
entry_vx.grid(row=0, column=1)

label_vy = tk.Label(frame, text="Скорость по Y:")
label_vy.grid(row=1, column=0)
entry_vy = tk.Entry(frame)
entry_vy.grid(row=1, column=1)

apply_button = tk.Button(frame, text="Применить", command=ball.set_speed)
apply_button.grid(row=2, columnspan=2)

ball.entry_vx = entry_vx
ball.entry_vy = entry_vy

# Установка начальных значений скорости в поля ввода
initial_vx = 3
initial_vy = 0
ball.set_initial_speed(initial_vx, initial_vy)

root.mainloop()
