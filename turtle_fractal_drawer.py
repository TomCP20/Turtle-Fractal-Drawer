"""Turtle Fractal Drawer - A Turtle program that draws fractals."""

from turtle import Turtle
from tkinter import simpledialog
from time import sleep
import math
from collections.abc import Callable
from itertools import cycle
from typing import Iterator

type Curve = Callable[[int, float, Iterator[str], Turtle], None]

# curves


def koch_snowflake(
    level: int, length: float, rainbow_generator: Iterator[str], t: Turtle
) -> None:
    """The Koch snowflake"""
    t.teleport(-length / 2, length / 3)
    step_length = length / (3 ** (level - 1))
    commands = l_system_gen(level, "F++F++F++", {"F": "F-F++F-F"})
    l_system_draw(commands, "F", 60, rainbow_generator, step_length, t)


def quadratic_koch_curve(
    level: int, length: float, rainbow_generator: Iterator[str], t: Turtle
) -> None:
    """The quadratic Koch curve"""
    t.teleport(-length / 2, 0)
    step_length = length / (3 ** (level - 1))
    commands = l_system_gen(level, "F", {"F": "F-F+F+F-F"})
    l_system_draw(commands, "F", 90, rainbow_generator, step_length, t)


def cesaro_fractal(
    level: int, length: float, rainbow_generator: Iterator[str], t: Turtle
) -> None:
    """The Cesàro fractal"""
    t.teleport(-length / 2, 0)
    step_length = length / (2.5 ** (level - 1))
    commands = l_system_gen(level, "F++", {"F": "F-F++F-F"})
    l_system_draw(commands, "F", 75.52, rainbow_generator, step_length, t)


def minkowski_sausage(
    level: int, length: float, rainbow_generator: Iterator[str], t: Turtle
) -> None:
    """The Minkowski sausage"""
    t.teleport(-length / 2, 0)
    step_length = length / (4 ** (level - 1))
    commands = l_system_gen(level, "F", {"F": "F+F-F-FF+F+F-F"})
    l_system_draw(commands, "F", 90, rainbow_generator, step_length, t)


def minkowski_island(
    level: int, length: float, rainbow_generator: Iterator[str], t: Turtle
) -> None:
    """The Minkowski sausage"""
    t.teleport(-length / 2, length / 2)
    step_length = length / (4 ** (level - 1))
    commands = l_system_gen(level, "F+F+F+F+", {"F": "F+F-F-FF+F+F-F"})
    l_system_draw(commands, "F", 90, rainbow_generator, step_length, t)


def hilbert_curve(
    level: int, curve_size: float, rainbow_generator: Iterator[str], t: Turtle
) -> None:
    """The Hilbert Curve"""
    t.teleport(-curve_size / 2, -curve_size / 2)
    step_length = curve_size / ((2**level) - 1)
    commands = l_system_gen(
        level, "-BF+AFA+FB-", {"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+"}
    )
    l_system_draw(commands, "F", 90, rainbow_generator, step_length, t)


def dragon_curve(
    level: int, size: float, rainbow_generator: Iterator[str], t: Turtle
) -> None:
    """The Dragon Curve"""
    step_length = size / (math.sqrt(2) * (level ** math.sqrt(2)))
    commands = l_system_gen(level, "F", {"F": "F-G", "G": "F+G"})
    l_system_draw(commands, "FG", 90, rainbow_generator, step_length, t)


def sierpinski_triangle(
    level: int, length: float, rainbow_generator: Iterator[str], t: Turtle
) -> None:
    """The Sierpiński triangle"""
    t.teleport(-length / 2, -length / 3)
    step_length = length / (2 ** (level - 1))
    commands = l_system_gen(level, "F-G-G", {"F": "F-G+F+G-F", "G": "GG"})
    l_system_draw(commands, "FG", 120, rainbow_generator, step_length, t)


def sierpinski_curve(
    level: int, length: float, rainbow_generator: Iterator[str], t: Turtle
) -> None:
    """The Sierpiński curve"""
    step_length = length / (2 ** (level) + 2 ** (level + 1 / 2) - 1 - 2 * math.sqrt(2))
    t.teleport(-step_length / 2, length / 2)
    commands = l_system_gen(level, "F++XF++F++XF", {"X": "XF-G-XF++F++XF-G-X"})
    l_system_draw(commands, "FG", 45, rainbow_generator, step_length, t)


def sierpinski_square_curve(
    level: int, length: float, rainbow_generator: Iterator[str], t: Turtle
) -> None:
    """The Sierpiński square curve"""
    step_length = length / (2 ** (level + 1) - 3)
    t.teleport(-step_length / 2, length / 2)
    commands = l_system_gen(level, "F+XF+F+XF", {"X": "XF-F+F-XF+F+XF-F+F-X"})
    l_system_draw(commands, "FG", 90, rainbow_generator, step_length, t)


