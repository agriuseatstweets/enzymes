import json
from .text import sanitize_entities, remove_elements
from .preprocessing.collect_content import handle_truncated

def open_tweet(path):
    with open(path) as f:
        return json.loads(f.read())

def test_remove_elements():
    string = 'foo bar baz qux'
    indices = [('', (4,7)), ('', (12, 15))]
    text = remove_elements(string, indices)
    assert text == 'foo  baz '

def test_remove_elements_tokens():
    string = 'foo bar baz qux'
    indices = [('[WHAT]', (4,7)), ('[YEAH]', (12, 15))]
    text = remove_elements(string, indices)
    assert text == 'foo [WHAT] baz [YEAH]'

def test_sanitize_urls():
    tweet = open_tweet('test/url_test.json')
    tweet = sanitize_entities(['urls'], tweet)
    assert tweet['text'] == 'You love what’s traditional, reliable, and set in stone. Howev... More for Capricorn'


def test_sanitize_urls_tokens():
    tweet = open_tweet('test/url_test.json')
    tweet = sanitize_entities([('urls', '[URL]')], tweet)
    assert tweet['text'] == 'You love what’s traditional, reliable, and set in stone. Howev... More for Capricorn [URL]'

def test_sanitize_urls_and_media():
    tweet = open_tweet('test/multi_url_test.json')
    tweet = handle_truncated(tweet)
    tweet = sanitize_entities(['urls', 'media'], tweet)

    assert tweet['text'] == """The Story of Pop Singer Pink: \n\nHere's some great Family conversations for the Dinner Table about #Pink. \n\nTalking points Kids will love on: \n- Self-Confidence\n- Conflict Management\n#AMillionDreams"""


def test_sanitize_urls_and_media_and_hashtags():
    tweet = open_tweet('test/multi_url_test.json')
    tweet = handle_truncated(tweet)
    tweet = sanitize_entities(['urls', 'media', 'hashtags'], tweet)

    # NOTE: The space before "."
    assert tweet['text'] == """The Story of Pop Singer Pink: \n\nHere's some great Family conversations for the Dinner Table about . \n\nTalking points Kids will love on: \n- Self-Confidence\n- Conflict Management"""


def test_sanitize_urls_and_media_and_hashtags():
    tweet = open_tweet('test/multi_url_test.json')
    tweet = handle_truncated(tweet)
    tweet = sanitize_entities([('urls', '[URL]'),
                               ('media', '[MEDIA]'),
                               ('hashtags', '[HASHTAG]')], tweet)

    assert tweet['text'] == """The Story of Pop Singer Pink: [URL]\n\nHere's some great Family conversations for the Dinner Table about [HASHTAG]. \n\nTalking points Kids will love on: \n- Self-Confidence\n- Conflict Management\n[HASHTAG] [MEDIA]"""
