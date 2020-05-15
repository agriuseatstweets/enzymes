from itertools import permutations
from toolz.curried import map, get_in, filter, frequencies
from toolz import pipe, unique
from functools import partial
import numpy as np
from scipy.sparse import dok_matrix

from .preprocessing.collect_content import replace_retweets, \
    handle_truncated, \
    simplify_entities, \
    deduplicate

from .preprocessing.preprocess import handle_truncated


select_ents = lambda keys: lambda d: [v for k, v in d.items() if k in keys]
uniq = lambda x: list(set(x))


def flatten(a):
    for x in a:
        for y in x:
            yield y


def encode_tuples(vocab, tuples):
    for t in tuples:
        try:
            enc = [vocab[p] for p in t]
            yield tuple(enc)
        except KeyError:
            pass


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


def prep_tweets(tweets):
    """Prepares tweets for entity analysis

    This function treets retweets as tweets and
    removes all duplicates. Thus, if tweet A
    is retweeted 10 times in the corpus,
    it will only show up once in the
    tweets returned by prep_tweets.

    :param tweets: iterator of tweets
    :returns: generator of entities

    >>> raw_tweets = [{'id': 2345, 'entities': [], ...}
    >>>               {'id': 9874, 'entities': [], ...}]
    >>>
    >>> tweets = prep_tweets(raw_tweets)
    """

    pipeline = [map(replace_retweets),
                deduplicate,
                map(handle_truncated),
                map(simplify_entities),
                map(get_in(['entities']))]

    return pipe(tweets, *pipeline)


def entity_counts(entities, tweets):
    """Counts entity occurence in tweets

    :param entities: list of entity types to include
    :param tweets: iterator of tweets from `prep_tweets`
    :returns: dictionary of entity values and counts

    >>> tweets = prep_tweets(tweets)
    >>> entity_counts(['urls', 'hashtags'], tweets)

    """

    fns = [filter(lambda x: x is not None),
           map(select_ents(entities)),
           map(flatten),
           flatten,
           frequencies]

    return pipe(tweets, *fns)


def entity_cooccurrence(entities, tweets, vocab):
    """Creates a cooccurrence matrix of entities in tweets

    :param entities: List of entity types to include
    :param tweets: Iterator of tweets
    :param vocab: Dictionary mapping terms to index
    :returns: A sparse matrix with the occurrences

    >>> # requires a vocab dictionary, which can be
    >>> # created from the `entity_counts`.
    >>>
    >>> tweets = prep_tweets(tweets)
    >>>
    >>> counts = entity_counts(['urls', 'hashtags'], tweets)
    >>> terms = {k for k, v in counts.items() if v > 5}
    >>> vocab = {k:i for i,k in enumerate(terms)}
    >>>
    >>> entity_cooccurrence(['urls', 'hashtags'], tweets, vocab)

    """

    fns = [filter(lambda x: x is not None),
           map(select_ents(entities)),
           map(flatten),
           map(uniq),
           map(lambda l: [x for x in l if x in vocab]),
           map(lambda d: permutations(d, 2)),
           flatten,
           partial(encode_tuples, vocab),
           co_matrix]

    return pipe(tweets, *fns)
