# Enzymes

Simple utilities for analyzing tweet data.

Mostly lazy. Expect a generator unless it's a reduction of some sort.


## Entities

Entities can be any of:

* hashtags
* user_mentions
* urls
* media

Or any combination of the above.


##### `prep_tweets`

`prep_tweets` prepares tweets for entitiy analysis. It does the following:

* Throws away all information that isn't the entities.
* Removes duplicates.
* Considers the retweeted_status if a tweet is a retweet. It also removes deuplicates (thus, if tweet A is retweeted 20 times in the data, it is only included once here).
* Handles truncation, gets entities from extended_tweets.


``` python
from enzymes.entities import prep_tweets, entity_counts, entity_cooccurrence

# entities.prep_tweets prepares tweets for analyzing entities
dat = prep_tweets(dat)

# calling "list" brings everything into memory, necessary if
# using more than once
dat = list(dat)
```

##### `entity_counts`

Retrieve counts of each unique entity value, can also be used to get unique entity values:

``` python
entity_counts(['urls', 'hashtags'], dat)
# { maga: 2789, who: 93 }
```


##### `entity_cooccurrence`

Create a cooccurrence matrix (`scipy.sparse.dok_matrix`) of the included entities.

``` python

# requires a vocab dictionary, which can be
# created from the `entity_counts`.

counts = entity_counts(['urls', 'hashtags'], dat)
terms = {k for k, v in counts.items() if v > 5}
vocab = {k:i for i,k in enumerate(terms)}

entity_cooccurrence(['urls', 'hashtags'], dat, vocab)
#  <2318x2318 sparse matrix of type '<class 'numpy.float64'>'
#	with 124336 stored elements in Dictionary Of Keys format>
```
