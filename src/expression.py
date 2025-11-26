from __future__ import annotations

from abc import ABC, abstractmethod


class Expression(ABC):
    def __and__(self, e: Expression) -> And:
        self_args = self.exprs if isinstance(self, And) else [self]
        e_args = e.exprs if isinstance(e, And) else [e]
        return And(self_args + e_args)

    def __or__(self, e: Expression) -> Or:
        self_args = self.exprs if isinstance(self, Or) else [self]
        e_args = e.exprs if isinstance(e, Or) else [e]
        return Or(self_args + e_args)

    def __gt__(self, e: Expression) -> Implies:
        return Implies(self, e)

    def __repr__(self) -> str:
        if len(slots := self._slots()) == 1:
            item = getattr(self, slots[0])
            if isinstance(item, list):
                s = ", ".join(str(x) for x in item)
                # s = ", ".join([str(x) if isinstance(x, Atom) else x for x in item])
            else:
                s = f"{item!r}" if not isinstance(item, Atom) else str(item)
        else:
            s = ", ".join(f"{k}={getattr(self, k)}" for k in slots)
        return f"{self.__class__.__name__}({s})"

    def __eq__(self, other: Expression) -> bool:
        return (type(self) is type(other)) and all(
            getattr(self, k, None) == getattr(other, k, None) for k in self._slots()
        )

    def _slots(self) -> list[str]:
        slots: list[str] = getattr(self, "__slots__", [])
        assert slots
        return slots

    def asdict(self) -> tuple[str, dict]:
        return (self.__class__.__name__, {k: getattr(self, k) for k in self._slots()})

    def atoms(self) -> set[str]:
        atoms: set[str] = set()
        for k in getattr(self, "__slots__", []):
            if isinstance(item := getattr(self, k), str):
                atoms.add(item)
            elif isinstance(item, Expression):
                atoms |= item.atoms()
            elif isinstance(item, list):
                for elem in item:
                    assert isinstance(elem, Expression), f"{elem=}; {type(elem)=}"
                    atoms |= elem.atoms()
            else:
                # print(type(item), item)
                raise TypeError(f"{item=}; {type(item)=}")
        return atoms

    @abstractmethod
    def eval(self, atoms: dict[str, bool]) -> bool: ...


class Atom(Expression):
    __slots__ = ("s",)
    s: str

    def __init__(self, s: str) -> None:
        self.s = s

    def __str__(self) -> str:
        return f"'{self.s}'"

    def eval(self, atoms: dict[str, bool]) -> bool:
        assert self.s in atoms, (self.s, atoms)
        return atoms[self.s]


class Not(Expression):
    __slots__ = ("s",)
    s: Expression

    def __init__(self, s: Expression) -> None:
        self.s = s

    def eval(self, atoms: dict[str, bool]) -> bool:
        return not self.s.eval(atoms)


class And(Expression):
    __slots__ = ("exprs",)
    exprs: list[Expression]

    def __init__(self, exprs: list[Expression]) -> None:
        self.exprs = exprs

    # def __str__(self) -> str:
    #     return super(self).__repr__(self)

    @classmethod
    def mk(cls, *exprs: Expression) -> And:
        return And(list(exprs))

    def eval(self, atoms: dict[str, bool]) -> bool:
        return all(e.eval(atoms) for e in self.exprs)


class Or(Expression):
    __slots__ = ("exprs",)
    exprs: list[Expression]

    def __init__(self, exprs: list[Expression]) -> None:
        self.exprs = exprs

    @classmethod
    def mk(cls, *exprs: Expression) -> Or:
        return Or(list(exprs))

    def eval(self, atoms: dict[str, bool]) -> bool:
        return any(e.eval(atoms) for e in self.exprs)


class Implies(Expression):
    __slots__ = ("antecedent", "consequent")
    antecedent: Expression
    consequent: Expression

    def __init__(self, antecedent: Expression, consequent: Expression) -> None:
        self.antecedent = antecedent
        self.consequent = consequent

    def eval(self, atoms: dict[str, bool]) -> bool:
        return not self.antecedent.eval(atoms) or self.consequent.eval(atoms)


def generate_integer_atoms(n: int) -> list[Atom]:
    assert n > 0, n
    return [Atom(str(i)) for i in range(n)]
