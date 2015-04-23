'''
Performance counter library

:author: Elie Bursztein (code@elie.net)
'''

from datetime import datetime
import json
import logging
from operator import itemgetter
import time

from google.appengine.api import urlfetch


class PerfCounters():
    '''
    Manage a set of performance counters
    '''
    COUNT_TIME = 1
    COUNT_VALUES = 2
    SORT_BY_VALUE = 1
    SORT_BY_NAME = 2

    def __init__(self, prefix=''):
        ''' Init a new set of counters.
            @param prefix: optional prefix that is automatically added to all counters.
        '''
        self.counters = {}
        self.counters_type = {}
        self.prefix = prefix

    def addCounters(self, counters):
        ''' Add a set of counters generated elsewhere.
        '''
        self.counters.update(counters.counters)
        self.counters_type.update(counters.counters_type)


    def recordValue(self, name, value):
        ''' Create a value counter
          @param name: name of the counter
          @param value: the initial value
        '''
        name = "%s_%s" % (self.prefix, name)
        self.counters[name] = {}
        self.counters[name]['start'] = value
        self.counters_type[name] = self.COUNT_VALUES

    def incValue(self, name, value=1):
        ''' Increment a value counter by a given value (default 1)
          @param name: name of the counter
          @param value: value to increment by (can be negative). Default 1
          @raise exception if counter don't exist
        '''
        name = "%s_%s" % (self.prefix, name)
        if name in self.counters:
            self.counters[name]['start'] += value
        else:
            error_msg = "counter '%s' incremented before being created" % name
            logging.error(error_msg)
            raise ValueError(error_msg)

    def start(self, name, warning_deadline=0, log_start=False):
        ''' Create a new time counter.
            @param name: counter name.
            @param log_warning: record a warning log entry using the logging package if the time take exceed log_warning.
            @param: log_start: record an info entry using the logging package when the counter start.
        '''
        name = "%s_%s" % (self.prefix, name)
        self.counters[name] = {}
        self.counters[name]['start'] = time.time()
        if warning_deadline:
            self.counters[name]['warning_deadline'] = warning_deadline
        self.counters_type[name] = self.COUNT_TIME
        if log_start:
            logging.info("%s start", name)

    def stop(self, name):
        ''' Stop a previously declared time counter.
            @param name: the name of the counter
        '''
        name = "%s_%s" % (self.prefix, name)
        if name in self.counters:
            self.counters[name]['stop'] = time.time()
        else:
            error_msg = "counter '%s' stopped before being created" % name
            logging.error(error_msg)
            raise Exception(error_msg)
        if 'warning_deadline' in self.counters[name]:
            diff = self.counters[name]['stop'] - self.counters[name]['start']
            if diff > self.counters[name]['warning_deadline']:
                logging.warn("counter %s deadline exceeded. Operation took: %s secs. Deadline was: %s secs", name, diff,
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
        '''Write counters in the info log'''
        lst = self.getSortedCounterValue(sorted_by)
        for c in lst:
            if self.counters_type[c[0]] == self.COUNT_TIME:
                v = "%s sec" % round(c[1], 3)
            else:
                v = c[1]
            logging.info("%s: %s", c[0], v)

    def getStringStats(self, sorted_by=1):
        ''' Return counters as strings'''
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
        ''' Return counters as a python array '''
        return self.getSortedCounterValue(self, sorted_by)

    def getSortedCounterValue(self, sorted_by=1):
        ''' Inner function used to process the counters.
        '''
        counters = []
        for name, data in self.counters.iteritems():
            if self.counters_type[name] == self.COUNT_TIME:
                if 'stop' not in data:
                    err = 'Counter %s was not stopped.' % name
                    raise Exception(err)
                counters.append([name, data['stop'] - data['start']])
            else:
                counters.append([name, data['start']])
        if sorted_by == self.SORT_BY_VALUE:
            lst = sorted(counters, key=itemgetter(1))
        else:
            lst = sorted(counters, key=itemgetter(0))
        return lst

    def recordCountersToElasticSearch(self):
        ''' Send counters values to elastic search
          @note: use self.prefix as document_type if it exist. Use counters otherwise

        '''
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
        try:
            content = urlfetch.fetch(url, payload=json_data, method=urlfetch.PUT, deadline=30).content
        except:
            error_msg = "Elasticserver appears offline"
            #if ElasticSearch.DEBUG:logging.error(error_msg)
            #raise Exception(error_msg)
            logging.warn(error_msg)
        logging.info('recording to elastic search: %s', url)
        return 1
      
      
      
      
    
    