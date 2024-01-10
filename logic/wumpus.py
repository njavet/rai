import collections
import functools

from rich.text import Text
from rich.console import Console
import random
import itertools

from logic import PropVar, Not, Implication, And, Or, Equivalence
# standard logical equivalences
# (A ∧ B) ≡ (B ∧ A) commutativity of ∧
# (A ∨ B) ≡ (B ∨ A) commutativity of ∨
# ((A ∧ B) ∧ C) ≡ (A ∧ (B ∧ C)) associativity of ∧
# ((A ∨ B) ∨ C) ≡ (A ∨ (B ∨ C)) associativity of ∨
# ¬(¬A) ≡ A double negation elimination


p00 = '(((A ∨ B) → C) ∧ (D ∧ (¬E)))'
# wumpus world
# wumpus and pit axioms
axiom00 = Not.from_prop_var('P00')
axiom01 = Not.from_prop_var('W00')

inds = list(itertools.product([0, 1, 2, 3], [0, 1, 2, 3], repeat=2))
breeze_vars = {}
stench_vars = {}
pit_vars = {}
wumpus_vars = {}
for i, j in breeze_vars:
    b = PropVar('B' + str(i) + str(j))
    s = PropVar('S' + str(i) + str(j))
    p = PropVar('P' + str(i) + str(j))
    w = PropVar('W' + str(i) + str(j))
    breeze_vars[i, j] = b
    stench_vars[i, j] = s
    pit_vars[i, j] = p
    wumpus_vars[i, j] = w

# corners
axiom_b00 = Equivalence(breeze_vars[0, 0], Or(pit_vars[0, 1], pit_vars[1, 0]))
axiom_b03 = Equivalence(breeze_vars[0, 3], Or(pit_vars[0, 2], pit_vars[1, 3]))
axiom_b30 = Equivalence(breeze_vars[3, 0], Or(pit_vars[2, 0], pit_vars[3, 1]))
axiom_b33 = Equivalence(breeze_vars[3, 3], Or(pit_vars[3, 2], pit_vars[2, 3]))

axiom_s00 = Equivalence(stench_vars[0, 0], Or(wumpus_vars[0, 1], wumpus_vars[1, 0]))
axiom_s03 = Equivalence(stench_vars[0, 3], Or(wumpus_vars[0, 2], wumpus_vars[1, 3]))
axiom_s30 = Equivalence(stench_vars[3, 0], Or(wumpus_vars[2, 0], wumpus_vars[3, 1]))
axiom_s33 = Equivalence(stench_vars[3, 3], Or(wumpus_vars[3, 2], wumpus_vars[2, 3]))


