"""
Performance counters library
"""
from __future__ import absolute_import

import time
from collections import defaultdict
import logging

from .report import VALUE, TIME, LAP
from . import display

__version__ = '2.0.0'
__author__ = 'Elie Bursztein (code@elie.net)'


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PerfCounters():
    """
    Manage a set of performance counters
    """

    def __init__(self, prefix=None):
        """Init a new set of counters.

        Args
            prefix (str, optional): prefix automatically appended to counters.
        """
        self.counters = defaultdict(dict)
        self.laps = defaultdict(list)
        self.prefix = prefix

    def __len__(self):
        return len(self.counters)

    def lap(self, name):
        """Record a lap for a given counter

        Args:
            name (str): counter name.
        """
        prefixed_name = self._prefix_counter(name)
        if name not in self.counters:
            self.start(name)
        self.laps[prefixed_name].append(time.time())
        self.counters[prefixed_name]['type'] = LAP

    def get(self, name):
        """Return the value of a given counter

        Args:
            name (str): Counter name.

        Returns:
            (int): Counter value
        """

        name = self._prefix_counter(name)
        if name not in self.counters:
            return None
        data = self.counters[name]
        if data['type'] in [TIME, LAP]:
            if 'stop' not in data:
                return time.time() - data['start']
            else:
                return data['stop'] - data['start']
        else:
            return data['value']

    def merge(self, counters):
        """Merge a set of counters generated elsewhere.

        Args:
            counters (PerfCounters): PerfCounters object
        """

        # need to do manual merge to check if there is a dup.
        # We don't need to check laps dups because laps always have a counter.
        for name, data in counters.counters.items():
            if name in self.counters:
                raise ValueError('Duplicate counter name:', name)
            else:
                self.counters[name] = data
                self.laps[name] = counters.laps[name]

    def set(self, name, value=1):
        """Set a value counter to a given values. Create it if needed.

        Args:
            name (str): counter name.
            value (int, optional): Defaults to 1. Counter value.
        """

        name = self._prefix_counter(name)
        self.counters[name]['value'] = value
        self.counters[name]['type'] = VALUE

    def increment(self, name, value=1):
        """
        Increment a value counter by the given value.

        Args:
            name (str): Counter name. Counter will be created if needed.
            value (int, optional): Defaults to 1. Value to increment by.
        """

        name = self._prefix_counter(name)
        if name in self.counters:
            self.counters[name]['value'] += value
        else:
            self.set(name, value=value)

    def start(self, name, warning_deadline=0, log=False):
        """ Create a new time counter.

        Args:
            name (str): counter name.
            warning_deadline (int, optional): log a warning if the counter
            exceed deadline.
            log(Bool, optional): log an info entry that counter started.
        """
        name = self._prefix_counter(name)
        if name in self.counters:
            raise ValueError("Timing counter exist. Counter name:", name)
        else:
            self.counters[name] = {}
            self.counters[name]['start'] = time.time()
            self.counters[name]['type'] = TIME

        if warning_deadline:
            self.counters[name]['warning_deadline'] = warning_deadline

        if log:
            logger.info("%s counter started", name)

    def stop(self, name, log=False):
        """ Stop a given time counter.

        Args:
            name (str): counter name.
            log (bool, optional): add info log entry with time elapsed.
        """
        name = self._prefix_counter(name)
        if name in self.counters:
            self.counters[name]['stop'] = time.time()
        else:
            error_msg = "counter '%s' stopped before being created" % name
            logger.error(error_msg)
            raise ValueError(error_msg)

        if log:
            delta = self.counters[name]['stop'] - self.counters[name]['start']
            logger.info("%s counter stopped - elapsed:%s" % (name, delta))

        if 'warning_deadline' in self.counters[name]:
            diff = self.counters[name]['stop'] - self.counters[name]['start']
            if diff > self.counters[name]['warning_deadline']:
                logger.warning("counter %s deadline exceeded. Operation took:\
                               %s secs. Deadline was: %s secs", name, diff,
                               self.counters[name]['warning_deadline'])

    def stop_all(self):
        """ Stop all time counters."""
        for name, data in self.counters.items():
            # TODO add test for stop all for LAP
            if self.counters[name]['type'] in [TIME, LAP]:
                if 'stop' not in data:
                    self.stop(name)

    def _prefix_counter(self, name):
        """Prefix counter if needed.

        Args:
            name (str): counter name.
        """

        if self.prefix:
            return "%s_%s" % (self.prefix, name)
        else:
            return name

    def report(self, sort_by='value', reverse=True):
        """Print counters in stdout as nicely formated tables.

        Args:
            sort_by (str, optional): How to sort the counters. Valid values
            are {value, name}. Defaults to 'value'.
            reverse (bool, optional): Reverse the sorting. Defaults to True.
        """
        display.report(self.counters, self.laps, sort_by, reverse)

    def to_text(self, sort_by='value', reverse=True):
        """Return counters data in a text format.

        Args:
            sort_by (str, optional): How to sort the counters.
            Defaults to 'value'.
            reverse (bool, optional): Reverse the sorting. Defaults to True.
        """
        return display.to_text(self.counters, self.laps, sort_by,
                               reverse)

    def to_grepable_text(self, sort_by='value', reverse=True):
        """Return counters data in a grepable text format.

        Args:
            sort_by (str, optional): How to sort the counters.
            Defaults to 'value'.
            reverse (bool, optional): Reverse the sorting. Defaults to True.
        """
        return display.to_grepable_text(self.counters, self.laps, sort_by,
                                        reverse)

    def to_html(self, sort_by='value', reverse=True):
        """Return counters in HTML format.

        Args:
            sort_by (str, optional): How to sort the counters.
            Defaults to 'value'.
            reverse (bool, optional): Reverse the sorting. Defaults to True.
        """
        return display.to_html(self.counters, self.laps, sort_by, reverse)

    def to_json(self):
        "Return counters as json"
        return display.to_json(self.counters, self.laps)
