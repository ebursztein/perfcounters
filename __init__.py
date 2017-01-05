"""
Performance counter library

:author: Elie Bursztein (code@elie.net)
"""

from datetime import datetime
import json
import logging
from operator import itemgetter
import time
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

__author__ = 'elie'

# logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PerfCounters():
    """
    Manage a set of performance counters
    """
    COUNT_TIME = 1
    COUNT_VALUES = 2
    SORT_BY_VALUE = 1
    SORT_BY_NAME = 2

    def __init__(self, prefix=''):
        """ Init a new set of counters.
            :param prefix: optional prefix that is automatically added to all counters.
        """
        self.counters = {}
        self.counters_type = {}
        self.prefix = prefix

    def addCounters(self, counters):
        """ Add a set of counters generated elsewhere.
        """
        self.counters.update(counters.counters)
        self.counters_type.update(counters.counters_type)


    def rec(self, name, value=0):
        """ Record a given value
        Semantic suggar for the recordValue function
        :param name: name of the counter
        :param value: the initial value. default 0
        :return:
        """
        self.recordValue(name, value)


    def recordValue(self, name, value=0):
        """ Create a value counter
          :param name: name of the counter
          :param value: the initial value. default 0
        """
        name = "%s_%s" % (self.prefix, name)
        self.counters[name] = value
        self.counters_type[name] = self.COUNT_VALUES


    def inc(self, name, value=1):
        """ Increment a value counter by a given value (default 1)
          :param name: name of the counter
          :param value: value to increment by (can be negative). Default 1
          :note: if counter don't exist creating it.
          :note: semantic sugar for incValue
        """
        self.incValue(name, value)

    def incValue(self, name, value=1):
        """ Increment a value counter by a given value (default 1)
          :param name: name of the counter
          :param value: value to increment by (can be negative). Default 1
          :note: if counter don't exist creating it
        """
        name = "%s_%s" % (self.prefix, name)
        if name in self.counters:
            self.counters[name] += value
        else:
            self.counters_type[name] = self.COUNT_VALUES
            self.counters[name] = value

    def start(self, name, warning_deadline=0, log_start=False):
        """ Create a new time counter.
            :param name: counter name.
            :param log_warning: record a warning log entry using the logging package if the time take exceed log_warning.
            :param: log_start: record an info entry using the logging package when the counter start.
        """
        name = "%s_%s" % (self.prefix, name)
        self.counters[name] = {}
        self.counters[name]['start'] = time.time()
        if warning_deadline:
            self.counters[name]['warning_deadline'] = warning_deadline
        self.counters_type[name] = self.COUNT_TIME
        if log_start:
            logger.info("%s start", name)

    def stop(self, name):
        """ Stop a previously declared time counter.
            :param name: the name of the counter
        """
        name = "%s_%s" % (self.prefix, name)
        if name in self.counters:
            self.counters[name]['stop'] = time.time()
        else:
            error_msg = "counter '%s' stopped before being created" % name
            logger.error(error_msg)
            raise Exception(error_msg)
        if 'warning_deadline' in self.counters[name]:
            diff = self.counters[name]['stop'] - self.counters[name]['start']
            if diff > self.counters[name]['warning_deadline']:
                logger.warn("counter %s deadline exceeded. Operation took: %s secs. Deadline was: %s secs", name, diff,
                             self.counters[name]['warning_deadline'])

    def getJsonStats(self, to_encapsulate=None, sorted_by=1):
        jsonData = {}
        lst = self.getSortedCounterValue(sorted_by)
        jsonData['counters'] = {'value': [],
                                'time': []
        }
        for c in lst:
            if self.counters_type[c[0]] == self.COUNT_TIME:
                counter_type = 'time'
            else:
                counter_type = 'value'
            counter = {'name': c[0],
                       counter_type: c[1],
            }
            if self.counters_type[c[0]] == self.COUNT_TIME:
                jsonData['counters']['time'].append(counter)
            else:
                jsonData['counters']['value'].append(counter)
        stats = json.dumps(jsonData)
        if to_encapsulate:
            return "[%s, %s]" % (to_encapsulate, stats)
        else:
            return stats

    def logCounters(self, sorted_by=1):
        """Write counters in the info log"""
        lst = self.getSortedCounterValue(sorted_by)
        str  = "Performance counters\nTiming counters:\n"
        value_header_added = 0
        for c in lst:
            if self.counters_type[c[0]] == self.COUNT_TIME:
                str += "\t%s: %s sec\n" % (c[0], round(c[1], 3))
            else:
                if not value_header_added:
                    str += "Value counters:\n"
                    value_header_added += 1
                str += "\t%s: %s\n" % (c[0], c[1])
        logger.info(str)
        return None

    def getStringStats(self, sorted_by=1):
        """ Return counters as strings"""
        counters = ''
        lst = self.getSortedCounterValue(sorted_by)
        for c in lst:
            counters += "%s: %s\n" % (c[0], c[1])
        return lst

    def getHTMLStats(self, sorted_by=1):
        counters = ''
        lst = self.getSortedCounterValue(sorted_by)
        for c in lst:
            counters += "%s: %s<br>" % (c[0], c[1])
        return lst

    def getPythonArrayStats(self, sorted_by=1):
        """ Return counters as a python array """
        return self.getSortedCounterValue(self, sorted_by)

    def getSortedCounterValue(self, sorted_by=1):
        """ Inner function used to process the counters.
        """
        time_counters = []
        value_counters = []
        for name, data in self.counters.iteritems():
            if self.counters_type[name] == self.COUNT_TIME:
                if 'stop' not in data:
                    err = 'Counter %s was not stopped.' % name
                    raise Exception(err)
                time_counters.append([name, data['stop'] - data['start']])
            else:
                value_counters.append([name, data])

        if sorted_by == self.SORT_BY_VALUE:
            lst = sorted(time_counters, key=itemgetter(1))
            lst += sorted(value_counters, key=itemgetter(1))
        else:
            lst = sorted(time_counters, key=itemgetter(0))
            lst += sorted(value_counters, key=itemgetter(0))
        return lst

    def get(self, name):
        """
        Return the value of a given counter
        :param name: name of the counter
        :note: semantic sugar for getCounterValue
        :return: the value or time took by the counter
        """
        return self.getCounterValue(name)

    def getCounterValue(self, name):
        """
        Return the value of a given counter
        :param name: name of the counter
        :return: the value or time took by the counter
        """
        name = "%s_%s" % (self.prefix, name)
        if name not in self.counters_type:
            return None
        data = self.counters[name]
        if self.counters_type[name] == self.COUNT_TIME:
            return data['stop'] - data['start']
        else:
            return data

    def recordCountersToElasticSearch(self):
        """ Send counters values to elastic search
          @note: use self.prefix as document_type if it exist. Use counters otherwise

        """
        ELASTICSEARCH_END_POINT = 'http://5070eb8fccf6a59651c8b2611de72468.recent.io'
        INDEX_NAME = "counters"  # describe the name space used for ES. Using the lib name by default
        self.content = {}
        if self.prefix != '':
            document_type = "%s_counters" % self.prefix
        else:
            document_type = 'counters'

        document_id = str(int(time.time() * 100000))
        url = "%s/%s/%s/%s" % (ELASTICSEARCH_END_POINT, INDEX_NAME, document_type, document_id)

        content = {}
        content['timestamp'] = datetime.now().isoformat()
        lst = self.getSortedCounterValue(sorted_by=1)
        # adding counters to the request
        for c in lst:
            counter_name = "%s_%s" % ('perf', c[0])
            content[counter_name] = c[1]
        try:
            json_data = json.dumps(content)
        except:
            error_msg = "Can't convert content to json"
            raise ValueError(error_msg)

        #posting data
        try:
            try:
                from google.appengine.api import urlfetch
                content = urlfetch.fetch(url, payload=json_data, method=urlfetch.PUT, deadline=30)
            except:
                try:
                    import requests
                    content = requests.put(url, data=json_data)
                except:
                    error_msg = "Can't upload to Elasticsearch. Try to install the requests library"
                    raise ValueError(error_msg)

        except:
            error_msg = "Elasticserver appears offline"
            #if ElasticSearch.DEBUG:logging.error(error_msg)
            #raise Exception(error_msg)
            logger.warn(error_msg)
        logger.info('recording to elastic search: %s', url)
        return 1


