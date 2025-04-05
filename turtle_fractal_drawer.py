"""Turtle Fractal Drawer - A Turtle program that draws fractals."""

import sys
from turtle import Turtle, Vec2D
from tkinter import simpledialog
from time import sleep
from math import sqrt
from collections.abc import Callable
from itertools import cycle
from dataclasses import dataclass, field
import re


LENGTH = 500

RAINBOW = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]


@dataclass(kw_only=True)
class Curve:
    """represents the propeties of a curve"""

    name: str
    _pos: tuple[float, float] | Callable[[int], tuple[float, float]] = (-1 / 2, -1 / 2)
    _heading: int | Callable[[int], int] = 0
    _curve_size: Callable[[int], float]
    axiom: str = "F"
    rules: dict[str, str]
    angle: float = 90

    def l_system_gen(self, level: int) -> str:
        """generates l-system commands"""
        commands: str = self.axiom
        pattern: re.Pattern[str] = re.compile("|".join(self.rules.keys()))
        for _ in range(level - 1):
            commands = pattern.sub(lambda m: self.rules[m.group(0)], commands)
        return commands

    def initial_pos(self, level: int) -> Vec2D:
        """The initial position for the turtle"""
        match self._pos:
            case (x, y):
                return LENGTH * Vec2D(x, y)
            case f:
                return LENGTH * Vec2D(*f(level))

    def initial_dir(self, level: int) -> int:
        """The initial position for the turtle"""
        match self._heading:
            case int(a):
                return a
            case f:
                return f(level)

    def step_length(self, level: int) -> float:
        """The initial position for the turtle"""
        return LENGTH / self._curve_size(level)


curves: list[Curve] = [
    Curve(
        name="""The Koch snowflake""",
        _pos=(-1 / 2, 1 / 3),
        _curve_size=lambda level: (3 ** (level - 1)),
        axiom="F++F++F++",
        rules={"F": "F-F++F-F"},
        angle=60,
    ),
    Curve(
        name="""The quadratic Koch curve""",
        _pos=(-1 / 2, 0),
        _curve_size=lambda level: (3 ** (level - 1)),
        rules={"F": "F-F+F+F-F"},
    ),
    Curve(
        name="""The Cesàro fractal""",
        _pos=(-1 / 2, 0),
        _curve_size=lambda level: (2.5 ** (level - 1)),
        axiom="F++",
        rules={"F": "F-F++F-F"},
        angle=75.52,
    ),
    Curve(
        name="""The Minkowski sausage""",
        _pos=(-1 / 2, 0),
        _curve_size=lambda level: (4 ** (level - 1)),
        rules={"F": "F+F-F-FF+F+F-F"},
    ),
    Curve(
        name="""The Minkowski island""",
        _pos=(-1 / 2, 1 / 2),
        _curve_size=lambda level: (4 ** (level - 1)),
        axiom="F+F+F+F+",
        rules={"F": "F+F-F-FF+F+F-F"},
    ),
    Curve(
        name="""The Hilbert Curve""",
        _curve_size=lambda level: ((2**level) - 1),
        axiom="-BF+AFA+FB-",
        rules={"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+"},
    ),
    Curve(
        name="""The Dragon Curve""",
        _pos=(0, 0),
        _curve_size=lambda level: (sqrt(2) * (level ** sqrt(2))),
        rules={"F": "F-G", "G": "F+G"},
    ),
    Curve(
        name="""The Twindragon Curve""",
        _pos=(0, 0),
        _curve_size=lambda level: (sqrt(2) * (level ** sqrt(2))),
        axiom="FX+FX+",
        rules={"X": "X+YF", "Y": "FX-Y"},
    ),
    Curve(
        name="""The Terdragon Curve""",
        _pos=(0, 0),
        _curve_size=lambda level: ((level+1)**3-(level+1))/2,
        axiom="F+F-F",
        rules={"F": "F+F-F"},
    ),
    Curve(
        name="""The Sierpiński triangle""",
        _pos=(-1 / 2, -1 / 3),
        _curve_size=lambda level: (2 ** (level - 1)),
        axiom="F-G-G",
        rules={"F": "F-G+F+G-F", "G": "GG"},
        angle=120,
    ),
    Curve(
        name="""The Sierpiński curve""",
        _pos=lambda level: (
            -1 / (2 * ((2 ** (level) - 2) * (1 + sqrt(2)) + 1)),
            1 / 2,
        ),
        _curve_size=lambda level: ((2 ** (level) - 2) * (1 + sqrt(2)) + 1),
        axiom="F++XF++F++XF",
        rules={"X": "XF-G-XF++F++XF-G-X"},
        angle=45,
    ),
    Curve(
        name="""The Sierpiński square curve""",
        _pos=lambda level: (-1 / (((2 ** (level + 1) - 3))) / 2, 1 / 2),
        _curve_size=lambda level: (2 ** (level + 1) - 3),
        axiom="F+XF+F+XF",
        rules={"X": "XF-F+F-XF+F+XF-F+F-X"},
    ),
    Curve(
        name="""The Sierpiński arrowhead curve""",
        _pos=(-1 / 2, -1 / 3),
        _heading=lambda level: 60 if level % 2 == 0 else 0,
        _curve_size=lambda level: (2 ** (level - 1)),
        axiom="XF",
        rules={"X": "YF+XF+Y", "Y": "XF-YF-X"},
        angle=60,
    ),
    Curve(
        name="""The Sierpiński Carpet""",
        _heading=45,
        _curve_size=lambda level: (sqrt(2) / 2) * ((3 ** (level - 1))),
        axiom="F",
        rules={"F": "F+F-F-F-f+F+F+F-F", "f": "fff"},
    ),
    Curve(
        name="""The Gosper curve""",
        _pos=(0, 1 / 4),
        _curve_size=lambda level: sqrt(7) ** (level),
        rules={"F": "F+G++G-F--FF-G+", "G": "-F+GG++G+F--F-G"},
        angle=60,
    ),
    Curve(
        name="""The Moore curve""",
        _pos=lambda level: (-1 / ((((2**level) - 1)) / 2), -1 / 2),
        _heading=90,
        _curve_size=lambda level: ((2**level) - 1),
        axiom="LFL+F+LFL",
        rules={"L": "-RF+LFL+FR-", "R": "+LF-RFR-FL+"},
    ),
    Curve(
        name="""The Peano curve""",
        _heading=90,
        _curve_size=lambda level: ((3**level) - 1),
        axiom="XFYFX+F+YFXFY-F-XFYFX",
        rules={"X": "XFYFX+F+YFXFY-F-XFYFX", "Y": "YFXFY-F-XFYFX+F+YFXFY"},
    ),
    Curve(
        name="""The Peano curve (diagonal)""",
        _heading=45,
        _curve_size=lambda level: (sqrt(2) / 2) * ((3 ** (level - 1))),
        axiom="F",
        rules={"F": "F+F-F-FF-F-F-FF"},
    ),
    Curve(
        name="""fractal (binary) tree""",
        _pos=(0, -1 / 2),
        _heading=90,
        _curve_size=lambda level: (2 ** (level - 1)) * (2 + sqrt(2)) / 3,
        axiom="F",
        rules={"F": "G[-F]+F", "G": "GG"},
        angle=45,
    ),
    Curve(
        name="""fractal (binary) tree with leaves""",
        _pos=(0, -1 / 2),
        _heading=90,
        _curve_size=lambda level: (2 ** (level - 1)) * (2 + sqrt(2)) / 3,
        axiom="FS",
        rules={"F": "G[-FS]+F", "G": "GG"},
        angle=45,
    ),
    Curve(
        name="""fractal plant""",
        _curve_size=lambda level: (1 + sqrt(2)) ** level,
        axiom="-F+[[X]-X]-F[-FX]+X",
        rules={"F": "FF", "X": "F+[[X]-X]-F[-FX]+X"},
        angle=45,
    ),
    Curve(
        name="""The Lévy C curve""",
        _pos=(-1 / 2, 1 / 2),
        _curve_size=lambda level: (sqrt(2)) ** (level - 1),
        axiom="F",
        rules={"F": "+F--F+"},
        angle=45,
    ),
]


