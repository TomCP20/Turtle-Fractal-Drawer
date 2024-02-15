from turtle import Turtle
from tkinter import simpledialog
from time import sleep
import math
from collections.abc import Callable
from itertools import cycle
import sys

#fractal

def koch_snowflake(level: int, length: float, rainbow_generator: cycle) -> None:
    t.teleport(-length/2, length/3)
    step_length = length/(3**(level-1))
    commands = l_system(level, "F", {"F": "F-F++F-F"})
    for _ in range(3):
        draw_l(commands, "F", 60, rainbow_generator, step_length)
        t.right(120)

def hilbert_curve(level: int, curve_size: float, rainbow_generator: cycle) -> None:
    t.teleport(-curve_size/2, -curve_size/2)
    step_length = curve_size/((2**level)-1)
    commands = l_system(level, "-BF+AFA+FB-", {"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+"})
    draw_l(commands, "F", 90, rainbow_generator, step_length)
    
def dragon_curve(level: int, size: float, rainbow_generator: cycle) -> None:
    step_length = size/(math.sqrt(2)*(level**math.sqrt(2)))
    commands = l_system(level, "F", {"F": "F-G", "G": "F+G"})
    draw_l(commands, "FG", 90, rainbow_generator, step_length)

def sierpinski_gasket(level: int, length: float, rainbow_generator: cycle) -> None:
    t.teleport(-length/2, -length/3)
    if level % 2 == 0:
        t.left(60)
    step_length = length/(2**(level-1))
    commands = l_system(level, "XF", {"X": "YF+XF+Y", "Y": " XF-YF-X"})
    draw_l(commands, "F", 60, rainbow_generator, step_length)

def draw_gosper_curve(level: int, size: float, rainbow_generator: cycle) -> None:
    t.teleport(0, size/4)
    step_length = size/math.sqrt(7)**(level)
    commands = l_system(level, "A", {"A": "A+B++B-A--AA-B+", "B": "-A+BB++B+A--A-B"})
    draw_l(commands, "AB", 60, rainbow_generator, step_length)

def moore_curve(level: int, curve_size: float, rainbow_generator: cycle) -> None:
    step_length = curve_size/((2**level)-1)
    t.teleport(-step_length/2, -curve_size/2)
    t.left(90)
    commands = l_system(level, "LFL+F+LFL", {"L": "-RF+LFL+FR-", "R": "+LF-RFR-FL+"})
    draw_l(commands, "F", 90, rainbow_generator, step_length)

def peano_curve(level: int, curve_size: float, rainbow_generator: cycle) -> None:
    step_length = curve_size/((3**level)-1)
    t.teleport(-curve_size/2, -curve_size/2)
    t.left(90)
    commands = l_system(level, "XFYFX+F+YFXFY-F-XFYFX", {"X": "XFYFX+F+YFXFY-F-XFYFX", "Y": "YFXFY-F-XFYFX+F+YFXFY"})
    draw_l(commands, "F", 90, rainbow_generator, step_length)

#utility

def substitute(commands: str, rules: dict[str, str]) -> str:
    return "".join(rules[c] if c in rules else c for c in commands)

def l_system(level: int, axiom: str, rules: dict[str, str]) -> str:
    if level == 1:
        return axiom
    else:
        return substitute(l_system(level-1, axiom, rules), rules)

def draw_l(commands: str, forward: str, angle: int, rainbow_generator: cycle, step_length: float):
    for c in commands:
        if c in forward:
            t.pencolor(next(rainbow_generator))
            t.forward(step_length)
        elif c == "+":
            t.right(angle)
        elif c == "-":
            t.left(angle)


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
    1: (koch_snowflake, "The Koch Snowflake"), 
    2: (hilbert_curve, "The Hilbert Curve"), 
    3: (dragon_curve, "The Dragon Curve"), 
    4: (sierpinski_gasket, "The Sierpiński gasket"), 
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