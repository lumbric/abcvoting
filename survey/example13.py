"""Example 13 (SAV)
from the survey: "Approval-Based Multi-Winner Voting:
Axioms, Algorithms, and Applications"
by Martin Lackner and Piotr Skowron
"""

from __future__ import print_function
import sys

sys.path.insert(0, "..")
from abcvoting import abcrules
from abcvoting.preferences import Profile
from abcvoting import misc


print(misc.header("Example 13", "*"))

# Approval profile
num_cand = 5
a, b, c, d, e = list(range(5))  # a = 0, b = 1, c = 2, ...
apprsets = [[a]] + [[b, c, d, e]] * 3
names = "abcde"

profile = Profile(num_cand, names=names)
profile.add_preferences(apprsets)

print(misc.header("Input:"))
print(profile.str_compact())

committees = abcrules.compute_sav(profile, 1, verbose=2)


# verify correctness
assert committees == [[a]]