def sierpinski_arrowhead_curve(
    level: int, length: float, rainbow_generator: Iterator[str], t: Turtle
) -> None:
    """The Sierpiński arrowhead curve"""
    t.teleport(-length / 2, -length / 3)
    if level % 2 == 0:
        t.left(60)
    step_length = length / (2 ** (level - 1))
    commands = l_system_gen(level, "XF", {"X": "YF+XF+Y", "Y": "XF-YF-X"})
    l_system_draw(commands, "F", 60, rainbow_generator, step_length, t)


def draw_gosper_curve(
    level: int, size: float, rainbow_generator: Iterator[str], t: Turtle
) -> None:
    """The Gosper curve"""
    t.teleport(0, size / 4)
    step_length = size / math.sqrt(7) ** (level)
    commands = l_system_gen(
        level, "A", {"A": "A+B++B-A--AA-B+", "B": "-A+BB++B+A--A-B"}
    )
    l_system_draw(commands, "AB", 60, rainbow_generator, step_length, t)


def moore_curve(
    level: int, curve_size: float, rainbow_generator: Iterator[str], t: Turtle
) -> None:
    """The Moore curve"""
    step_length = curve_size / ((2**level) - 1)
    t.teleport(-step_length / 2, -curve_size / 2)
    t.left(90)
    commands = l_system_gen(
        level, "LFL+F+LFL", {"L": "-RF+LFL+FR-", "R": "+LF-RFR-FL+"}
    )
    l_system_draw(commands, "F", 90, rainbow_generator, step_length, t)


def peano_curve(
    level: int, curve_size: float, rainbow_generator: Iterator[str], t: Turtle
) -> None:
    """The Peano curve"""
    step_length = curve_size / ((3**level) - 1)
    t.teleport(-curve_size / 2, -curve_size / 2)
    t.left(90)
    commands = l_system_gen(
        level,
        "XFYFX+F+YFXFY-F-XFYFX",
        {"X": "XFYFX+F+YFXFY-F-XFYFX", "Y": "YFXFY-F-XFYFX+F+YFXFY"},
    )
    l_system_draw(commands, "F", 90, rainbow_generator, step_length, t)


# utility


def l_system_gen(level: int, axiom: str, rules: dict[str, str]) -> str:
    """generates l-system commands"""
    if level == 1:
        return axiom
    return "".join(
        rules[command] if command in rules else command
        for command in l_system_gen(level - 1, axiom, rules)
    )


def l_system_draw(
    commands: str,
    forward: str,
    angle: float,
    rainbow_generator: Iterator[str],
    step_length: float,
    t: Turtle,
) -> None:
    """draws l-system commands using the turtle"""
    for c in commands:
        if c in forward:
            t.pencolor(next(rainbow_generator))
            t.forward(step_length)
        elif c == "+":
            t.right(angle)
        elif c == "-":
            t.left(angle)


def iterate_curve(
    curve: Curve,
    max_iterations: int,
    size: float,
    col_list: list[str],
    t: Turtle,
) -> None:
    """draws multiple iterations of a curve"""
    for i in range(1, max_iterations + 1):
        reset(t)
        curve(i, size, cycle(col_list), t)
        sleep(1)


# UI


def reset(t: Turtle) -> None:
    """resets the turtle"""
    t.reset()
    t.screen.screensize(canvwidth=500, canvheight=500, bg="black")
    t.hideturtle()
    t.speed(0)


def main():
    """main function"""
    curves: list[Curve] = [
        koch_snowflake,
        quadratic_koch_curve,
        cesaro_fractal,
        minkowski_sausage,
        minkowski_island,
        hilbert_curve,
        dragon_curve,
        sierpinski_triangle,
        sierpinski_curve,
        sierpinski_square_curve,
        sierpinski_arrowhead_curve,
        draw_gosper_curve,
        moore_curve,
        peano_curve,
    ]
    dialog = "What curve do you want to display?\n" + "\n".join(
        f"{i}) {v.__doc__}" for i, v in enumerate(curves, 1)
    )

    curvesno = simpledialog.askinteger(
        "Select fractal", dialog, minvalue=1, maxvalue=len(curves)
    )
    if not curvesno:
        return
    curve = curves[curvesno - 1]

    max_iterations = simpledialog.askinteger(
        "Max iterations", "How many iterations of the curve do you want?", minvalue=1
    )
    if not max_iterations:
        return

    rainbow = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
    t = Turtle()
    reset(t)

    iterate_curve(curve, max_iterations, 500, rainbow, t)

    t.screen.mainloop()


if __name__ == "__main__":
    main()
