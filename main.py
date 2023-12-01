import math
import tkinter as tk
from tkinter import messagebox


class MovingBall:
    def __init__(self, canvas, x1, y1, x2, y2, x3, y3, x, y, vx, vy):
        """
            Инициализация шарика и треугольника на холсте.
            Параметры:
            canvas: Объект Canvas для отображения элементов.
            x1, y1, x2, y2, x3, y3 (int): Координаты вершин треугольника.
            x, y (int): Координаты центра шарика.
            vx, vy (float): Компоненты скорости шарика по x и y.
        """
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

        self.ball = self.canvas.create_oval(self.x - self.r, self.y - self.r,
                                            self.x + self.r, self.y + self.r, fill="blue")

        self.canvas.create_line(self.x1, self.y1, self.x2, self.y2)
        self.canvas.create_line(self.x2, self.y2, self.x3, self.y3)
        self.canvas.create_line(self.x3, self.y3, self.x1, self.y1)
        self.is_moving = False

    def distance_to_segment(self, x, y, x1, y1, x2, y2):
        """
            Данная функция ассчитывает расстояние от точки (x, y)
            до отрезка с координатами (x1, y1) и (x2, y2).
            Параметры:
            x, y (int): Координаты точки.
            x1, y1, x2, y2 (int): Координаты концов отрезка.
        """
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
        """
            Функция отвечает за движение шарика и взаимодействие
            с треугольником при столкновении.
        """
        if self.is_moving:  # Проверка на состояние движения
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
        """
            Функция удаляет все объекты Canvas.
        """
        self.canvas.delete('all')

    def set_speed(self):
        """
            Функция задает скорость шарика на основе данных из полей ввода.
        """
        try:
            new_vx = float(self.entry_vx.get())
            new_vy = float(self.entry_vy.get())
            self.vx = new_vx
            self.vy = new_vy
        except ValueError:
            pass

    def start_movement(self):
        """
            Функция начинает движение шарика.
        """
        if self.entry_vx.get() and self.entry_vy.get():  # Проверяем, заполнены ли поля скорости
            self.vx = float(self.entry_vx.get())
            self.vy = float(self.entry_vy.get())
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, заполните все поля.")
            return

        self.is_moving = True
        self.move_ball()
    def stop_movement(self):
        """
            Останавливает движение шарика.
        """
        self.is_moving = False
        self.vx, self.vy = 0, 0
        self.entry_vx.delete(0, tk.END)
        self.entry_vy.delete(0, tk.END)
        self.set_initial_speed(3, 0)

    def set_initial_speed(self, initial_vx, initial_vy):
        """
            Задает начальную скорость в поля ввода.
            Параметры:
            initial_vx, initial_vy (int): Начальные значения скорости по x и y.
        """
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

# Добавление кнопок "Старт" и "Стоп" и остального интерфейса
apply_button = tk.Button(root, text="Cтарт", command=ball.start_movement)
apply_button.pack()

stop_button = tk.Button(root, text="Стоп", command=ball.stop_movement)
stop_button.pack()

label_vx = tk.Label(root, text="Скорость по X:")
label_vx.pack()
entry_vx = tk.Entry(root)
entry_vx.pack()

label_vy = tk.Label(root, text="Скорость по Y:")
label_vy.pack()
entry_vy = tk.Entry(root)
entry_vy.pack()


ball.entry_vx = entry_vx
ball.entry_vy = entry_vy

# Установка начальных значений скорости в поля ввода
initial_vx = 3
initial_vy = 0
ball.set_initial_speed(initial_vx, initial_vy)

root.mainloop()
