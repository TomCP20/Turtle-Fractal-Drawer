"""Turtle Fractal Drawer - A Turtle program that draws fractals."""

from turtle import Turtle
from tkinter import simpledialog
from time import sleep
import math
from collections.abc import Callable
from itertools import cycle
from dataclasses import dataclass, field
import re
from typing import Self


LENGTH = 500

@dataclass
class CurveDrawer:
    """class that draws the curve"""

    col_list: list[str]
    t: Turtle = field(init=False, default_factory=Turtle)

    def koch_snowflake(self, level: int) -> None:
        """The Koch snowflake"""
        self.t.teleport(-LENGTH / 2, LENGTH / 3)
        step_length: float = LENGTH / (3 ** (level - 1))
        commands = self.l_system_gen("F++F++F++", {"F": "F-F++F-F"}, level)
        self.l_system_draw(commands, "F", 60, step_length)

    def quadratic_koch_curve(self, level: int) -> None:
        """The quadratic Koch curve"""
        self.t.teleport(-LENGTH / 2, 0)
        step_length = LENGTH / (3 ** (level - 1))
        commands = self.l_system_gen("F", {"F": "F-F+F+F-F"}, level)
        self.l_system_draw(commands, "F", 90, step_length)

    def cesaro_fractal(self, level: int) -> None:
        """The Cesàro fractal"""
        self.t.teleport(-LENGTH / 2, 0)
        step_length = LENGTH / (2.5 ** (level - 1))
        commands = self.l_system_gen("F++", {"F": "F-F++F-F"}, level)
        self.l_system_draw(commands, "F", 75.52, step_length)

    def minkowski_sausage(self, level: int) -> None:
        """The Minkowski sausage"""
        self.t.teleport(-LENGTH / 2, 0)
        step_length = LENGTH / (4 ** (level - 1))
        commands = self.l_system_gen("F", {"F": "F+F-F-FF+F+F-F"}, level)
        self.l_system_draw(commands, "F", 90, step_length)

    def minkowski_island(self, level: int) -> None:
        """The Minkowski sausage"""
        self.t.teleport(-LENGTH / 2, LENGTH / 2)
        step_length = LENGTH / (4 ** (level - 1))
        commands = self.l_system_gen("F+F+F+F+", {"F": "F+F-F-FF+F+F-F"}, level)
        self.l_system_draw(commands, "F", 90, step_length)

    def hilbert_curve(self, level: int) -> None:
        """The Hilbert Curve"""
        self.t.teleport(-LENGTH / 2, -LENGTH / 2)
        step_length = LENGTH / ((2**level) - 1)
        commands = self.l_system_gen(
            "-BF+AFA+FB-", {"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+"}, level
        )
        self.l_system_draw(commands, "F", 90, step_length)

    def dragon_curve(self, level: int) -> None:
        """The Dragon Curve"""
        step_length = LENGTH / (math.sqrt(2) * (level ** math.sqrt(2)))
        commands = self.l_system_gen("F", {"F": "F-G", "G": "F+G"}, level)
        self.l_system_draw(commands, "FG", 90, step_length)

    def sierpinski_triangle(self, level: int) -> None:
        """The Sierpiński triangle"""
        self.t.teleport(-LENGTH / 2, -LENGTH / 3)
        step_length = LENGTH / (2 ** (level - 1))
        commands = self.l_system_gen("F-G-G", {"F": "F-G+F+G-F", "G": "GG"}, level)
        self.l_system_draw(commands, "FG", 120, step_length)

    def sierpinski_curve(self, level: int) -> None:
        """The Sierpiński curve"""
        step_length = LENGTH / (
            2 ** (level) + 2 ** (level + 1 / 2) - 1 - 2 * math.sqrt(2)
        )
        self.t.teleport(-step_length / 2, LENGTH / 2)
        commands = self.l_system_gen("F++XF++F++XF", {"X": "XF-G-XF++F++XF-G-X"}, level)
        self.l_system_draw(commands, "FG", 45, step_length)

    def sierpinski_square_curve(self, level: int) -> None:
        """The Sierpiński square curve"""
        step_length = LENGTH / (2 ** (level + 1) - 3)
        self.t.teleport(-step_length / 2, LENGTH / 2)
        commands = self.l_system_gen("F+XF+F+XF", {"X": "XF-F+F-XF+F+XF-F+F-X"}, level)
        self.l_system_draw(commands, "FG", 90, step_length)

    def sierpinski_arrowhead_curve(self, level: int) -> None:
        """The Sierpiński arrowhead curve"""
        self.t.teleport(-LENGTH / 2, -LENGTH / 3)
        if level % 2 == 0:
            self.t.left(60)
        step_length = LENGTH / (2 ** (level - 1))
        commands = self.l_system_gen("XF", {"X": "YF+XF+Y", "Y": "XF-YF-X"}, level)
        self.l_system_draw(commands, "F", 60, step_length)

    def draw_gosper_curve(self, level: int) -> None:
        """The Gosper curve"""
        self.t.teleport(0, LENGTH / 4)
        step_length = LENGTH / math.sqrt(7) ** (level)
        commands = self.l_system_gen(
            "A", {"A": "A+B++B-A--AA-B+", "B": "-A+BB++B+A--A-B"}, level
        )
        self.l_system_draw(commands, "AB", 60, step_length)

    def moore_curve(self, level: int) -> None:
        """The Moore curve"""
        step_length = LENGTH / ((2**level) - 1)
        self.t.teleport(-step_length / 2, -LENGTH / 2)
        self.t.left(90)
        commands = self.l_system_gen(
            "LFL+F+LFL", {"L": "-RF+LFL+FR-", "R": "+LF-RFR-FL+"}, level
        )
        self.l_system_draw(commands, "F", 90, step_length)

    def peano_curve(self, level: int) -> None:
        """The Peano curve"""
        step_length = LENGTH / ((3**level) - 1)
        self.t.teleport(-LENGTH / 2, -LENGTH / 2)
        self.t.left(90)
        commands = self.l_system_gen(
            "XFYFX+F+YFXFY-F-XFYFX",
            {"X": "XFYFX+F+YFXFY-F-XFYFX", "Y": "YFXFY-F-XFYFX+F+YFXFY"},
            level,
        )
        self.l_system_draw(commands, "F", 90, step_length)

    def l_system_gen(self, axiom: str, rules: dict[str, str], level: int) -> str:
        """generates l-system commands"""
        commands = axiom
        pattern: re.Pattern[str] = re.compile("|".join(rules.keys()))
        for _ in range(level - 1):
            commands = pattern.sub(lambda m: rules[m.group(0)], commands)
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
        self,
        curve_func: Callable[[Self, int], None],
        max_iterations: int,
    ) -> None:
        """draws multiple iterations of a curve"""
        for i in range(1, max_iterations + 1):
            self.reset()
            curve_func(self, i)
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
    curves: list[Callable[[CurveDrawer, int], None]] = [
        CurveDrawer.koch_snowflake,
        CurveDrawer.quadratic_koch_curve,
        CurveDrawer.cesaro_fractal,
        CurveDrawer.minkowski_sausage,
        CurveDrawer.minkowski_island,
        CurveDrawer.hilbert_curve,
        CurveDrawer.dragon_curve,
        CurveDrawer.sierpinski_triangle,
        CurveDrawer.sierpinski_curve,
        CurveDrawer.sierpinski_square_curve,
        CurveDrawer.sierpinski_arrowhead_curve,
        CurveDrawer.draw_gosper_curve,
        CurveDrawer.moore_curve,
        CurveDrawer.peano_curve,
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

    curve_drawer = CurveDrawer(rainbow)
    curve_drawer.iterate_curve(curve_func, max_iterations)


if __name__ == "__main__":
    main()
