from copy import deepcopy

from pandagg.node.query.compound import Bool
from pandagg.node.query.full_text import Match
from pandagg.search import Search


from unittest import TestCase

from pandagg.tree.aggs import Aggs
from pandagg.tree.query import Query


class SearchTestCase(TestCase):
    def test_expand__to_dot_is_respected(self):
        s = Search().query("match", a__b=42, _expand__to_dot=False)

        self.assertEqual({"query": {"match": {"a__b": {"query": 42}}}}, s.to_dict())

    def test_search_query_combines_query(self):
        s = Search()

        s2 = s.query("match", f=42)
        self.assertEqual(s2._query.to_dict(), Query(Match(f=42)).to_dict())
        self.assertEqual(s._query.to_dict(), None)

        s3 = s2.query("match", f=43)
        self.assertEqual(s2._query.to_dict(), Query(Match(f=42)).to_dict())
        self.assertEqual(
            s3._query.to_dict(), Query(Bool(must=[Match(f=42), Match(f=43)])).to_dict()
        )

    def test_using(self):
        o = object()
        o2 = object()
        s = Search(using=o)
        self.assertIs(s._using, o)
        s2 = s.using(o2)
        self.assertIs(s._using, o)
        self.assertIs(s2._using, o2)

    def test_query_always_returns_search(self):
        s = Search()
        self.assertIsInstance(s.query("match", f=42), Search)

    def test_source_copied_on_clone(self):
        s = Search().source(False)

        self.assertEqual(s._clone()._source, s._source)
        self.assertIs(s._clone()._source, False)

        s2 = Search().source([])
        assert s2._clone()._source == s2._source
        assert s2._source == []

        s3 = Search().source(["some", "fields"])
        assert s3._clone()._source == s3._source
        assert s3._clone()._source == ["some", "fields"]

    def test_copy_clones(self):
        from copy import copy

        s1 = Search().source(["some", "fields"])
        s2 = copy(s1)

        assert s1 == s2
        assert s1 is not s2

    def test_aggs_allow_two_metric(self):
        s = Search()

        s = s.aggs([Aggs("max", name="a", field="a"), Aggs("max", name="b", field="b")])

        self.assertEqual(s.to_dict(),{
            "aggs": {"a": {"max": {"field": "a"}}, "b": {"max": {"field": "b"}}}
        })

    def test_aggs_get_copied_on_change(self):
        s = Search().query("match_all")
        s.aggs.bucket("per_tag", "terms", field="f").metric(
            "max_score", "max", field="score"
        )

        s2 = s.query("match_all")
        s2.aggs.bucket("per_month", "date_histogram", field="date", interval="month")
        s3 = s2.query("match_all")
        s3.aggs["per_month"].metric("max_score", "max", field="score")
        s4 = s3._clone()
        s4.aggs.metric("max_score", "max", field="score")

        d = {
            "query": {"match_all": {}},
            "aggs": {
                "per_tag": {
                    "terms": {"field": "f"},
                    "aggs": {"max_score": {"max": {"field": "score"}}},
                }
            },
        }

        assert d == s.to_dict()
        d["aggs"]["per_month"] = {
            "date_histogram": {"field": "date", "interval": "month"}
        }
        assert d == s2.to_dict()
        d["aggs"]["per_month"]["aggs"] = {"max_score": {"max": {"field": "score"}}}
        assert d == s3.to_dict()
        d["aggs"]["max_score"] = {"max": {"field": "score"}}
        assert d == s4.to_dict()

    def test_search_index(self):
        s = Search(index="i")
        assert s._index == ["i"]
        s = s.index("i2")
        assert s._index == ["i", "i2"]
        s = s.index(u"i3")
        assert s._index == ["i", "i2", "i3"]
        s = s.index()
        assert s._index is None
        s = Search(index=("i", "i2"))
        assert s._index == ["i", "i2"]
        s = Search(index=["i", "i2"])
        assert s._index == ["i", "i2"]
        s = Search()
        s = s.index("i", "i2")
        assert s._index == ["i", "i2"]
        s2 = s.index("i3")
        assert s._index == ["i", "i2"]
        assert s2._index == ["i", "i2", "i3"]
        s = Search()
        s = s.index(["i", "i2"], "i3")
        assert s._index == ["i", "i2", "i3"]
        s2 = s.index("i4")
        assert s._index == ["i", "i2", "i3"]
        assert s2._index == ["i", "i2", "i3", "i4"]
        s2 = s.index(["i4"])
        assert s2._index == ["i", "i2", "i3", "i4"]
        s2 = s.index(("i4", "i5"))
        assert s2._index == ["i", "i2", "i3", "i4", "i5"]

    def test_sort(self):
        s = Search()
        s = s.sort("fielda", "-fieldb")

        assert ["fielda", {"fieldb": {"order": "desc"}}] == s._sort
        assert {"sort": ["fielda", {"fieldb": {"order": "desc"}}]} == s.to_dict()

        s = s.sort()
        assert [] == s._sort
        assert Search().to_dict() == s.to_dict()

    def test_slice(self):
        s = Search()
        assert {"from": 3, "size": 7} == s[3:10].to_dict()
        assert {"from": 0, "size": 5} == s[:5].to_dict()
        assert {"from": 3, "size": 10} == s[3:].to_dict()
        assert {"from": 0, "size": 0} == s[0:0].to_dict()

    def test_index(self):
        s = Search()
        assert {"from": 3, "size": 1} == s[3].to_dict()

    def test_search_to_dict(self):
        s = Search()
        assert {} == s.to_dict()

        s = s.query("match", f=42)
        assert {"query": {"match": {"f": {"query": 42}}}} == s.to_dict()

        assert {"query": {"match": {"f":{"query": 42}}}, "size": 10} == s.to_dict(size=10)

        s = s.aggs("terms", name="per_tag", field="f").aggs(
            "max", name="max_score", field="score"
        )
        d = {
            "aggs": {
                "per_tag": {
                    "terms": {"field": "f"},
                    "aggs": {"max_score": {"max": {"field": "score"}}},
                }
            },
            "query": {"match": {"f": {"query": 42}}},
        }
        self.assertEqual(d, s.to_dict())

        s = Search().params(size=5)
        assert {"size": 5} == s.to_dict()
        s = s.params(from_=42)
        assert {"size": 5, "from": 42} == s.to_dict()

    def test_complex_example(self):
        s = Search()
        s = (
            s.query("match", title="python")
            .must_not("match", title="ruby")
            .should(
                Query("term", category="meetup"), Query("term", category="conference")
            )
            .post_filter("terms", tags=["prague", "czech"])
            .script_fields(more_attendees="doc['attendees'].value + 42")
        )

        s.aggs("terms", name="per_country", field="country").aggs(
            "avg_attendees", "avg", field="attendees"
        )

        s.bool(minimum_should_match=2)

        s = s.highlight_options(order="score").highlight(
            "title", "body", fragment_size=50
        )

        assert {
            "query": {
                "bool": {
                    "filter": [
                        {
                            "bool": {
                                "should": [
                                    {"term": {"category": "meetup"}},
                                    {"term": {"category": "conference"}},
                                ]
                            }
                        }
                    ],
                    "must": [{"match": {"title": "python"}}],
                    "must_not": [{"match": {"title": "ruby"}}],
                    "minimum_should_match": 2,
                }
            },
            "post_filter": {"terms": {"tags": ["prague", "czech"]}},
            "aggs": {
                "per_country": {
                    "terms": {"field": "country"},
                    "aggs": {"avg_attendees": {"avg": {"field": "attendees"}}},
                }
            },
            "highlight": {
                "order": "score",
                "fields": {
                    "title": {"fragment_size": 50},
                    "body": {"fragment_size": 50},
                },
            },
            "script_fields": {
                "more_attendees": {"script": "doc['attendees'].value + 42"}
            },
        } == s.to_dict()

    def test_reverse(self):
        d = {'aggs': {'per_country': {'aggs': {'avg_attendees': {'avg': {'field': 'attendees'}}},
                                      'terms': {'field': 'country'}}},
             'highlight': {'fields': {'title': {'fragment_size': 50}}, 'order': 'score'},
             'post_filter': {'bool': {'must': [{'terms': {'tags': ['prague', 'czech']}}]}},
             'query': {'bool': {'filter': [{'bool': {'should': [{'term': {'category': {'value': 'meetup'}}},
                                                                {'term': {'category': {'value': 'conference'}}}]}}],
                                'must': [{'bool': {'minimum_should_match': 2,
                                                   'must': [{'match': {'title': {'query': 'python'}}}],
                                                   'must_not': [{'match': {'title': {'query': 'ruby'}}}]}}]}},
             'script_fields': {'more_attendees': {'script': "doc['attendees'].value + 42"}},
             'size': 5,
             'sort': ['title', {'category': {'order': 'desc'}}, '_score'],
             'suggest': {'my-title-suggestions-1': {'term': {'field': 'title', 'size': 3},
                                                    'text': 'devloping distibutd saerch '
                                                            'engies'}}}

        d2 = deepcopy(d)

        s = Search.from_dict(d)

        # make sure we haven't modified anything in place
        self.assertEqual(d, d2)
        self.assertEqual(d, s.to_dict())

    def test_from_dict_doesnt_need_query(self):
        s = Search.from_dict({"size": 5})

        assert {"size": 5} == s.to_dict()

    def test_params_being_passed_to_search(self, mock_client):
        s = Search(using="mock")
        s = s.params(routing="42")
        s.execute()

        mock_client.search.assert_called_once_with(index=None, body={}, routing="42")

    def test_source(self):
        assert {} == Search().source().to_dict()

        assert {
            "_source": {"includes": ["foo.bar.*"], "excludes": ["foo.one"]}
        } == Search().source(includes=["foo.bar.*"], excludes=["foo.one"]).to_dict()

        assert {"_source": False} == Search().source(False).to_dict()

        assert {"_source": ["f1", "f2"]} == Search().source(
            includes=["foo.bar.*"], excludes=["foo.one"]
        ).source(["f1", "f2"]).to_dict()

    def test_source_on_clone(self):
        self.assertEqual(
            {
                "_source": {"includes": ["foo.bar.*"], "excludes": ["foo.one"]},
                "query": {"bool": {"filter": [{"term": {"title": {"value": "python"}}}],}},
            },
            Search()
            .source(includes=["foo.bar.*"])
            .source(excludes=["foo.one"])
            .filter("term", title="python")
            .to_dict(),
        )
        assert {
            "_source": False,
            "query": {"bool": {"filter": [{"term": {"title": "python"}}],}},
        } == Search().source(False).filter("term", title="python").to_dict()

    def test_source_on_clear(self):
        assert (
            {}
            == Search()
            .source(includes=["foo.bar.*"])
            .source(includes=None, excludes=None)
            .to_dict()
        )

    def test_suggest_accepts_global_text(self):
        s = Search.from_dict(
            {
                "suggest": {
                    "text": "the amsterdma meetpu",
                    "my-suggest-1": {"term": {"field": "title"}},
                    "my-suggest-2": {"text": "other", "term": {"field": "body"}},
                }
            }
        )

        assert {
            "suggest": {
                "my-suggest-1": {
                    "term": {"field": "title"},
                    "text": "the amsterdma meetpu",
                },
                "my-suggest-2": {"term": {"field": "body"}, "text": "other"},
            }
        } == s.to_dict()

    def test_suggest(self):
        s = Search()
        s = s.suggest("my_suggestion", "pyhton", term={"field": "title"})

        assert {
            "suggest": {"my_suggestion": {"term": {"field": "title"}, "text": "pyhton"}}
        } == s.to_dict()

    def test_exclude(self):
        s = Search()
        s = s.exclude("match", title="python")

        self.assertEqual(
            {
                "query": {
                    "bool": {
                        "filter": [
                            {
                                "bool": {
                                    "must_not": [
                                        {"match": {"title": {"query": "python"}}}
                                    ]
                                }
                            }
                        ]
                    }
                }
            },
            s.to_dict(),
        )

    def test_delete_by_query(self, mock_client):
        s = Search(using="mock").query("match", lang="java")
        s.delete()

        mock_client.delete_by_query.assert_called_once_with(
            index=None, body={"query": {"match": {"lang": "java"}}}
        )

    def test_update_from_dict(self):
        s = Search()
        s.update_from_dict({"indices_boost": [{"important-documents": 2}]})
        s.update_from_dict({"_source": ["id", "name"]})

        assert {
            "indices_boost": [{"important-documents": 2}],
            "_source": ["id", "name"],
        } == s.to_dict()
