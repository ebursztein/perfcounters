# PerfCounters API

`PerfCounters()` available functions:

* [constructor](#constructor)
* [get](#get)
* [increment](#increment)
* [lap](#lap)
* [merge](#merge)
* [start](#start)
* [report](#report)
* [stop](#stop)
* [stop_all](#stop_all)
* [to_json](#to_json)
* [to_html](#to_html)
* [to_text](#to_text)
* [to_grepable_text](#to_grepable_text)

<a id="constructor"></a>
## constructor

```python
PerfCounters(self, prefix=None)
```

### arguments

- **prefix**: prefix that will be preprended to every counter to avoid name collision. Mostly used if you intend to merge counters from multi-origin with `merge`.

<a id="markdown-get" name="get"></a>
## get

```python
PerfCounters.get(self, name)
```

Return the value of a given counter. Return elapsed time (float) for a timing counter and the value for a value counter.

### arguments

- **name (str)**: Counter name.

### returns

(int): Counter value

<a id="markdown-merge" name="merge"></a>
## merge

```python
PerfCounters.merge(self, counters)
```

Merge a set of counters generated elsewhere.

### arguments

- **counters (PerfCounters)**: PerfCounters object

### set

```python
PerfCounters.set(self, name, value=1)
```

Set a value counter to a given values. Create it if needed.

### arguments

- **name (str)**: counter name.
- **value (int, optional)**: Defaults to 1. Counter value.

<a id="markdown-increment" name="increment"></a>
## increment

```python
PerfCounters.increment(self, name, value=1)
```

Increment a value counter by the given value.

### arguments

- **name (str)**: Counter name. Counter will be created if needed.
- **value (int, optional)**: Defaults to 1. Value to increment by.

<a id="markdown-start" name="start"></a>
## start

```python
PerfCounters.start(self, name, warning_deadline=0, log_start=False)
```

Create a new time counter.

### arguments

- **name (str)**: counter name.
- **warning_deadline (int, optional)**: log a warning if the counter exceed deadline.
- **log(Bool, optional)**: if True log an info entry when the counter starts.

<a id="markdown-stop" name="stop"></a>
## stop

```python
PerfCounters.stop(self, name)
```

Stop a given time counter.

### arguments

- **name (str)**: counter name.
- **log(Bool, optional)**: if True log an info entry that the counter stopped with its value.

<a id="markdown-stop_all" name="stop_all"></a>
## stop_all

```python
PerfCounters.stop_all(self)
```

Stop all time counters.

<a id="markdown-report" name="report"></a>
## report

```python
PerfCounters.report(self, sort_by='value', reverse=True)
```

Print counters in `stdout` as nicely formated tables.

### arguments

- *sort_by (str, optional)*: How to sort the counters. Valid values are {value, name}. Defaults to 'value'.
- *reverse (bool, optional)*: Reverse the sorting. Defaults to True.


### output example

```bash

-=[Value counters]=-

+----------------+-----------+
| name           |     value |
+================+===========+
| total_value    | 494280557 |
+----------------+-----------+
| num_iterations |    372159 |
+----------------+-----------+

-=[Timing counters]=-

+--------+------------+
| name   |      value |
+========+============+
| loop   | 0.00195169 |
+--------+------------+
```

<a id="markdown-to_json" name="to_json"></a>
## to_json

```python
PerfCounters.to_json(self)
```

Return counters as json object

### output example

```json
{
  "Timing counters": [
    [
      "loop",
      0.0019519329071044922
    ]
  ],
  "Value counters": [
    [
      "total_value",
      493950295
    ]
  ]
}
```

<a id="markdown-to_html" name="to_html"></a>
## to_html

```python
PerfCounters.to_html(self, sort_by=1, reverse=True)
```

Return counters as HTML tables

### arguments

- **sort_by (int, optional)**: Defaults to `SORT_BY_VALUE`. How to sort counters.
- **reverse (bool, optional)**: Defaults to `False`. Reverse sort order.

### returns

str: counters as HTML tables

### output example

```html
Timing counters</br><table>
<thead>
<tr><th>name  </th><th style="text-align: right;">     value</th></tr>
</thead>
<tbody>
<tr><td>loop  </td><td style="text-align: right;">0.00195193</td></tr>
</tbody>
</table></br>Value counters</br><table>
<thead>
<tr><th>name       </th><th style="text-align: right;">    value</th></tr>
</thead>
<tbody>
<tr><td>total_value</td><td style="text-align: right;">493950295</td></tr>
</tbody>
</table></br>
```

<a id="markdown-log" name="log"></a>
## log

```python
PerfCounters.log(self, sort_by=1, reverse=True)
```

Write counters in the info log

### arguments

- **sort_by (int, optional)**: Defaults to `SORT_BY_VALUE`. How to sort counters.
- **reverse (bool, optional)**: Defaults to `False`. Reverse sort order.