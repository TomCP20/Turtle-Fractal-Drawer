from turtle import Turtle
from tkinter import simpledialog
from time import sleep
import math
from collections.abc import Callable
from itertools import cycle

#fractal

def koch_snowflake(level: int, length: float, rainbow_generator: cycle) -> None:
    
    if level == 1:
        t.pencolor(next(rainbow_generator))
        t.forward(length)
    else:
        koch_snowflake(level-1, length/3, rainbow_generator)
        t.left(60)
        koch_snowflake(level-1, length/3, rainbow_generator)
        t.right(120)
        koch_snowflake(level-1, length/3, rainbow_generator)
        t.left(60)
        koch_snowflake(level-1, length/3, rainbow_generator)

def koch_start(level: int, length: float, rainbow_generator: cycle) -> None:
    t.teleport(-length/2, length/3)
    for _ in range(3):
        koch_snowflake(level, length, rainbow_generator)
        t.right(120)

def gen_hilbert(level: int) -> str:
    if level == 0:
        return ""
    else:
        return "L" + invert_commands(gen_hilbert(level-1)) + "FR" + gen_hilbert(level-1) + "F" + gen_hilbert(level-1) + "RF" + invert_commands(gen_hilbert(level-1)) + "L"

def hilbert_curve(level: int, curve_size: float, rainbow_generator: cycle) -> None:
    t.teleport(-curve_size/2, -curve_size/2)
    step_length = curve_size/((2**level)-1)
    draw_curve_has_f(gen_hilbert(level), step_length, rainbow_generator)

def gen_dragon(level: int) -> str:
    if level == 1:
        return "R"
    else:
        return gen_dragon(level-1) + "R" + invert_commands(gen_dragon(level-1))[::-1]
    
def dragon_curve(level: int, size: float, rainbow_generator: cycle) -> None:
    draw_curve_no_f(gen_dragon(level), size/(math.sqrt(2)*(level**math.sqrt(2))), rainbow_generator)

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

def gen_gosper(level: int) -> str:
    if level == 1:
        return "A"
    return substitute(gen_gosper(level-1), {"A": "A-B--B+A++AA+B-", "B": "+A-BB--B-A++A+B"})

def draw_gosper_curve(level: int, size: float, rainbow_generator: cycle) -> None:
    t.teleport(0, size/4)
    commands = gen_gosper(level)
    step = size/math.sqrt(7)**(level)
    for c in commands:
        if c == "A" or c == "B":
            t.pencolor(next(rainbow_generator))
            t.forward(step)
        elif c == "+":
            t.left(60)
        elif c == "-":
            t.right(60)

def gen_moore(level: int) -> str:
    if level == 1:
        return "LFL+F+LFL"
    else:
        return substitute(gen_moore(level-1), {"L": "-RF+LFL+FR-", "R": "+LF-RFR-FL+"})

def moore_curve(level: int, curve_size: float, rainbow_generator: cycle) -> None:
    step_length = curve_size/((2**level)-1)
    t.teleport(-step_length/2, -curve_size/2)
    t.left(90)
    commands = gen_moore(level)
    for c in commands:
        if c == "F":
            t.pencolor(next(rainbow_generator))
            t.forward(step_length)
        elif c == "+":
            t.right(90)
        elif c == "-":
            t.left(90)
#utility

def substitute(commands: str, rules: dict[str, str]):
    return "".join(rules[c] if c in rules else c for c in commands)

def invert_commands(commands: str) -> str:
    return substitute(commands, {"R": "L", "L": "R", "F": "F"})

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

def iterate_curve(curve: Callable[[int, float, cycle], None], max_iterations: int, size: float, col_list: list[str]) -> None:
    for i in range(1, max_iterations+1):
        reset()
        curve(i, size, cycle(col_list))
        sleep(1)

#UI

def reset():
    t.reset()
    t.screen.screensize(canvwidth=500, canvheight=500,  bg="black")
    t.hideturtle()
    t.speed(0)


curves = {1: koch_start, 2: hilbert_curve, 3: dragon_curve, 4: sierpinski_start, 5: draw_gosper_curve, 6: moore_curve}
curvesno = None
dialog = "\n".join(["What curve do you want to display?", "1) The Koch Snowflake", "2) The Hilbert Curve", "3) The Dragon Curve", "4) Sierpiński gasket", "5) Gosper curve", "6) Moore curve"])
while not curvesno:
    curvesno = simpledialog.askinteger("Select fractal", dialog, minvalue=1, maxvalue=6)
curve = curves[curvesno]

max_iterations = None
while not max_iterations:
    max_iterations = simpledialog.askinteger("Max iterations", "How many iterations of the curve do you want?", minvalue=1)

rainbow = ['red','orange','yellow','green','blue','indigo','violet']
alt = ["red", "green"]

t = Turtle()
reset()

iterate_curve(curve, max_iterations, 500, rainbow)

t.screen.mainloop()