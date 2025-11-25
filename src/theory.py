from __future__ import annotations
from dataclasses import dataclass

from src.consistency import check_consistency
from src.default import Default
from src.expression import Expression
from pprint import pprint


@dataclass(frozen=True, slots=True)
class Theory:
    facts: list[Expression]
    defaults: list[Default]

    @classmethod
    def mk(cls, *args: Expression | Default) -> Theory:
        facts: list[Expression] = []
        defaults: list[Default] = []
        for arg in args:
            if isinstance(arg, Expression):
                facts.append(arg)
            elif isinstance(arg, Default):
                defaults.append(arg)
            else:
                raise TypeError(f"{arg=}; {type(arg)=}")
        return Theory(facts, defaults)

    def _default_premises_satisfied(self, d: Default) -> bool:
        return all(p in self.facts for p in d.premises)

    def _default_consistent(self, d: Default) -> bool:
        return check_consistency(*(self.facts + d.premises + d.assumptions))

    def _default_applicable(self, d: Default) -> bool:
        return self._default_premises_satisfied(d) and self._default_consistent(d)

    def generate_extensions(self) -> dict[tuple[str, ...], Theory]:
        extensions: dict[tuple[str, ...], Theory] = {}
        for d in self.defaults:
            # check derivability
            if self._default_applicable(d):
                # print(d)
                extension = Theory(
                    self.facts + [d.conclusion],
                    defaults=[d_ for d_ in self.defaults if d_ != d],
                )
                extensions[(d.name,)] = extension
                # pprint(extensions)
                further_extensions = extension.generate_extensions()
                for key_of_defaults, further_extension in further_extensions.items():
                    extensions[(d.name, *key_of_defaults)] = further_extension
                # pprint(extensions)
            # if not all(p in self.facts for p in d.premises):
            #     continue
            # if not check_consistency(*(self.facts + d.premises + d.assumptions)):
            #     continue
            # if not all(check_consistency(a) for a in d.assumptions):
            #     continue
            # extension = Theory(
            #     self.facts + [d.conclusion],
            #     defaults=[d_ for d_ in self.defaults if d_ != d],
            # )
            # extensions[(d.name,)] = extension
            # further_extensions = extension.generate_extensions()
            # for key_of_defaults, further_extension in further_extensions.items():
            #     extensions[(d.name, *key_of_defaults)] = further_extension

        return extensions
