"""
Performance counters library
"""
from datetime import datetime
import json
import logging
from operator import itemgetter
import time
from tabulate import tabulate
from collections import defaultdict

__version__ = '1.0.0'
__author__ = 'Elie Bursztein (code@elie.net)'


# logger
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PerfCounters():
    """
    Manage a set of performance counters
    """
    TIMER_COUNTER = 1
    VALUE_COUNTER = 2

    SORT_BY_VALUE = 1
    SORT_BY_NAME = 0

    def __init__(self, prefix=None):
        """Init a new set of counters.

        Args
            prefix (str, optional): prefix automatically appended to counters.
        """
        self.counters = defaultdict(dict)
        self.prefix = prefix

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
        if self.counters[name]['type'] == self.TIMER_COUNTER:
            return data['stop'] - data['start']
        else:
            return data['value']

    def merge(self, counters):
        """Merge a set of counters generated elsewhere.

        Args:
            counters (PerfCounters): PerfCounters object
        """
        self.counters.update(counters.counters)
  
    def set(self, name, value=1):
        """Set a recording counter to a given values

        Args:
            name (str): counter name.
            value (int, optional): Defaults to 1. Counter value.
        """

        name = self._prefix_counter(name)
        self.counters[name]['value'] = value
        self.counters[name]['type'] = self.VALUE_COUNTER

    def increment(self, name, value=1):
        """
        Increment counter by the given value.

        Args:
            name (str): Counter name. Counter will be created if needed.
            value (int, optional): Defaults to 1. Value to increment by.
        """

        name = self._prefix_counter(name)
        if name in self.counters:
            self.counters[name]['value'] += value
        else:
            self.set(name, value=value)

    def start(self, name, warning_deadline=0, log_start=False):
        """ Create a new time counter.

        Args
            name (str): counter name.
            warning_deadline (int, optional): log a warning if the counter \
            exceed deadline.
            log_start(Bool, optional): if True log an info entry when \
            the counter start.
        """
        name = self._prefix_counter(name)
        self.counters[name] = {}
        self.counters[name]['start'] = time.time()
        self.counters[name]['type'] = self.TIMER_COUNTER

        if warning_deadline:
            self.counters[name]['warning_deadline'] = warning_deadline

        if log_start:
            logger.info("%s start", name)

    def stop(self, name):
        """ Stop a previously declared time counter.
            name (str): the name of the counter
        """
        name = self._prefix_counter(name)
        if name in self.counters:
            self.counters[name]['stop'] = time.time()
        else:
            error_msg = "counter '%s' stopped before being created" % name
            logger.error(error_msg)
            raise ValueError(error_msg)

        if 'warning_deadline' in self.counters[name]:
            diff = self.counters[name]['stop'] - self.counters[name]['start']
            if diff > self.counters[name]['warning_deadline']:
                logger.warn("counter %s deadline exceeded. Operation took:\
                            %s secs. Deadline was: %s secs", name, diff,
                            self.counters[name]['warning_deadline'])

    def to_json(self):
        """Return counters as json object"""

        counters = self._get_counter_lists()
        return json.dumps(counters)

    def to_html(self, sort_by=1, reverse=False):
        """Return counters as HTML tables

        Args
            sort_by (int, optional): Defaults to SORT_BY_VALUE. How to\
            sort counters.
            reverse (bool, optional): Defaults to False. Reverse sort order.
        Return
            str: counters as HTML tables
        """
        tables = self._tabulate(table_format='html')
        html = ""
        for table_name, table in tables.items():
            html += "%s</br>%s</br>" % (table_name, table)
        return html

    def report(self, sort_by=1, reverse=False):
        """Print counters in a nicely formated table.

        Args
            sort_by (int, optional): Defaults to SORT_BY_VALUE. How to\
            sort counters.
            reverse (bool, optional): Defaults to False. Reverse sort order.
        """
        tables = self._tabulate(sort_by=sort_by, reverse=reverse)
        for table_name, table in tables.items():
            print("-=[%s]=-\n" % table_name)
            print("%s\n" % table)

    def log(self, sort_by=1, reverse=False):
        """Write counters in the info log

        Args
            sort_by (int, optional): Defaults to SORT_BY_VALUE. How to\
            sort counters.
            reverse (bool, optional): Defaults to False. Reverse sort order.
        """
        counter_lists = self._get_counter_lists(sort_by, reverse)
        for cnt_type, cnts in counter_lists.items():
            logger.info("\n-=[%s]=-\n" % cnt_type)
            for cnt in cnts:
                logger.info("%s:%s\n" % cnt[0], cnt[1])

    def _tabulate(self, sort_by=1, reverse=False, table_format='grid'):
        """Format counters as ASCII tables.

        Args
            sort_by (int, optional): Defaults to SORT_BY_VALUE. How to\
            sort counters.
            reverse (bool, optional): Defaults to False. Reverse sort order.
            table_format (str, optional): Defaults to grid. Tabulate table\
            format style to use.
        Return
            dict: time_counters, value_counters as ASCII tables.
        """

        tables = {}
        counter_lists = self._get_counter_lists(sort_by, reverse)
        headers = ["name", "value"]

        for cnt_type, cnts in counter_lists.items():
            tables[cnt_type] = tabulate(cnts, headers, tablefmt=table_format)

        return tables

    def _get_counter_lists(self, sort_by=1, reverse=False):
        """ Get sorted counter lists.
        """
        counters = defaultdict(list)
        for name, data in self.counters.items():
            if self.counters[name]['type'] == self.TIMER_COUNTER:
                if 'stop' not in data:
                    err = 'Counter %s was not stopped.' % name
                    raise Exception(err)
                counters['Timing counters'].append([name,
                                                 data['stop'] - data['start']])
            else:
                counters['Value counters'].append([name, data['value']])

        for k, v in counters.items():
            counters[k] = sorted(v, key=itemgetter(sort_by), reverse=reverse) 

        return counters

    def _prefix_counter(self, name):
        """Prefix counter if needed.

        Args:
            name (str): counter name.
        """

        if self.prefix:
            return "%s_%s" % (self.prefix, name)
        else:
            return name

