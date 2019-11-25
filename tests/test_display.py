import json
from .fixtures import *  # noqa: F401, F403
from perfcounters.report import TIME_COUNTERS, VALUE_COUNTERS, LAPS_COUNTERS


def test_to_json_values(counters):
    js = counters.to_json()
    cnts = json.loads(js)
    assert VALUE_COUNTERS in cnts
    # by default counters are in reverse order
    assert cnts[VALUE_COUNTERS][1][0] == 'value'
    assert cnts[VALUE_COUNTERS][1][1] == 42


def test_to_json_time(counters):
    js = counters.to_json()
    cnts = json.loads(js)
    assert TIME_COUNTERS in cnts
    assert cnts[TIME_COUNTERS][0][0] == 'lap'
    assert cnts[TIME_COUNTERS][1][0] == 'time'


def test_to_json_laps(counters):
    js = counters.to_json()
    cnts = json.loads(js)
    assert LAPS_COUNTERS in cnts
    assert cnts[LAPS_COUNTERS][0]['name'] == 'lap'
    assert len(cnts[LAPS_COUNTERS][0]['laps']) == 2
    min_val = cnts[LAPS_COUNTERS][0]['stats']['min']
    max_val = cnts[LAPS_COUNTERS][0]['stats']['max']
    avg_val = cnts[LAPS_COUNTERS][0]['stats']['average']
    assert min_val <= max_val
    assert min_val >= .2
    assert avg_val >= min_val
    assert avg_val <= max_val


def test_report(counters, capsys):
    counters.report()
    out, _ = capsys.readouterr()

    # headers
    for s in [VALUE_COUNTERS, TIME_COUNTERS, LAPS_COUNTERS]:
        assert "-=[%s]=-" % s in out

    # values
    assert "\n| name   |   value |" in out
    assert "\n|--------+---------|\n| value2 |      43 |\n" in out

    # time
    assert "time2" in out

    # lap
    assert 'lap' in out
    assert 'min' in out
    assert 'stddev' in out
    assert 'lap time' in out


def test_to_html(counters):
    html = counters.to_html()
    # headers
    for s in [VALUE_COUNTERS, TIME_COUNTERS, LAPS_COUNTERS]:
        assert "<h1>%s</h1>" % s in html


# def test_log(counters, caplog):
#     counters.log()
#     txt = caplog.text
#     assert "value:42" in txt
