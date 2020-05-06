from itertools import permutations
from toolz.curried import map, get_in, filter, frequencies
from toolz import pipe
import numpy as np
from scipy.sparse import dok_matrix

from enzymes.preprocessing.collect_content import replace_retweets, \
    handle_truncated, \
    simplify_entities

from enzymes.preprocessing.deduplicate import deduplicate


select_ents = lambda keys: lambda d: [v for k, v in d.items() if k in keys]
uniq = lambda x: list(set(x))

def prep_tweets(tweets):

    pipeline = [map(replace_retweets),
                deduplicate(lambda x: x['id']),
                map(handle_truncated),
                map(simplify_entities),
                map(get_in(['entities']))]


    return pipe(tweets, *pipeline)

def flatten(a):
    for x in a:
        for y in x:
            yield y

def cooccurrence(pairs):
    lookup = {}
    counter = 0

    for pair in pairs:
        for p in pair:
            if p not in lookup:
                lookup[p] = counter
                counter += 1
        a, b = [lookup[p] for p in pair]
        yield (a, b)


def co_matrix(pairs):

    # BRINGS PAIRS INTO MEMORY:
    pairs = list(pairs)

    if len(pairs) == 0:
        raise TypeError('co_matrix was passed data of length 0')

    N = max(list(flatten(pairs))) + 1
    m = dok_matrix((N, N), np.int32)

    for i, j in pairs:
        m[i, j] += 1

    return m


def entity_counts(entities, dat):
    fns = [filter(lambda x: x is not None),
           map(select_ents(entities)),
           map(flatten),
           flatten,
           frequencies]

    return pipe(dat, *fns)


def entity_cooccurrence(entities, dat):
    fns = [filter(lambda x: x is not None),
           map(select_ents(entities)),
           map(flatten),
           map(uniq),
           map(lambda d: permutations(d, 2)),
           flatten,
           cooccurrence,
           co_matrix]

    return pipe(dat, *fns)
