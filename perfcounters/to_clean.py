    def _tabulate(self, sort_by=1, reverse=True, table_format='grid'):
        """Format counters as ASCII tables.

        Args:
            sort_by (int, optional): Defaults to SORT_BY_VALUE. How to\
            sort counters.
            reverse (bool, optional): Defaults to False. Reverse sort order.
            table_format (str, optional): Defaults to grid. Tabulate table\
            format style to use.

        Returns:
            dict: time_counters, value_counters as ASCII tables.
        """

        tables = {}
        counter_lists = self._get_counter_lists(sort_by, reverse)

        for cnt_type, cnts in counter_lists.items():

            # add laps stats if they exist to timer counters
            if cnt_type == self.TIMER_COUNTER and len(self.laps):
                headers = ['name', 'value', 'laps']

            else:
                headers = ["name", "value"]

            tables[cnt_type] = tabulate(cnts, headers, tablefmt=table_format)

        return tables

    def _get_counter_lists(self, sort_by=1, reverse=True):
        """Get sorted counter lists.
        """
        counters = defaultdict(list)
        for name, data in self.counters.items():
            if self.counters[name]['type'] == self.TIMER_COUNTER:
                if 'stop' not in data:
                    delta = time.time() - data['start']
                else:
                    delta = data['stop'] - data['start']
                # FIXME: lap stats
                counters['Timing counters'].append([name, delta])
            else:
                counters['Value counters'].append([name, data['value']])

        for k, v in counters.items():
            counters[k] = sorted(v, key=itemgetter(sort_by), reverse=reverse)

        return counters


   def report(self, sort_by=1, reverse=True):
        """Print counters in stdout as nicely formated tables.

        Args:
            sort_by (int, optional): Defaults to SORT_BY_VALUE. How to\
            sort counters.
            reverse (bool, optional): Defaults to False. Reverse sort order.
        """
        tables = self._tabulate(sort_by=sort_by, reverse=reverse)
        for table_name, table in tables.items():
            print("-=[%s]=-\n" % table_name)
            print("%s\n" % table)

    def log(self, sort_by=1, reverse=True):
        """Write counters in the info log

        Args:
            sort_by (int, optional): Defaults to SORT_BY_VALUE. How to\
            sort counters.
            reverse (bool, optional): Defaults to False. Reverse sort order.
        """
        counter_lists = self._get_counter_lists(sort_by, reverse)
        for cnt_type, cnts in counter_lists.items():
            logger.info("\n-=[%s]=-\n" % cnt_type)
            for cnt in cnts:
                logger.info("%s:%s\n" % (cnt[0], cnt[1]))




    def to_json(self):
        """Return counters as json object"""
        counters = self._get_counter_lists()
        # FIXME add laps and don't use a list
        return json.dumps(counters)

    def to_html(self, sort_by=1, reverse=True):
        """Return counters as HTML tables

        Args:
            sort_by (int, optional): Defaults to SORT_BY_VALUE. How to\
            sort counters.
            reverse (bool, optional): Defaults to False. Reverse sort order.
        Returns:
            str: counters as HTML tables
        """
        tables = self._tabulate(table_format='html')
        html = ""
        for table_name, table in tables.items():
            html += "%s</br>%s</br>" % (table_name, table)
        return html