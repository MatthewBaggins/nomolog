from functools import reduce
import itertools as it
import operator as op

from src.expression import Expression


def bin_strings(n: int) -> list[list[bool]]:  # of length n
    strings: list[list[bool]] = []
    for x in range(n + 1):
        # y = n - x
        for idxs in it.combinations(range(n), x):
            s: list[bool] = [False] * n
            for i in idxs:
                s[i] = True
            strings.append(s)
    return strings


def check_consistency(
    *exprs: Expression,
) -> bool:  # ? maybe richer return/report/whatever?
    atoms: list[str] = list(reduce(op.or_, [e.atoms() for e in exprs]))
    # print(atoms)
    n = len(atoms)
    value_strings = bin_strings(n)
    for vs in value_strings:
        vd = dict(zip(atoms, vs))
        expr_truth_values = [e.eval(vd) for e in exprs]
        if all(expr_truth_values):
            return True
    # print(value_strings)
    return False
