# Advanced usage examples

Here are a few examples that demonstrate PerfCounters advanced options. All the examples showcased in this section are available as part of the [demo script](https://github.com/ebursztein/perfcounters/blob/master/demo.py)

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
counters.report(reverse=False)

print("sort by name desc")
counters.report(sort_by=PerfCounters.SORT_BY_NAME)

print("sort by name asc")
counters.report(sort_by=PerfCounters.SORT_BY_NAME, reverse=False)
```

This code produce the following expected results:

**sort by value desc (default)**:

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

**sort by value asc**:

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

**sort by name desc**:

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

**sort by name asc**:

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

## Reporting options

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

**HTML output**

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

**JSON output**

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

## Getting the numbers of counters

```python
counters = PerfCounters()
counters.set('test', 42)
print(len(counters))
```