import unittest
from tkinter import Tk, Canvas, Frame, Entry, Button
from main import MovingBall


class TestMovingBall(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=350, height=300, bd=0, highlightthickness=0)
        self.frame = Frame(self.root)
        self.entry_vx = Entry(self.frame)
        self.entry_vy = Entry(self.frame)
        self.ball = MovingBall(self.canvas, 40, 40, 260, 40, 150, 200, 170, 150, 3, 0)
        self.ball.entry_vx = self.entry_vx
        self.ball.entry_vy = self.entry_vy

    def test_ball_existence(self):
        # Проверка существования шарика на canvas
        self.assertIsNotNone(self.ball.ball)

    def test_ball_color(self):
        # Проверка цвета шарика
        ball_color = self.canvas.itemcget(self.ball.ball, "fill")
        self.assertEqual(ball_color, "blue")

    def tearDown(self):
        self.root.destroy()


if __name__ == "__main__":
    unittest.main()