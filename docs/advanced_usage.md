# Advanced usage examples

Here are a few examples that demonstrate PerfCounters advanced options. All the examples showcased in this section are available as part of the [demo script](https://github.com/ebursztein/perfcounters/blob/master/demo.py)

Available examples:
- [Merging counters](#merge)
- [Customizing counters output sorting](#sorting)
- [Outputing counters in various format](#output)
- [Getting the number of counters](#counting)

<a id="deadline"></a>
## Adding counter deadline

It is possible to specify a deadline while creating a timing counter. If the couter value exceed this deadline then a warning log entry will be issued. These warning are mostly used to help monitoring API performance overtime. Adding a deadline is a simple as:

```python
counters = PerfCounters()
# counter will emit a log warning if time between start and stop exceed 1sec.
counters.start('deadline_monitor', warning_deadline=1)
time.sleep(2)
counters.stop('deadline_monitor')
```

<a id="merge"></a>
## Merging counters

It is possible to merge counters from two PerfCounter objects. This is usually used to aggregate counters coming from subfunctions. To avoid counter name collision PerfCounters allows counter names auto-prefixing by adding a prefix in the constructor. if two counters have the same name `PerfCounters` will raise a `ValueError`.

Both prefixing and merging is illustrated in the following example:

```python
counters = PerfCounters()
counters.set('test', 42)

# set counter prefix via constructor to avoid name collision
other_counters = PerfCounters('others')
other_counters.set('test', 42)
counters.report()
```

This result of the following output:

```bash
-=[Value counters]=-

+-------------+---------+
| name        |   value |
+=============+=========+
| test        |      42 |
+-------------+---------+
| others_test |      42 |
+-------------+---------+
```

<a id="sorting"></a>
## Sorting counters

By default counters are sorted by "value desc". You can change this behavior with the optional arguments available in all reporting functions: `report()`, `to_html()`, `log()`...

here is a short example that illustrate the various sorting options:

```python
counters = PerfCounters()
counters.set('a', 42)
counters.set('b', 40)
counters.set('c', 41)

print("sort by value desc (default)")
counters.report()

print("sort by value asc")
# the sort_by parameter is optional as value is the default value.
counters.report(sort_by='value', reverse=False)

print("sort by name desc")
counters.report(sort_by='name')

print("sort by name asc")
counters.report(sort_by='name', reverse=False)
```

*note*: PerfCounters only output a table if needed. So if there is no timing counters then the timing table will not be outputed. Accordingly the code above produce the following expected results.

**(default) sort by value desc output result**:

```bash
-=[Value counters]=-

+--------+---------+
| name   |   value |
+========+=========+
| a      |      42 |
+--------+---------+
| c      |      41 |
+--------+---------+
| b      |      40 |
+--------+---------+
```

**sort by value asc output result**:

```bash
-=[Value counters]=-

+--------+---------+
| name   |   value |
+========+=========+
| b      |      40 |
+--------+---------+
| c      |      41 |
+--------+---------+
| a      |      42 |
+--------+---------+
```

**sort by name desc output result**:

```bash
-=[Value counters]=-

+--------+---------+
| name   |   value |
+========+=========+
| c      |      41 |
+--------+---------+
| b      |      40 |
+--------+---------+
| a      |      42 |
+--------+---------+
```

**sort by name asc output result**:

```bash
-=[Value counters]=-

+--------+---------+
| name   |   value |
+========+=========+
| a      |      42 |
+--------+---------+
| b      |      40 |
+--------+---------+
| c      |      41 |
+--------+---------+
```

<a id="output"></a>
## Output options

Beside printing in terminal `perfcounters` offers multiple reporting options. Here are the main ones:

```python
counters = PerfCounters()
counters.start('loop')
for i in range(1000):
    v = randint(0, 1000000)
    counters.increment('total_value', v)
counters.stop('loop')

print("Terminal output")
counters.report()

print("HTML output")
print(counters.to_html())

print("JSON output")
print(counters.to_json())

print("Log output")
counters.log()
```

**HTML output result**

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

**JSON output result**

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

<a id="counting"></a>
## Getting the numbers of counters

```python
counters = PerfCounters()
counters.set('test', 42)
print(len(counters))
```
