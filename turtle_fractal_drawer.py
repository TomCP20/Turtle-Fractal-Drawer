"""Turtle Fractal Drawer - A Turtle program that draws fractals."""

from turtle import Turtle
from tkinter import simpledialog
from time import sleep
import math
from collections.abc import Callable
from itertools import cycle
from dataclasses import dataclass
import re


@dataclass
class Curve:
    """class that draws the curve"""

    level: int
    length: float
    col_list: list[str]
    t: Turtle

    def koch_snowflake(
        self,
    ) -> None:
        """The Koch snowflake"""
        self.t.teleport(-self.length / 2, self.length / 3)
        step_length: float = self.length / (3 ** (self.level - 1))
        commands = self.l_system_gen("F++F++F++", {"F": "F-F++F-F"})
        self.l_system_draw(commands, "F", 60, step_length)

    def quadratic_koch_curve(self) -> None:
        """The quadratic Koch curve"""
        self.t.teleport(-self.length / 2, 0)
        step_length = self.length / (3 ** (self.level - 1))
        commands = self.l_system_gen("F", {"F": "F-F+F+F-F"})
        self.l_system_draw(commands, "F", 90, step_length)

    def cesaro_fractal(self) -> None:
        """The Cesàro fractal"""
        self.t.teleport(-self.length / 2, 0)
        step_length = self.length / (2.5 ** (self.level - 1))
        commands = self.l_system_gen("F++", {"F": "F-F++F-F"})
        self.l_system_draw(commands, "F", 75.52, step_length)

    def minkowski_sausage(self) -> None:
        """The Minkowski sausage"""
        self.t.teleport(-self.length / 2, 0)
        step_length = self.length / (4 ** (self.level - 1))
        commands = self.l_system_gen("F", {"F": "F+F-F-FF+F+F-F"})
        self.l_system_draw(commands, "F", 90, step_length)

    def minkowski_island(self) -> None:
        """The Minkowski sausage"""
        self.t.teleport(-self.length / 2, self.length / 2)
        step_length = self.length / (4 ** (self.level - 1))
        commands = self.l_system_gen("F+F+F+F+", {"F": "F+F-F-FF+F+F-F"})
        self.l_system_draw(commands, "F", 90, step_length)

    def hilbert_curve(self) -> None:
        """The Hilbert Curve"""
        self.t.teleport(-self.length / 2, -self.length / 2)
        step_length = self.length / ((2**self.level) - 1)
        commands = self.l_system_gen(
            "-BF+AFA+FB-", {"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+"}
        )
        self.l_system_draw(commands, "F", 90, step_length)

    def dragon_curve(self) -> None:
        """The Dragon Curve"""
        step_length = self.length / (math.sqrt(2) * (self.level ** math.sqrt(2)))
        commands = self.l_system_gen("F", {"F": "F-G", "G": "F+G"})
        self.l_system_draw(commands, "FG", 90, step_length)

    def sierpinski_triangle(self) -> None:
        """The Sierpiński triangle"""
        self.t.teleport(-self.length / 2, -self.length / 3)
        step_length = self.length / (2 ** (self.level - 1))
        commands = self.l_system_gen("F-G-G", {"F": "F-G+F+G-F", "G": "GG"})
        self.l_system_draw(commands, "FG", 120, step_length)

    def sierpinski_curve(self) -> None:
        """The Sierpiński curve"""
        step_length = self.length / (
            2 ** (self.level) + 2 ** (self.level + 1 / 2) - 1 - 2 * math.sqrt(2)
        )
        self.t.teleport(-step_length / 2, self.length / 2)
        commands = self.l_system_gen("F++XF++F++XF", {"X": "XF-G-XF++F++XF-G-X"})
        self.l_system_draw(commands, "FG", 45, step_length)

    def sierpinski_square_curve(self) -> None:
        """The Sierpiński square curve"""
        step_length = self.length / (2 ** (self.level + 1) - 3)
        self.t.teleport(-step_length / 2, self.length / 2)
        commands = self.l_system_gen("F+XF+F+XF", {"X": "XF-F+F-XF+F+XF-F+F-X"})
        self.l_system_draw(commands, "FG", 90, step_length)

    def sierpinski_arrowhead_curve(self) -> None:
        """The Sierpiński arrowhead curve"""
        self.t.teleport(-self.length / 2, -self.length / 3)
        if self.level % 2 == 0:
            self.t.left(60)
        step_length = self.length / (2 ** (self.level - 1))
        commands = self.l_system_gen("XF", {"X": "YF+XF+Y", "Y": "XF-YF-X"})
        self.l_system_draw(commands, "F", 60, step_length)

    def draw_gosper_curve(self) -> None:
        """The Gosper curve"""
        self.t.teleport(0, self.length / 4)
        step_length = self.length / math.sqrt(7) ** (self.level)
        commands = self.l_system_gen(
            "A", {"A": "A+B++B-A--AA-B+", "B": "-A+BB++B+A--A-B"}
        )
        self.l_system_draw(commands, "AB", 60, step_length)

    def moore_curve(self) -> None:
        """The Moore curve"""
        step_length = self.length / ((2**self.level) - 1)
        self.t.teleport(-step_length / 2, -self.length / 2)
        self.t.left(90)
        commands = self.l_system_gen(
            "LFL+F+LFL", {"L": "-RF+LFL+FR-", "R": "+LF-RFR-FL+"}
        )
        self.l_system_draw(commands, "F", 90, step_length)

    def peano_curve(self) -> None:
        """The Peano curve"""
        step_length = self.length / ((3**self.level) - 1)
        self.t.teleport(-self.length / 2, -self.length / 2)
        self.t.left(90)
        commands = self.l_system_gen(
            "XFYFX+F+YFXFY-F-XFYFX",
            {"X": "XFYFX+F+YFXFY-F-XFYFX", "Y": "YFXFY-F-XFYFX+F+YFXFY"},
        )
        self.l_system_draw(commands, "F", 90, step_length)

    def l_system_gen(self, axiom: str, rules: dict[str, str]) -> str:
        """generates l-system commands"""
        commands = axiom
        pattern: re.Pattern[str] = re.compile("|".join(rules.keys()))
        for _ in range(self.level - 1):
            commands = pattern.sub(lambda m : rules[m.group(0)], commands)
        return commands

    def l_system_draw(
        self,
        commands: str,
        forward: str,
        angle: float,
        step_length: float,
    ) -> None:
        """draws l-system commands using the turtle"""
        rainbow_generator = cycle(self.col_list)
        for c in commands:
            if c in forward:
                self.t.pencolor(next(rainbow_generator))
                self.t.forward(step_length)
            elif c == "+":
                self.t.right(angle)
            elif c == "-":
                self.t.left(angle)


