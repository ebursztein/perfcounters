from unittest.loader import VALID_MODULE_NAME
import pytest
from perfcounters import ValueCounters


def test_e2e():
    cnts = ValueCounters()
    cnts.start('a')
    cnts.inc('a', 42)
    assert cnts.get('a') >= 42
    cnts.dec('a', 2)
    assert cnts.get('a') == 40
    cnts.set('a', 2)
    assert cnts.get('a') == 2


def test_laps():
    cnts = ValueCounters()
    cnts.start('a', value=10)
    cnts.lap('a')
    cnts.inc('a', 10)
    assert cnts.get('a') == 20
    assert len(cnts.get_laps('a')) == 2


def test_wrong_get_name():
    with pytest.raises(ValueError):
        cnts = ValueCounters()
        cnts.start('a')
        cnts.get('b')


def test_reset():
    cnts = ValueCounters()
    cnts.start('a', value=32)
    assert cnts.get('a') == 32
    cnts.reset('a')
    assert cnts.get('a') == 0

def test_reset_all():
    cnts = ValueCounters()
    cnts.start('a', value=32)
    cnts.start('b', value=33)
    assert cnts.get('a') == 32
    assert cnts.get('b') == 33

    cnts.reset_all()
    assert cnts.get('a') == 0
    assert cnts.get('b') == 0


def test_report():
    cnts = ValueCounters()
    cnts.start('a', value=32)
    cnts.start('b', value=33)
    assert 'b' in cnts.to_json()
    assert 'b' in cnts.to_html()
    assert 'b' in cnts.to_latex()