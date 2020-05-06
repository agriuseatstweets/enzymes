from .deduplicate import *

def test_deduplicate():
    tweets = [{'id': 123}, {'id': 345}, {'id': 123}]
    t = deduplicate(lambda x: x['id'], tweets)
    t = list(t)
    assert t == [{'id': 123}, {'id': 345}]
