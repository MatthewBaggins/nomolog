from __future__ import annotations
from dataclasses import dataclass

from src.consistency import check_consistency
from src.expression import Expression


@dataclass(frozen=True, slots=True)
class Default:
    name: str
    premises: list[Expression]
    assumptions: list[Expression]
    conclusion: Expression

    @classmethod
    def mk(
        cls,
        name: str,
        premises: list[Expression] | Expression,
        assumptions: list[Expression] | Expression,
        conclusion: Expression,
    ) -> Default:
        premises = premises if isinstance(premises, list) else [premises]
        assumptions = assumptions if isinstance(assumptions, list) else [assumptions]
        return cls(name, premises, assumptions, conclusion)

    def __post_init__(self) -> None:
        check_consistency(*self.assumptions)
