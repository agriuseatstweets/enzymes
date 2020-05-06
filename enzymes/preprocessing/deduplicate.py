from toolz import curry

@curry
def deduplicate(key, dat):
    ids = set()
    for d in dat:
        i = key(d)
        if i not in ids:
            ids.add(i)
            yield d
