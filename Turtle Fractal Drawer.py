from turtle import Turtle
from tkinter import simpledialog
from time import sleep
import math
from collections.abc import Callable
from itertools import cycle

def reset(t):
    t.reset()
    t.screen.bgcolor("black")
    t.hideturtle()
    t.speed(0)

def invert_commands(commands: str) -> str:
    swap = {"R": "L", "L": "R", "F": "F"}
    return "".join(swap[c] for c in commands)

def draw_curve_has_f(commands: str, step_length: float, rainbow_generator: cycle) -> None:
    for c in commands:
        if c == "R":
            t.right(90)
        elif c == "L":
            t.left(90)
        elif c =="F":
            t.pencolor(next(rainbow_generator))
            t.forward(step_length)

def draw_curve_no_f(commands: str, step_length: float, rainbow_generator: cycle) -> None:
    t.pencolor(next(rainbow_generator))
    t.forward(step_length)
    for c in commands:
        if c == "R":
            t.right(90)
        elif c == "L":
            t.left(90)
        t.pencolor(next(rainbow_generator))
        t.forward(step_length)
            

def koch_curve(level: int, length: float, rainbow_generator: cycle) -> None:
    
    if level == 1:
        t.pencolor(next(rainbow_generator))
        t.forward(length)
    else:
        koch_curve(level-1, length/3, rainbow_generator)
        t.left(60)
        koch_curve(level-1, length/3, rainbow_generator)
        t.right(120)
        koch_curve(level-1, length/3, rainbow_generator)
        t.left(60)
        koch_curve(level-1, length/3, rainbow_generator)

def koch_snowflake(level: int, length: float, rainbow_generator: cycle) -> None:
    t.teleport(-length/2, length/3)
    for _ in range(3):
        koch_curve(level, length, rainbow_generator)
        t.right(120)

def hilbert(level: int) -> str:
    if level == 0:
        return ""
    else:
        return "L" + invert_commands(hilbert(level-1)) + "FR" + hilbert(level-1) + "F" + hilbert(level-1) + "RF" + invert_commands(hilbert(level-1)) + "L"

def hilbert_curve(level: int, curve_size: float, rainbow_generator: cycle) -> None:
    t.teleport(-curve_size/2, -curve_size/2)
    step_length = curve_size/((2**level)-1)
    draw_curve_has_f(hilbert(level), step_length, rainbow_generator)

def dragon(level: int) -> str:
    if level == 1:
        return "R"
    else:
        return dragon(level-1) + "R" + invert_commands(dragon(level-1))[::-1]
    
def dragon_curve(level: int, size: float, rainbow_generator: cycle) -> None:
    draw_curve_no_f(dragon(level), size/(level*math.sqrt(2)), rainbow_generator)

def sierpinski_gasket(level: int, length: float, rainbow_generator: cycle, flipped=1) -> None:
    
    if level == 1:
        t.pencolor(next(rainbow_generator))
        t.forward(length)
    else:
        t.left(60*flipped)
        sierpinski_gasket(level-1, length/2, rainbow_generator, -flipped)
        t.right(60*flipped)
        sierpinski_gasket(level-1, length/2, rainbow_generator, flipped)
        t.right(60*flipped)
        sierpinski_gasket(level-1, length/2, rainbow_generator, -flipped)
        t.left(60*flipped)

def sierpinski_start(level: int, length: float, rainbow_generator) -> None:
    t.teleport(-length/2, -length/3)
    sierpinski_gasket(level, length, rainbow_generator)
   

def iterate_curve(curve: Callable[[int, float, cycle], None], max_iterations: int, size: float, col_list: list[str]) -> None:
    for i in range(1, max_iterations+1):
        print(f"Starting iteration {i}.")
        reset(t)
        t.screen.bgcolor("black")
        t.hideturtle()
        t.speed(0)
        curve(i, size, cycle(col_list))
        sleep(1)
    print("Finished iterations.")

curves = {1: koch_snowflake, 2: hilbert_curve, 3: dragon_curve, 4: sierpinski_start}
curvesno = None
while not curvesno:
    curvesno = simpledialog.askinteger("Select fractal", "What curve do you want to display?\n1) The Koch Snowflake\n2) The Hilbert Curve\n3) The Dragon Curve\n4) Sierpiński gasket", minvalue=1, maxvalue=4)
curve = curves[curvesno]

max_iterations = None
while not max_iterations:
    max_iterations = simpledialog.askinteger("Max iterations", "How many iterations of the curve do you want?", minvalue=1)

rainbow = ['red','orange','yellow','green','blue','indigo','violet']
alt = ["red", "green"]

t = Turtle()
reset(t)

iterate_curve(curve, max_iterations, 500, rainbow)

t.screen.mainloop()