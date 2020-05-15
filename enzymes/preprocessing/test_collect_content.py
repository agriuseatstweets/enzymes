from .collect_content import *
from .preprocess import handle_truncated


quoted_tweet = {
    "truncated": True,
    "user" : { "screen_name": "max", "id": "foo" },
    "text" : "foo",
    "entities" : {"hashtags" : [{"text": "foo"}]},
    "extended_tweet" : {
        "full_text" : "foobar",
        "entities" : { "hashtags" : [{"text" : "foo"}, {"text" : "bar"}]}
    },
    "quoted_status" : {
        "text": "bar",
        "user" : { "screen_name" : "matt", "nope" : "gone" },
        "created_at" : "Mon Apr 17 13:53:38 +0000 2017",
        "id_str" : "123",
        "entities" : {"hashtags" : [{"text": "foo"}]},
    }
}


quoted_tweet_ext = {
    "truncated": True,
    "user" : { "screen_name": "max", "id": "foo" },
    "text" : "foo",
    "entities" : {"hashtags" : [{"text": "foo"}]},
    "extended_tweet" : {
        "full_text" : "foobar",
        "entities" : { "hashtags" : [{"text" : "foo"}, {"text" : "bar"}]}
    },
    "quoted_status" : {
        "user" : { "screen_name" : "matt", "nope" : "gone" },
        "created_at" : "Mon Apr 17 13:53:38 +0000 2017",
        "truncated" : True,
        "id_str" : "123",
        "entities" : {"hashtags" : [{"text": "foo"}]},
        "extended_tweet" : {
            "full_text" : "foobarbaz",
            "entities" : { "hashtags" : [{"text" : "foo"}, {"text" : "bar"}, {"text" : "qux"}]}
        }
    }
}

retweet_ext = {
    "user" : { "screen_name": "max", "id": "foo" },
    "truncated" : True,
    "text" : "foo",
    "entities" : {"hashtags" : [{"text": "foo"}]},
    "extended_tweet" : {
        "full_text" : "foobar",
        "entities" : { "hashtags" : [{"text" : "foo"}, {"text" : "bar"}]}
    },
    "retweeted_status" : {
        "user" : { "screen_name" : "matt", "nope" : "gone" },
        "truncated" : True,
        "created_at" : "Mon Apr 17 13:53:38 +0000 2017",
        "id_str" : "123",
        "entities" : {"hashtags" : [{"text": "foo"}]},
        "extended_tweet" : {
            "full_text" : "foobarbaz",
            "entities" : { "hashtags" : [{"text" : "foo"}, {"text" : "bar"}, {"text" : "qux"}]}
        }
    }
}

retweet = {
    "user" : { "screen_name": "max", "id": "foo" },
    "truncated" : False,
    "text" : "foo",
    "entities" : {"hashtags" : [{"text": "foo"}]},
    "retweeted_status" : {
        "user" : { "screen_name" : "matt", "nope" : "gone" },
        "truncated" : False,
        "created_at" : "Mon Apr 17 13:53:38 +0000 2017",
        "id_str" : "123",
        "text": "foobar",
        "entities" : {"hashtags" : [{"text": "foo"}, {"text": "bar"}]}
    }
}

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

ext_entities = {
    "user" : { "screen_name": "max", "id": "foo" },
    "truncated" : False,
    "text" : "foo",
    "entities" : {"hashtags": [{"text": "baz"}], "media" : [{"expanded_url": "foo"}]},
    "extended_entities" : {"media" : [{"expanded_url": "foo"}, {"expanded_url": "bar"}]}
}




def test_simplify_entities_on_extended_entities():
    t = simplify_entities(ext_entities)
    assert t['entities']['media'] == ['foo', 'bar']
    assert t['entities']['hashtags'] == ['baz']

def test_simplify_entities_reg_tweet():
    t = simplify_entities(tweet)
    assert t['entities']['hashtags'] == ['foo']

def test_replace_retweets_rt():
    t = replace_retweets(retweet)
    t = handle_truncated(t)
    t = simplify_entities(t)
    assert t['entities']['hashtags'] == ['foo', 'bar']
    assert t['text'] == 'foobar'

def test_replace_retweets_extended_rt():
    t = replace_retweets(retweet_ext)
    t = handle_truncated(t)
    t = simplify_entities(t)
    assert t['entities']['hashtags'] == ['foo', 'bar', 'qux']
    assert t['text'] == 'foobarbaz'

def test_collect_retweeted_by():
    retweets = [{'id': 'foo', 'ag_retweeted_by': [123]},
                {'id': 'foo', 'ag_retweeted_by': [245]},
                {'id': 'bar', 'ag_retweeted_by': [123]}]


    assert collect_retweeted_by(retweets) == {'foo': [123, 245], 'bar': [123]}
