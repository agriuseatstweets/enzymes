from .preprocess import handle_truncated, handle_extended_mode

ext = {
    "user" : { "screen_name": "max", "id": "foo" },
    "truncated" : True,
    "text" : "foo",
    "entities" : {"hashtags" : [{"text": "foo"}]},
    "extended_tweet" : {
        "full_text" : "foobar",
        "entities" : { "hashtags" : [{"text" : "foo"}, {"text" : "bar"}]}
    }
}

tweet = {
    "user" : { "screen_name": "max", "id": "foo" },
    "truncated" : False,
    "text" : "foo",
    "entities" : {"hashtags" : [{"text": "foo"}]}
}


ext_mode = {
    "truncated" : False,
    "text" : "",
    "full_text": "foo bar"
}


def test_handle_truncated_ext():
    t = handle_truncated(ext)
    assert t['text'] == 'foobar'
    assert len(t['entities']['hashtags']) == 2

def test_handle_truncated_on_simple_tweet():
    t = handle_truncated(tweet)
    assert t['text'] == 'foo'

def test_handle_extended_mode():
    t = handle_extended_mode(ext_mode)
    assert t['text'] == 'foo bar'
