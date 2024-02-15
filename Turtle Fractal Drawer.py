from turtle import Turtle
from tkinter import simpledialog
from time import sleep
import math
from collections.abc import Callable
from itertools import cycle
import sys

#fractal

def koch_snowflake(level: int, length: float, rainbow_generator: cycle, t: Turtle) -> None:
    t.teleport(-length/2, length/3)
    step_length = length/(3**(level-1))
    commands = l_system_gen(level, "F++F++F++", {"F": "F-F++F-F"})
    l_system_draw(commands, "F", 60, rainbow_generator, step_length, t)

def quadratic_koch_curve(level: int, length: float, rainbow_generator: cycle, t: Turtle) -> None:
    t.teleport(-length/2, 0)
    step_length = length/(3**(level-1))
    commands = l_system_gen(level, "F", {"F": "F-F+F+F-F"})
    l_system_draw(commands, "F", 90, rainbow_generator, step_length, t)

def hilbert_curve(level: int, curve_size: float, rainbow_generator: cycle, t: Turtle) -> None:
    t.teleport(-curve_size/2, -curve_size/2)
    step_length = curve_size/((2**level)-1)
    commands = l_system_gen(level, "-BF+AFA+FB-", {"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+"})
    l_system_draw(commands, "F", 90, rainbow_generator, step_length, t)
    
def dragon_curve(level: int, size: float, rainbow_generator: cycle, t: Turtle) -> None:
    step_length = size/(math.sqrt(2)*(level**math.sqrt(2)))
    commands = l_system_gen(level, "F", {"F": "F-G", "G": "F+G"})
    l_system_draw(commands, "FG", 90, rainbow_generator, step_length, t)

def sierpinski_triangle(level: int, length: float, rainbow_generator: cycle, t: Turtle) -> None:
    t.teleport(-length/2, -length/3)
    step_length = length/(2**(level-1))
    commands = l_system_gen(level, "F-G-G", {"F": "F-G+F+G-F", "G": "GG"})
    l_system_draw(commands, "FG", 120, rainbow_generator, step_length, t)

def sierpinski_arrowhead_curve(level: int, length: float, rainbow_generator: cycle, t: Turtle) -> None:
    t.teleport(-length/2, -length/3)
    if level % 2 == 0:
        t.left(60)
    step_length = length/(2**(level-1))
    commands = l_system_gen(level, "XF", {"X": "YF+XF+Y", "Y": "XF-YF-X"})
    l_system_draw(commands, "F", 60, rainbow_generator, step_length, t)

def draw_gosper_curve(level: int, size: float, rainbow_generator: cycle, t: Turtle) -> None:
    t.teleport(0, size/4)
    step_length = size/math.sqrt(7)**(level)
    commands = l_system_gen(level, "A", {"A": "A+B++B-A--AA-B+", "B": "-A+BB++B+A--A-B"})
    l_system_draw(commands, "AB", 60, rainbow_generator, step_length, t)

def moore_curve(level: int, curve_size: float, rainbow_generator: cycle, t: Turtle) -> None:
    step_length = curve_size/((2**level)-1)
    t.teleport(-step_length/2, -curve_size/2)
    t.left(90)
    commands = l_system_gen(level, "LFL+F+LFL", {"L": "-RF+LFL+FR-", "R": "+LF-RFR-FL+"})
    l_system_draw(commands, "F", 90, rainbow_generator, step_length, t)

def peano_curve(level: int, curve_size: float, rainbow_generator: cycle, t: Turtle) -> None:
    step_length = curve_size/((3**level)-1)
    t.teleport(-curve_size/2, -curve_size/2)
    t.left(90)
    commands = l_system_gen(level, "XFYFX+F+YFXFY-F-XFYFX", {"X": "XFYFX+F+YFXFY-F-XFYFX", "Y": "YFXFY-F-XFYFX+F+YFXFY"})
    l_system_draw(commands, "F", 90, rainbow_generator, step_length, t)

#utility

def substitute(commands: str, rules: dict[str, str]) -> str:
    return "".join(rules[c] if c in rules else c for c in commands)

def l_system_gen(level: int, axiom: str, rules: dict[str, str]) -> str:
    if level == 1:
        return axiom
    else:
        return substitute(l_system_gen(level-1, axiom, rules), rules)

def l_system_draw(commands: str, forward: str, angle: int, rainbow_generator: cycle, step_length: float, t: Turtle):
    for c in commands:
        if c in forward:
            t.pencolor(next(rainbow_generator))
            t.forward(step_length)
        elif c == "+":
            t.right(angle)
        elif c == "-":
            t.left(angle)


def iterate_curve(curve: Callable[[int, float, cycle, Turtle], None], max_iterations: int, size: float, col_list: list[str], t: Turtle) -> None:
    for i in range(1, max_iterations+1):
        reset(t)
        curve(i, size, cycle(col_list), t)
        sleep(1)

#UI

def reset(t: Turtle):
    t.reset()
    t.screen.screensize(canvwidth=500, canvheight=500,  bg="black")
    t.hideturtle()
    t.speed(0)

def main():
    curves = [
        (koch_snowflake, "The Koch Snowflake"),
        (quadratic_koch_curve, "The Quadratic Koch curve"),
        (hilbert_curve, "The Hilbert Curve"), 
        (dragon_curve, "The Dragon Curve"), 
        (sierpinski_triangle, "The Sierpiński triangle"),
        (sierpinski_arrowhead_curve, "The Sierpiński arrowhead curve"), 
        (draw_gosper_curve, "The Gosper curve"), 
        (moore_curve, "The Moore curve"), 
        (peano_curve, "The Peano curve")]
    dialog = "\n".join(["What curve do you want to display?"] + [f"{i}) {v[1]}" for i, v in enumerate(curves, 1)])

    
    curvesno = simpledialog.askinteger("Select fractal", dialog, minvalue=1, maxvalue=len(curves))
    if not curvesno:
        return
    curve = curves[curvesno-1][0]

    max_iterations = simpledialog.askinteger("Max iterations", "How many iterations of the curve do you want?", minvalue=1)
    if not max_iterations:
        return

    rainbow = ['red','orange','yellow','green','blue','indigo','violet']
    t = Turtle()
    reset(t)

    iterate_curve(curve, max_iterations, 500, rainbow, t)

    t.screen.mainloop()

if __name__ == '__main__':
    main()
