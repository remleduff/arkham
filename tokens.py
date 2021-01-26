#!/usr/bin/env python3
from itertools import combinations
from pprint import pprint
from random import sample
from tabulate import tabulate

ELDERSIGN = 'eldersign'
SKULL = 'skull'
CULTIST = 'cultist'
TABLET = 'tablet'
HEART = 'heart'

TENTACLE = 'tentacle'

BLESSING = 'blessing'
CURSE = 'curse'


# One 'cultist removed for flashback'
# CULTIST,
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
        SKULL,
        SKULL,
        CULTIST,
        TABLET,
        TABLET,
        HEART,
        HEART,
        TENTACLE,
        ELDERSIGN,
        ]

spooky = {
        BLESSING: 2,
        CURSE: -2,
        ELDERSIGN: 1,
        SKULL: -2,
        CULTIST: -2,
        TABLET: -2,
        HEART: -3,
        }

blurses = {BLESSING, CURSE}

def is_blursed(token):
    if isinstance(token, list):
        return BLESSING in token or CURSE in token
    return token == BLESSING or token == CURSE

def blursed(tokens):
    if isinstance(tokens, list):
        if BLESSING in tokens:
            return BLESSING
        if CURSE in tokens:
            return CURSE
    return None


def pull_tokens(bag, n):
    return sample(bag, n)


def modifiers(tokens, ignore={}):
    return [spooky.get(token, token) for token in tokens if not token in ignore]


def is_success(tokens, difficulty):
    if TENTACLE in tokens:
        return False
    return sum(modifiers(tokens)) > difficulty


def jacky_target_difficulty_strat(combo, difficulty=-2, bag=bag):
    outcome = list(combo)

    blurse = blursed(combo)
    m = modifiers(combo, ignore=blurses)
    if TENTACLE in combo:
        # Jacqueline can only cancel the tentacle, which leaves the other two tokens
        outcome.remove(TENTACLE)
    elif m and max(m) > difficulty:
        # We can pass the test, cancel the other tokens
        outcome = [max(m)]
    elif blurse:
        # We can't pass the test, take a blessing or curse, preferring blessings, then resolve
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


def crystal_pendulum():
    vals = {}
    for combo in combos:
        if TENTACLE in combo:
            value = sum(spooky.get(token, token) for token in combo if token != TENTACLE)
            vals[value] = vals.get(value, 0) + 1
            total += 1
        else:
            for value in set(spooky.get(token, token) for token in combo):
                vals[value] = vals.get(value, 0) + 1
                total += 1
    return vals



def monte(strat, bag=bag, trials=1000):
    result = []
    for i in range(trials):
        tokens = pull_tokens(bag, 3)
        outcome = strat(tokens, bag)
        result.append(outcome)
    return result


def count_successes(outcomes, difficulty, trials):
    return sum(is_success(outcome, difficulty) for outcome in outcomes) / trials


def best_pendulum_guess(outcomes, difficulty, trials):
    sail_by = [abs(sum(modifiers(outcome)) - difficulty) for outcome in outcomes if TENTACLE not in outcome]
    return max(set(sail_by), key=sail_by.count)


def run_sim(eval_fn, trials=10000):
    trials = 10000
    results = []
    for difficulty in range(-2, 5):
        strat = lambda tokens, bag: jacky_target_difficulty_strat(tokens, -difficulty, bag)
        for curses in range(11):
            row = [f'{difficulty}({curses})']
            for blessings in range(11):
                outcomes = monte(strat, bag + [BLESSING] * blessings + [CURSE] * curses, trials)
                result = eval_fn(outcomes, difficulty, trials)
                row.append(result)
            results.append(row)
    return results


#results = run_sim(count_successes)
#
#results.sort(key=lambda x: x[1])
#print(tabulate(results, headers=['Difficulty(curses)', '0 blessings', *range(1,11)]))


#print('Most frequent success-by or fail-by value for Pendulum:')
#results = run_sim(best_pendulum_guess)
#print(tabulate(results, headers=['Difficulty(curses)', '0 blessings', *range(1,11)]))


#vals = skill_test()
#probs = {k: v/n for k,v in vals.items()}

#pprint(n)
#pprint(vals)
#pprint(probs)

#x = [BLESSING, -1, -2, CURSE]
#b = resolve_blurse_outcomes(x)
