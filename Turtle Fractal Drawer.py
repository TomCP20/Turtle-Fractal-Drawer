from turtle import Turtle
from time import sleep
import math
from collections.abc import Callable
from itertools import cycle

t = Turtle()
def reset_screen():
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

def iterate_curve(curve: Callable[[int, float, cycle], None], max_iterations: int, size: float, col_list: list[str]) -> None:
    for i in range(1, max_iterations+1):
        print(f"Starting iteration {i}.")
        reset_screen()
        curve(i, size, cycle(col_list))
        sleep(1)
    print("Finished iterations.")



def get_curve(curves):
    while True:
        print("What curve do you want to display?")
        for num, (_, name) in curves.items():
            print(f"{num}) {name}.")
        no = input()
        if no in curves:
            return curves[no][0]
        else:
            print(f"Input Error: {no} is not a valid input.")

def get_max_iterations():
    while True:
        print("How many iterations of the curve do you want?:")
        no = input()
        try:
            no = int(no)
            if no > 0:
                return no
            else:
                print(f"Input Error: {no} out of range")
        except ValueError:
            print(f"Input Error: {no} is not an int")

reset_screen()

curves = {"1": (koch_snowflake, "The Koch Snowflake"), "2": (hilbert_curve, "The Hilbert Curve"), "3": (dragon_curve, "The Dragon Curve")}
curve = get_curve(curves)

rainbow = ['red','orange','yellow','green','blue','indigo','violet']
alt = ["red", "green"]

max_iterations = get_max_iterations()

iterate_curve(curve, max_iterations, 500, rainbow)

input("Press enter to quit.")