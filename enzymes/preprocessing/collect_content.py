from copy import copy
from toolz import get_in, assoc_in, reduceby

def _set_from(tweet, dest, from_):
    return assoc_in(tweet, dest, get_in(from_, tweet))

def _extract_entity(tweet, from_, get_out, root_from, root_to='entities'):
    li = get_in([root_from, from_], tweet)
    if not li:
        return tweet

    extracted = [h[get_out] for h in li]

    if not tweet[root_to]:
        tweet[root_to] = {}

    tweet = assoc_in(tweet, [root_to, from_], extracted)

    return tweet

def simplify_entities(tweet):
    li = [('user_mentions', 'screen_name', 'entities'),
          ('hashtags', 'text', 'entities'),
          ('urls', 'expanded_url', 'entities'),
          ('media', 'expanded_url', 'entities'),
          ('media', 'expanded_url', 'extended_entities')]

    for a, b, r in li:
        tweet = _extract_entity(tweet, a, b, r)

    return tweet

def handle_truncated(tweet):
    truncated = get_in(['truncated'], tweet)
    if truncated:
        tweet = _set_from(tweet, ['entities'], ['extended_tweet', 'entities'])
        tweet = _set_from(tweet, ['text'], ['extended_tweet', 'full_text'])
    return tweet

def replace_retweets(tweet):
    if tweet.get('retweeted_status'):
        rt = tweet['retweeted_status']
        rt['ag_retweeted_by'] = [tweet['user']['id']]
        tweet = rt
    return tweet

def collect_retweeted_by(tweets):
    return reduceby(lambda x: x['id'],
                    lambda acc, t: acc + t['ag_retweeted_by'],
                    tweets,
                    [])
