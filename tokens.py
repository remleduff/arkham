#!/usr/bin/env python3
from random import sample

ELDERSIGN = 'eldersign'
SKULL = 'skull'
CULTIST = 'cultist'
TABLET = 'tablet'
HEART = 'heart'

TENTACLE = 'tentacle'

BLESSING = 'blessing'
CURSE = 'curse'


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

def modifiers(tokens, ignore={}):
    return [spooky.get(token, token) for token in tokens if not token in ignore]


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
    tokens = sample(bag, n)
    remaining = list(bag)
    for token in tokens:
        remaining.remove(token)
    return tokens, remaining


def is_success(tokens, difficulty):
    if TENTACLE in tokens:
        return False
    return sum(modifiers(tokens)) > difficulty


def monte(strat, bag=bag, trials=10000, **kwargs):
    outcomes = []
    for i in range(trials):
        outcome = strat(bag, **kwargs)
        outcomes.append(outcome)
    return outcomes 


def success_probability(outcomes, difficulty, trials=10000):
    return sum(is_success(outcome, difficulty) for outcome in outcomes) / trials


def best_pendulum_guess(outcomes, difficulty, trials=10000):
    success_or_fail_by = [abs(sum(modifiers(outcome)) - difficulty) for outcome in outcomes if TENTACLE not in outcome]
    return max(set(success_or_fail_by), key=success_or_fail_by.count)


def null_eval(outcomes, **kwargs):
    return outcomes


def default_strategy(bag, **kwargs):
    tokens, remaining = pull_tokens(bag, 1)
    outcome = tokens

    while blursed(tokens):
        tokens, remaining = pull_tokens(remaining, 1)
        for token in tokens:
            outcome.append(token)
    return outcome


def run_sim(eval_fn=null_eval, strat=default_strategy, **kwargs):
    results = [[None for blessing in range(11)] for curse in range(11)]
    for curses in range(11):
        for blessings in range(11):
            outcomes = monte(strat, bag + [BLESSING] * blessings + [CURSE] * curses, **kwargs)
            results[curses][blessings] = eval_fn(outcomes, **kwargs)
    return results

#run_sim(success_probability, difficulty=-2)
