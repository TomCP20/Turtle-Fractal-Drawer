"""Turtle Fractal Drawer - A Turtle program that draws fractals."""

from turtle import Turtle
from tkinter import simpledialog
from time import sleep
from math import sqrt
from collections.abc import Callable
from itertools import cycle
from dataclasses import dataclass, field
import re


LENGTH = 500


@dataclass(kw_only = True)
class Curve:
    """represents the propeties of a curve"""

    name: str
    _pos: tuple[float, float] | Callable[[int], tuple[float, float]]
    _dir: int | Callable[[int], int] = 0
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

    def initial_dir(self, level: int) -> tuple[float, float]:
        """The initial position for the turtle"""
        match self._pos:
            case (x, y):
                pass
            case f:
                x, y = f(level)
        x = LENGTH / x if x else 0
        y = LENGTH / y if y else 0
        return (x, y)

    def initial_angle(self, level: int) -> int:
        """The initial position for the turtle"""
        match self._dir:
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
        _pos=(-2, 3),
        _curve_size=lambda level: (3 ** (level - 1)),
        axiom="F++F++F++",
        rules={"F": "F-F++F-F"},
        angle=60,
    ),
    Curve(
        name="""The quadratic Koch curve""",
        _pos=(-2, 0),
        _curve_size=lambda level: (3 ** (level - 1)),
        rules={"F": "F-F+F+F-F"},
    ),
    Curve(
        name="""The Cesàro fractal""",
        _pos=(-2, 0),
        _curve_size=lambda level: (2.5 ** (level - 1)),
        axiom="F++",
        rules={"F": "F-F++F-F"},
        angle=75.52,
    ),
    Curve(
        name="""The Minkowski sausage""",
        _pos=(-2, 0),
        _curve_size=lambda level: (4 ** (level - 1)),
        rules={"F": "F+F-F-FF+F+F-F"},
    ),
    Curve(
        name="""The Minkowski island""",
        _pos=(-2, 2),
        _curve_size=lambda level: (4 ** (level - 1)),
        axiom="F+F+F+F+",
        rules={"F": "F+F-F-FF+F+F-F"},
    ),
    Curve(
        name="""The Hilbert Curve""",
        _pos=(-2, -2),
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
        name="""The Sierpiński triangle""",
        _pos=(-2, -3),
        _curve_size=lambda level: (2 ** (level - 1)),
        axiom="F-G-G",
        rules={"F": "F-G+F+G-F", "G": "GG"},
        angle=120,
    ),
    Curve(
        name="""The Sierpiński curve""",
        _pos=lambda level: (
            -2 * ((2 ** (level) - 2) * (1 + sqrt(2)) + 1),
            2,
        ),
        _curve_size=lambda level: ((2 ** (level) - 2) * (1 + sqrt(2)) + 1),
        axiom="F++XF++F++XF",
        rules={"X": "XF-G-XF++F++XF-G-X"},
        angle=45,
    ),
    Curve(
        name="""The Sierpiński square curve""",
        _pos=lambda level: (-((2 ** (level + 1) - 3)) / 2, 2),
        _curve_size=lambda level: (2 ** (level + 1) - 3),
        axiom="F+XF+F+XF",
        rules={"X": "XF-F+F-XF+F+XF-F+F-X"},
    ),
    Curve(
        name="""The Sierpiński arrowhead curve""",
        _pos=(-2, -3),
        _dir=lambda level: 60 if level % 2 == 0 else 0,
        _curve_size=lambda level: (2 ** (level - 1)),
        axiom="XF",
        rules={"X": "YF+XF+Y", "Y": "XF-YF-X"},
        angle=60,
    ),
    Curve(
        name="""The Gosper curve""",
        _pos=(0, 4),
        _curve_size=lambda level: sqrt(7) ** (level),
        rules={"F": "F+G++G-F--FF-G+", "G": "-F+GG++G+F--F-G"},
        angle=60,
    ),
    Curve(
        name="""The Moore curve""",
        _pos=lambda level: (-(((2**level) - 1)) / 2, -2),
        _dir=90,
        _curve_size=lambda level: ((2**level) - 1),
        axiom="LFL+F+LFL",
        rules={"L": "-RF+LFL+FR-", "R": "+LF-RFR-FL+"},
    ),
    Curve(
        name="""The Peano curve""",
        _pos=(-2, -2),
        _dir=90,
        _curve_size=lambda level: ((3**level) - 1),
        axiom="XFYFX+F+YFXFY-F-XFYFX",
        rules={"X": "XFYFX+F+YFXFY-F-XFYFX", "Y": "YFXFY-F-XFYFX+F+YFXFY"},
    ),
    Curve(
        name="""fractal (binary) tree""",
        _pos=(0, -2),
        _dir=90,
        _curve_size=lambda level: (2**(level-1))*(2+sqrt(2))/3,
        axiom="FS",
        rules={"F": "G[-FS]+F", "G": "GG"},
        angle=45
    ),
    Curve(
        name="""fractal plant""",
        _pos=(-2, -2),
        _curve_size=lambda level: (level-1)**2 + 1,
        axiom="-X",
        rules={"F": "FF", "X": "F+[[X]-X]-F[-FX]+X"},
        angle=45
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
        x, y = self.curve.initial_dir(level)
        self.t.teleport(x, y)
        self.t.setheading(self.curve.initial_angle(level))
        rainbow_generator = cycle(self.col_list)
        step_length = self.curve.step_length(level)
        commands = self.curve.l_system_gen(level)
        stack: list[tuple[tuple[float, float], float]] = []
        for c in commands:
            if c in "FG":
                self.t.pencolor(next(rainbow_generator))
                self.t.forward(step_length)
            elif c == "+":
                self.t.right(self.curve.angle)
            elif c == "-":
                self.t.left(self.curve.angle)
            elif c == "[":
                stack.append((self.t.pos(), self.t.heading()))
            elif c == "]":
                pos, h = stack.pop()
                self.t.teleport(*pos)
                self.t.seth(h)
            elif c == "S":
                self.t.showturtle()
                self.t.stamp()
                self.t.hideturtle()

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