@dataclass
class CurveDrawer:
    """class that draws the curve"""

    col_list: list[str]
    curve: Curve
    t: Turtle = field(init=False, default_factory=Turtle)

    def l_system_draw(self, level: int) -> None:
        """draws l-system commands using the turtle"""
        self.t.teleport(*self.curve.initial_pos(level))
        self.t.setheading(self.curve.initial_dir(level))
        rainbow_generator = cycle(self.col_list)
        step_length = self.curve.step_length(level)
        stack: list[tuple[Vec2D, float]] = []
        for command in self.curve.l_system_gen(level):
            match command:
                case "F" | "G":
                    self.t.pencolor(next(rainbow_generator))
                    self.t.forward(step_length)
                case "f":
                    self.t.penup()
                    self.t.forward(step_length)
                    self.t.pendown()
                case "+":
                    self.t.right(self.curve.angle)
                case "-":
                    self.t.left(self.curve.angle)
                case "[":
                    stack.append((self.t.pos(), self.t.heading()))
                case "]":
                    pos, h = stack.pop()
                    self.t.teleport(*pos)
                    self.t.seth(h)
                case "S":
                    self.t.showturtle()
                    self.t.stamp()
                    self.t.hideturtle()
                case _:
                    pass

    def iterate_curve(
        self,
        iterations: int,
    ) -> None:
        """draws multiple iterations of a curve"""
        for i in range(1, iterations + 1):
            self.reset()
            self.l_system_draw(i)
            sleep(1)
        self.t.screen.mainloop()

    def reset(self) -> None:
        """resets the turtle"""
        self.t.reset()
        self.t.screen.screensize(canvwidth=500, canvheight=500, bg="black")
        self.t.hideturtle()
        self.t.speed(0)


def get_curve():
    """ask the user for the desired curve"""
    dialog = "What curve do you want to display?\n" + "\n".join(
        f"{i}) {v.name}" for i, v in enumerate(curves, 1)
    )

    curvesno = simpledialog.askinteger(
        "Select fractal", dialog, minvalue=1, maxvalue=len(curves)
    )
    if not curvesno:
        sys.exit()
    return curves[curvesno - 1]


def get_iterations():
    """ask the user for the desired number of iterations"""
    iterations = simpledialog.askinteger(
        "Max iterations", "How many iterations of the curve do you want?", minvalue=1
    )
    if not iterations:
        sys.exit()
    return iterations


def main():
    """main function"""
    curve = get_curve()

    iterations = get_iterations()

    curve_drawer = CurveDrawer(RAINBOW, curve)
    curve_drawer.iterate_curve(iterations)


def test():
    """a function that draws all the curves for testing purposes"""
    curve_drawer = CurveDrawer(RAINBOW, curves[0])
    for curve in curves:
        print(curve.name)
        curve_drawer.curve = curve
        curve_drawer.reset()
        curve_drawer.l_system_draw(4)
        sleep(1)


if __name__ == "__main__":
    main()