def iterate_curve(
    curve_func: Callable[[Curve], None],
    max_iterations: int,
    size: float,
    col_list: list[str],
    t: Turtle,
) -> None:
    """draws multiple iterations of a curve"""
    for i in range(1, max_iterations + 1):
        reset(t)
        curve_func(Curve(i, size, col_list, t))
        sleep(1)


def reset(t: Turtle) -> None:
    """resets the turtle"""
    t.reset()
    t.screen.screensize(canvwidth=500, canvheight=500, bg="black")
    t.hideturtle()
    t.speed(0)


def main():
    """main function"""
    curves: list[Callable[[Curve], None]] = [
        Curve.koch_snowflake,
        Curve.quadratic_koch_curve,
        Curve.cesaro_fractal,
        Curve.minkowski_sausage,
        Curve.minkowski_island,
        Curve.hilbert_curve,
        Curve.dragon_curve,
        Curve.sierpinski_triangle,
        Curve.sierpinski_curve,
        Curve.sierpinski_square_curve,
        Curve.sierpinski_arrowhead_curve,
        Curve.draw_gosper_curve,
        Curve.moore_curve,
        Curve.peano_curve,
    ]
    dialog = "What curve do you want to display?\n" + "\n".join(
        f"{i}) {v.__doc__}" for i, v in enumerate(curves, 1)
    )

    curvesno = simpledialog.askinteger(
        "Select fractal", dialog, minvalue=1, maxvalue=len(curves)
    )
    if not curvesno:
        return
    curve_func = curves[curvesno - 1]

    max_iterations = simpledialog.askinteger(
        "Max iterations", "How many iterations of the curve do you want?", minvalue=1
    )
    if not max_iterations:
        return

    rainbow = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
    t = Turtle()

    iterate_curve(curve_func, max_iterations, 500, rainbow, t)

    t.screen.mainloop()


if __name__ == "__main__":
    main()
