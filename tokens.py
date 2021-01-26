#!/usr/bin/env python3
from itertools import combinations
from pprint import pprint
from random import sample
from tabulate import tabulate

# One 'cultist removed for flashback'
# 'cultist',
bag = [
        0,
        -1,
        -1,
        -2,
        -2,
        -3,
        -3,
        -4,
        -4,
        -5,
        -6,
        -8,
        'skull',
        'skull',
        'cultist',
        'tablet',
        'tablet',
        'heart',
        'heart',
        'tentacle',
        'eldersign',
        ]

spooky = {
        'blessing': 2,
        'curse': -2,
        'eldersign': 1,
        'skull': -2,
        'cultist': -2,
        'tablet': -2,
        'heart': -3,
        }

blurses = {'blessing', 'curse'}

#c = combinations([spooky.get(token, token) for token in bag if token != 'tentacle'], 3)
combos = list(combinations(bag, 3))

total = 0
n = len(combos)

def is_blursed(token):
    if isinstance(token, list):
        return 'blessing' in token or 'curse' in token
    return token == 'blessing' or token == 'curse'

def crystal_pendulum():
    vals = {}
    for combo in combos:
        if 'tentacle' in combo:
            value = sum(spooky.get(token, token) for token in combo if token != 'tentacle')
            vals[value] = vals.get(value, 0) + 1
            total += 1
        else:
            for value in set(spooky.get(token, token) for token in combo):
                vals[value] = vals.get(value, 0) + 1
                total += 1
    return vals


def resolve_blurse_outcomes(combo, resolved=[]):
    c = list(combo)
    t = list(bag)
    for token in resolved:
        t.remove(token)
    for token in combo:
        t.remove(token)
        if not is_blursed(token):
            c.remove(token)
            resolved.append(token)

    if not c or not is_blursed(c):
        return [c + resolved]

    print(f'{c}')

    r = []
    if 'blessing' in c:
        c.remove('blessing')
        r += [resolve_blurse_outcomes(c + [token], resolved + ['blessing']) for token in t]

    if 'curse' in c:
        c.remove('curse')
        r += [resolve_blurse_outcomes(c + [token], resolved + ['curse']) for token in t]

    return r


def skill_test_odds(target=-2):
    vals = {}
    for c in combos:
        combo = list(c)

        cancelled = False
        outcomes = []

        modifiers = set(spooky.get(token, token) for token in combo if not is_blursed(token) and not token == 'tentacle')

        if 'tentacle' in combo:
            combo.remove('tentacle')
            outcomes.append(combo)
        elif max(modifiers) > target:
            outcomes.append([max(modifiers)])
        elif is_blursed(combo):
            if 'blessing' in combo:
                combo.remove('blessing')
                outcomes.extend(resolve_blurse_outcomes(['blessing'], combo))
            else:
                combo.remove('curse')
                outcomes.extend(resolve_blurse_outcomes(['curse'], combo))


        #for outcome in outcomes:
        #    value = sum(spooky.get(token, token) for token in outcome)
        #    vals[value] = vals.get(value, 0) + 1
    return vals


def blursed(tokens):
    if isinstance(tokens, list):
        if 'blessing' in tokens:
            return 'blessing'
        if 'curse' in tokens:
            return 'curse'
    return None


def pull_tokens(bag, n):
    return sample(bag, n)


def modifiers(tokens, ignore={}):
    return [spooky.get(token, token) for token in tokens if not token in ignore]

def jacky_target_difficulty_strat(combo, difficulty=-2, bag=bag):
    outcome = list(combo)

    blurse = blursed(combo)
    if 'tentacle' in combo:
        outcome.remove('tentacle')
    elif (m := modifiers(combo, ignore=blurses)) and max(m) > difficulty:
        outcome = [max(m)]
    elif blurse:
        remaining = list(bag)
        for token in combo:
            remaining.remove(token)

        outcome = [blurse]
        tokens = [blurse]
        while blursed(tokens):
            tokens = pull_tokens(remaining, 1)
            for token in tokens:
                remaining.remove(token)
                outcome.append(token)
    return outcome


def is_success(tokens, difficulty):
    if 'tentacle' in tokens:
        return False
    return sum(modifiers(tokens)) > difficulty


def monte(bag=bag, difficulty=-2, trials=1000):
    result = []
    successes = 0
    for i in range(trials):
        tokens = pull_tokens(bag, 3)
        outcome = jacky_target_difficulty_strat(tokens, difficulty, bag)
        result.append(outcome)
        #if i % 100:
        #    print(f'{tokens} - {difficulty} {curses} {blessings} - {outcome} {is_success(outcome, difficulty)}')
        if is_success(outcome, difficulty):
            successes += 1
    return successes


trials = 10000
results = []
for difficulty in range(-2, 5):
    for curses in range(0, 10):
        row = [f'{difficulty}({curses})']
        for blessings in range(11):
            successes = monte(bag + ['blessing'] * blessings + ['curse'] * curses, -difficulty, trials)
            row.append(successes / trials)
        results.append(row)


results.sort(key=lambda x: x[1])
print(tabulate(results, headers=['Difficulty(curses)', '0 blessings', *range(1,11)]))



#vals = skill_test()
#probs = {k: v/n for k,v in vals.items()}

#pprint(n)
#pprint(vals)
#pprint(probs)

#x = ['blessing', -1, -2, 'curse']
#b = resolve_blurse_outcomes(x)
