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
    initial_pos: Callable[[int], tuple[float, float]]
    initial_angle: Callable[[int], int]
    step_length: Callable[[int], float]
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


curves: list[Curve] = [
    Curve(
        """The Koch snowflake""",
        lambda _: (-LENGTH / 2, LENGTH / 3),
        lambda _: 0,
        lambda level: LENGTH / (3 ** (level - 1)),
        "F++F++F++",
        {"F": "F-F++F-F"},
        60,
    ),
    Curve(
        """The quadratic Koch curve""",
        lambda _: (-LENGTH / 2, 0),
        lambda _: 0,
        lambda level: LENGTH / (3 ** (level - 1)),
        "F",
        {"F": "F-F+F+F-F"},
    ),
    Curve(
        """The Cesàro fractal""",
        lambda _: (-LENGTH / 2, 0),
        lambda _: 0,
        lambda level: LENGTH / (2.5 ** (level - 1)),
        "F++",
        {"F": "F-F++F-F"},
        75.52,
    ),
    Curve(
        """The Minkowski sausage""",
        lambda _: (-LENGTH / 2, 0),
        lambda _: 0,
        lambda level: LENGTH / (4 ** (level - 1)),
        "F",
        {"F": "F+F-F-FF+F+F-F"},
    ),
    Curve(
        """The Minkowski island""",
        lambda _: (-LENGTH / 2, LENGTH / 2),
        lambda _: 0,
        lambda level: LENGTH / (4 ** (level - 1)),
        "F+F+F+F+",
        {"F": "F+F-F-FF+F+F-F"},
    ),
    Curve(
        """The Hilbert Curve""",
        lambda _: (-LENGTH / 2, -LENGTH / 2),
        lambda _: 0,
        lambda level: LENGTH / ((2**level) - 1),
        "-BF+AFA+FB-",
        {"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+"},
    ),
    Curve(
        """The Dragon Curve""",
        lambda _: (0, 0),
        lambda _: 0,
        lambda level: LENGTH / (math.sqrt(2) * (level ** math.sqrt(2))),
        "F",
        {"F": "F-G", "G": "F+G"},
    ),
    Curve(
        """The Sierpiński triangle""",
        lambda _: (-LENGTH / 2, -LENGTH / 3),
        lambda _: 0,
        lambda level: LENGTH / (2 ** (level - 1)),
        "F-G-G",
        {"F": "F-G+F+G-F", "G": "GG"},
        120,
    ),
    Curve(
        """The Sierpiński curve""",
        lambda level: (
            -(LENGTH / (2 ** (level) + 2 ** (level + 1 / 2) - 1 - 2 * math.sqrt(2)))
            / 2,
            LENGTH / 2,
        ),
        lambda _: 0,
        lambda level: LENGTH
        / (2 ** (level) + 2 ** (level + 1 / 2) - 1 - 2 * math.sqrt(2)),
        "F++XF++F++XF",
        {"X": "XF-G-XF++F++XF-G-X"},
        45,
    ),
    Curve(
        """The Sierpiński square curve""",
        lambda level: (-(LENGTH / (2 ** (level + 1) - 3)) / 2, LENGTH / 2),
        lambda _: 0,
        lambda level: LENGTH / (2 ** (level + 1) - 3),
        "F+XF+F+XF",
        {"X": "XF-F+F-XF+F+XF-F+F-X"},
    ),
    Curve(
        """The Sierpiński arrowhead curve""",
        lambda _: (-LENGTH / 2, -LENGTH / 3),
        lambda level: 60 if level % 2 == 0 else 0,
        lambda level: LENGTH / (2 ** (level - 1)),
        "XF",
        {"X": "YF+XF+Y", "Y": "XF-YF-X"},
        60,
    ),
    Curve(
        """The Gosper curve""",
        lambda _: (0, LENGTH / 4),
        lambda _: 0,
        lambda level: LENGTH / math.sqrt(7) ** (level),
        "F",
        {"F": "F+G++G-F--FF-G+", "G": "-F+GG++G+F--F-G"},
        60,
    ),
    Curve(
        """The Moore curve""",
        lambda level: (-(LENGTH / ((2**level) - 1)) / 2, -LENGTH / 2),
        lambda _: 90,
        lambda level: LENGTH / ((2**level) - 1),
        "LFL+F+LFL",
        {"L": "-RF+LFL+FR-", "R": "+LF-RFR-FL+"},
    ),
    Curve(
        """The Peano curve""",
        lambda _: (-LENGTH / 2, -LENGTH / 2),
        lambda _: 90,
        lambda level: LENGTH / ((3**level) - 1),
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
        self.t.teleport(*self.curve.initial_pos(level))
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
