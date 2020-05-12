from functools import partial
from toolz.curried import filter
from toolz import unique

only_tweets = filter(lambda d: d.get('created_at'))
deduplicate = partial(unique, key=lambda x: x['id'])
