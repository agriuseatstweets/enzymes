from functools import partial
from toolz.curried import filter
from toolz import unique, get_in, assoc_in


only_tweets = filter(lambda d: d.get('created_at'))
deduplicate = partial(unique, key=lambda x: x['id'])

def handle_extended_mode(tweet):
    return {**tweet, 'text': tweet['full_text']}


def _set_from(tweet, dest, from_):
    return assoc_in(tweet, dest, get_in(from_, tweet))

def handle_truncated(tweet):
    truncated = get_in(['truncated'], tweet)
    if truncated:
        tweet = _set_from(tweet, ['entities'], ['extended_tweet', 'entities'])
        tweet = _set_from(tweet, ['text'], ['extended_tweet', 'full_text'])
    return tweet
