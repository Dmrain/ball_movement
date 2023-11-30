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

    def test_initial_speed(self):
        initial_vx = 3
        initial_vy = 0
        self.ball.set_initial_speed(initial_vx, initial_vy)
        self.assertEqual(self.entry_vx.get(), str(initial_vx))
        self.assertEqual(self.entry_vy.get(), str(initial_vy))

    def test_set_speed(self):
        new_vx = 5
        new_vy = -2
        self.entry_vx.insert(0, str(new_vx))
        self.entry_vy.insert(0, str(new_vy))
        self.ball.set_speed()
        self.assertEqual(self.ball.vx, new_vx)
        self.assertEqual(self.ball.vy, new_vy)

    def tearDown(self):
        self.root.destroy()


if __name__ == "__main__":
    unittest.main()
