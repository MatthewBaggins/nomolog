from pprint import pprint
import typing as typ

from src import (
    Atom,
    Not,
    Default,
    Theory,
    generate_integer_atoms,
    Expression,
)


def test1() -> None:
    b = Atom("b")
    f = Atom("f")
    x = Atom("x")
    not_f = Not(f)
    d1 = Default.mk("d1", b, f, f)
    d2 = Default.mk("d2", b, not_f, not_f)
    d3 = Default.mk("d3", f, b, x)
    theory = Theory.mk(b, d1, d2, d3)

    # print(theory)

    extensions = theory.generate_extensions()
    pprint(extensions)


def test2() -> None:
    atoms = typ.cast(list[Expression], generate_integer_atoms(10))
    d1 = Default.mk(
        "d1",
        premises=atoms[:3],
        assumptions=[atoms[5], atoms[-1]],
        conclusion=atoms[-1],
    )
    d2 = Default.mk(
        "d2", premises=atoms[:6], assumptions=atoms[6:], conclusion=atoms[7]
    )
    d3 = Default.mk(
        "d3", premises=atoms[3:7], assumptions=[Not(atoms[8])], conclusion=Not(atoms[8])
    )
    d4 = Default.mk(
        "d4", premises=[atoms[0], atoms[9]], assumptions=[atoms[8]], conclusion=atoms[8]
    )

    theory = Theory(atoms[:5], [d1, d2, d3, d4])
    # print(theory)
    extensions = theory.generate_extensions()
    pprint(extensions)


if __name__ == "__main__":
    test2()
