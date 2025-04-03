"""Turtle Fractal Drawer - A Turtle program that draws fractals."""

from turtle import Turtle
from tkinter import simpledialog
from time import sleep
import math
from collections.abc import Callable
from itertools import cycle
from dataclasses import dataclass, field
import re


LENGTH = 500


@dataclass
class Curve:
    """represents the propeties of a curve"""

    name: str
    _initial_pos: tuple[float, float] | Callable[[int], tuple[float, float]]
    _initial_angle: int | Callable[[int], int]
    _curve_size: Callable[[int], float]
    axiom: str
    rules: dict[str, str]
    angle: float = 90

    def l_system_gen(self, level: int) -> str:
        """generates l-system commands"""
        commands: str = self.axiom
        pattern: re.Pattern[str] = re.compile("|".join(self.rules.keys()))
        for _ in range(level - 1):
            commands = pattern.sub(lambda m: self.rules[m.group(0)], commands)
        return commands

    def initial_pos(self, level: int) -> tuple[float, float]:
        """The initial position for the turtle"""
        match self._initial_pos:
            case (x, y):
                pass
            case f:
                x, y = f(level)
        x = LENGTH / x if x else 0
        y = LENGTH / y if y else 0
        return (x, y)

    def initial_angle(self, level: int) -> int:
        """The initial position for the turtle"""
        match self._initial_angle:
            case int(a):
                return a
            case f:
                return f(level)

    def step_length(self, level: int) -> float:
        """The initial position for the turtle"""
        return LENGTH / self._curve_size(level)


curves: list[Curve] = [
    Curve(
        """The Koch snowflake""",
        (-2, 3),
        0,
        lambda level: (3 ** (level - 1)),
        "F++F++F++",
        {"F": "F-F++F-F"},
        60,
    ),
    Curve(
        """The quadratic Koch curve""",
        (-2, 0),
        0,
        lambda level: (3 ** (level - 1)),
        "F",
        {"F": "F-F+F+F-F"},
    ),
    Curve(
        """The Cesàro fractal""",
        (-2, 0),
        0,
        lambda level: (2.5 ** (level - 1)),
        "F++",
        {"F": "F-F++F-F"},
        75.52,
    ),
    Curve(
        """The Minkowski sausage""",
        (-2, 0),
        0,
        lambda level: (4 ** (level - 1)),
        "F",
        {"F": "F+F-F-FF+F+F-F"},
    ),
    Curve(
        """The Minkowski island""",
        (-2, 2),
        0,
        lambda level: (4 ** (level - 1)),
        "F+F+F+F+",
        {"F": "F+F-F-FF+F+F-F"},
    ),
    Curve(
        """The Hilbert Curve""",
        (-2, -2),
        0,
        lambda level: ((2**level) - 1),
        "-BF+AFA+FB-",
        {"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+"},
    ),
    Curve(
        """The Dragon Curve""",
        (0, 0),
        0,
        lambda level: (math.sqrt(2) * (level ** math.sqrt(2))),
        "F",
        {"F": "F-G", "G": "F+G"},
    ),
    Curve(
        """The Sierpiński triangle""",
        (-2, -3),
        0,
        lambda level: (2 ** (level - 1)),
        "F-G-G",
        {"F": "F-G+F+G-F", "G": "GG"},
        120,
    ),
    Curve(
        """The Sierpiński curve""",
        lambda level: (
            -2 * ((2 ** (level) - 2) * (1 + math.sqrt(2)) + 1),
            2,
        ),
        0,
        lambda level: ((2 ** (level) - 2) * (1 + math.sqrt(2)) + 1),
        "F++XF++F++XF",
        {"X": "XF-G-XF++F++XF-G-X"},
        45,
    ),
    Curve(
        """The Sierpiński square curve""",
        lambda level: (-((2 ** (level + 1) - 3)) / 2, 2),
        0,
        lambda level: (2 ** (level + 1) - 3),
        "F+XF+F+XF",
        {"X": "XF-F+F-XF+F+XF-F+F-X"},
    ),
    Curve(
        """The Sierpiński arrowhead curve""",
        (-2, -3),
        lambda level: 60 if level % 2 == 0 else 0,
        lambda level: (2 ** (level - 1)),
        "XF",
        {"X": "YF+XF+Y", "Y": "XF-YF-X"},
        60,
    ),
    Curve(
        """The Gosper curve""",
        (0, 4),
        0,
        lambda level: math.sqrt(7) ** (level),
        "F",
        {"F": "F+G++G-F--FF-G+", "G": "-F+GG++G+F--F-G"},
        60,
    ),
    Curve(
        """The Moore curve""",
        lambda level: (-(((2**level) - 1)) / 2, -2),
        90,
        lambda level: ((2**level) - 1),
        "LFL+F+LFL",
        {"L": "-RF+LFL+FR-", "R": "+LF-RFR-FL+"},
    ),
    Curve(
        """The Peano curve""",
        (-2, -2),
        90,
        lambda level: ((3**level) - 1),
        "XFYFX+F+YFXFY-F-XFYFX",
        {"X": "XFYFX+F+YFXFY-F-XFYFX", "Y": "YFXFY-F-XFYFX+F+YFXFY"},
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
        x, y = self.curve.initial_pos(level)
        self.t.teleport(x, y)
        self.t.left(self.curve.initial_angle(level))
        rainbow_generator = cycle(self.col_list)
        step_length = self.curve.step_length(level)
        commands = self.curve.l_system_gen(level)
        for c in commands:
            if c in "FG":
                self.t.pencolor(next(rainbow_generator))
                self.t.forward(step_length)
            elif c == "+":
                self.t.right(self.curve.angle)
            elif c == "-":
                self.t.left(self.curve.angle)

    def iterate_curve(
        self,
        max_iterations: int,
    ) -> None:
        """draws multiple iterations of a curve"""
        for i in range(1, max_iterations + 1):
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


def main():
    """main function"""
    dialog = "What curve do you want to display?\n" + "\n".join(
        f"{i}) {v.name}" for i, v in enumerate(curves, 1)
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

    curve_drawer = CurveDrawer(rainbow, curve)
    curve_drawer.iterate_curve(max_iterations)


if __name__ == "__main__":
    main()
