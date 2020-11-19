"""Proposition A.4
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


print(misc.header("Proposition A.4", "*"))

num_cand = 6
a, b, c, d, e, f = list(range(6))  # a = 0, b = 1, c = 2, ...
names = "abcdef"

manipulations = [
    ("sav", 1, [[a, b, c], [d, e]], [a], [[d], [e]], [[a]]),
    (
        "revseqpav",
        2,
        [[a, b, c], [b, d], [c, b], [a, d, e], [b, e]],
        [a],
        [[b, d], [b, e]],
        [[a, b]],
    ),
    (
        "seqphrag",
        2,
        [[0, 1, 2], [0, 1], [1, 5], [2, 4], [1, 4, 5], [1, 3, 5]],
        [2],
        [[1, 5]],
        [[1, 2]],
    ),
    (
        "seqpav",
        3,
        [[0, 1], [1, 3], [2, 5], [0, 1, 5], [1, 5], [1, 2]],
        [0],
        [[1, 2, 5]],
        [[0, 1, 5]],
    ),
    (
        "mav",
        3,
        [[0, 1, 2], [1, 3], [0, 1, 4], [0, 1, 3], [0, 1, 4], [0, 1]],
        [2],
        [[0, 1, 3]],
        [[0, 1, 2]],
    ),
    (
        "pav",
        3,
        [[2, 3, 4], [0, 1], [1, 5], [0, 2, 3], [1, 2, 5], [2, 4, 5]],
        [4],
        [[1, 2, 5]],
        [[1, 2, 4]],
    ),
    (
        "rule-x",
        3,
        [[1, 2, 3], [0, 1], [1, 3], [2, 3], [3, 4], [3, 4]],
        [2],
        [[1, 3, 4]],
        [[1, 2, 3]],
    ),
    ("greedy-monroe", 2, [[0, 1], [0, 2, 5], [0, 2, 3], [4, 5]], [1], [[0, 2]], [[0, 1]]),
    (
        "monroe",
        3,
        [
            [1, 3],
            [0, 1, 2],
            [1, 4],
            [3, 4],
            [4, 5],
            [1, 2, 4],
            [2, 3, 4],
            [1, 2],
            [0, 5],
            [1, 2, 3],
            [0, 5],
            [0, 3],
        ],
        [5],
        [[0, 1, 4]],
        [[1, 3, 5]],
    ),
    (
        "seqcc",
        3,
        [
            [1, 4, 5],
            [0, 1],
            [3, 4, 5],
            [3, 4],
            [1, 5],
            [2, 3],
            [0, 1, 2],
            [0, 2],
            [2, 3],
            [0, 1, 4],
            [0, 4, 5],
            [1, 2, 3],
        ],
        [2],
        [[0, 1, 3]],
        [[1, 2, 4]],
    ),
]

for manip in manipulations:
    rule_id, committeesize, apprsets, modvote, commsfirst, commsafter = manip

    print(misc.header(abcrules.rules[rule_id].longname, "-"))

    profile = Profile(num_cand, names=names)
    profile.add_preferences(apprsets)
    truepref = profile.preferences[0].approved
    print(profile.str_compact())

    # irresolute if possible
    if False in abcrules.rules[rule_id].resolute:
        resolute = False
    else:
        resolute = True

    committees = abcrules.compute(rule_id, profile, committeesize, resolute=resolute)
    print("original winning committees:\n" + misc.str_candsets(committees, names))

    # verify correctness
    assert committees == commsfirst

    print(
        "Manipulation by voter 0: "
        + misc.str_candset(apprsets[0], names)
        + " --> "
        + misc.str_candset(modvote, names)
    )
    if not all(c in truepref for c in modvote):
        print(" (not a subset!)")

    apprsets[0] = modvote
    profile = Profile(num_cand, names=names)
    profile.add_preferences(apprsets)

    committees = abcrules.compute(rule_id, profile, committeesize, resolute=resolute)
    print("\nwinning committees after manipulation:\n" + misc.str_candsets(committees, names))

    # verify correctness
    assert committees == commsafter

    # verify that this is a counterexample to inclusion-strategyproofness
    # with the Kelly (cautious) set extension
    for commfirst in commsfirst:
        for commafter in commsafter:
            for c in set(commfirst) & set(truepref):
                assert c in commafter
            assert set(commfirst) & set(truepref) < set(commafter) & set(truepref)
