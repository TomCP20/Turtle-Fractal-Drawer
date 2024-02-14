from turtle import Turtle
from tkinter import simpledialog
from time import sleep
import math
from collections.abc import Callable
from itertools import cycle
import sys

#fractal

def koch_snowflake(level: int, length: float, rainbow_generator: cycle) -> None:
    step_length = length/(3**(level-1))
    commands = l_system(level, "F", {"F": "F+F--F+F"})
    for c in commands:
        if c == "F":
            t.pencolor(next(rainbow_generator))
            t.forward(step_length)
        elif c == "-":
            t.right(60)
        elif c == "+":
            t.left(60)


def koch_start(level: int, length: float, rainbow_generator: cycle) -> None:
    t.teleport(-length/2, length/3)
    for _ in range(3):
        koch_snowflake(level, length, rainbow_generator)
        t.right(120)

def hilbert_curve(level: int, curve_size: float, rainbow_generator: cycle) -> None:
    t.teleport(-curve_size/2, -curve_size/2)
    step_length = curve_size/((2**level)-1)
    commands = l_system(level, "+BF-AFA-FB+", {"A": "+BF-AFA-FB+", "B": "-AF+BFB+FA-"})
    for c in commands:
        if c == "-":
            t.right(90)
        elif c == "+":
            t.left(90)
        elif c =="F":
            t.pencolor(next(rainbow_generator))
            t.forward(step_length)
    
def dragon_curve(level: int, size: float, rainbow_generator: cycle) -> None:
    
    step_length = size/(math.sqrt(2)*(level**math.sqrt(2)))
    commands = l_system(level, "F", {"F": "F+G", "G": "F-G"})
    for c in commands:
        if c == "-":
            t.right(90)
        elif c == "+":
            t.left(90)
        elif c == "F" or c == "G":
            t.pencolor(next(rainbow_generator))
            t.forward(step_length)

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

def draw_gosper_curve(level: int, size: float, rainbow_generator: cycle) -> None:
    t.teleport(0, size/4)
    commands = l_system(level, "A", {"A": "A-B--B+A++AA+B-", "B": "+A-BB--B-A++A+B"})
    step = size/math.sqrt(7)**(level)
    for c in commands:
        if c == "A" or c == "B":
            t.pencolor(next(rainbow_generator))
            t.forward(step)
        elif c == "+":
            t.left(60)
        elif c == "-":
            t.right(60)

def moore_curve(level: int, curve_size: float, rainbow_generator: cycle) -> None:
    step_length = curve_size/((2**level)-1)
    t.teleport(-step_length/2, -curve_size/2)
    t.left(90)
    commands = l_system(level, "LFL+F+LFL", {"L": "-RF+LFL+FR-", "R": "+LF-RFR-FL+"})
    for c in commands:
        if c == "F":
            t.pencolor(next(rainbow_generator))
            t.forward(step_length)
        elif c == "+":
            t.right(90)
        elif c == "-":
            t.left(90)

def peano_curve(level: int, curve_size: float, rainbow_generator: cycle) -> None:
    step_length = curve_size/((3**level)-1)
    t.teleport(-curve_size/2, -curve_size/2)
    t.left(90)
    commands = l_system(level, "XFYFX+F+YFXFY-F-XFYFX", {"X": "XFYFX+F+YFXFY-F-XFYFX", "Y": "YFXFY-F-XFYFX+F+YFXFY"})
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

def l_system(level: int, axiom: str, rules: dict[str, str]) -> str:
    if level == 1:
        return axiom
    else:
        return substitute(l_system(level-1, axiom, rules), rules)

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


curves = {
    1: (koch_start, "The Koch Snowflake"), 
    2: (hilbert_curve, "The Hilbert Curve"), 
    3: (dragon_curve, "The Dragon Curve"), 
    4: (sierpinski_start, "The Sierpiński gasket"), 
    5: (draw_gosper_curve, "The Gosper curve"), 
    6: (moore_curve, "The Moore curve"), 
    7: (peano_curve, "The Peano curve")}
dialog = "\n".join(["What curve do you want to display?"] + [f"{k}) {v[1]}" for k, v in curves.items()])
curvesno = simpledialog.askinteger("Select fractal", dialog, minvalue=1, maxvalue=max(curves))
if not curvesno:
    sys.exit()
curve = curves[curvesno][0]

max_iterations = simpledialog.askinteger("Max iterations", "How many iterations of the curve do you want?", minvalue=1)

if not max_iterations:
    sys.exit()

rainbow = ['red','orange','yellow','green','blue','indigo','violet']
alt = ["red", "green"]

t = Turtle()
reset()

iterate_curve(curve, max_iterations, 500, rainbow)

t.screen.mainloop()