from toolz import curry

def remove_elements(string, indices):
    prev = 0
    out = ''
    for tok, (start, end) in indices:
        out += string[prev:start]
        out += tok
        prev = end
    return out + string[prev:]

@curry
def sanitize_entities(entities, tweet):
    """Removes entities from text of tweet, optionally adding token

    :param entities: list of strings or list of tuples
                     if tuples, second element is token to replace
                     the entity.
    :param tweet: tweet dictionary
    :returns: tweet dictionary

    Examples
    --------
    >>> sanitize_entities(['urls'], tweet)
    >>> sanitize_entities([('urls', '[URL]')], tweet)
    """

    if isinstance(entities[0], str):
        entities = [(e, '') for e in entities]

    valid_entities = {'hashtags', 'urls', 'user_mentions', 'symbols', 'media'}

    for ent, _ in entities:
        if ent not in valid_entities:
            raise Exception(f'The following entity is not valid: {ent}')

    indices = [(tok, u['indices']) for ent, tok in entities
               for u in tweet['entities'].get(ent, [])]

    indices = sorted(indices, key=lambda x: x[1][0])
    text = remove_elements(tweet['text'], indices)

    # clean up whitespace from ends
    text = text.strip()
    return {**tweet, 'text': text}
