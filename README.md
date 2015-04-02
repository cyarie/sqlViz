# The SQL Visualizer:
### A Cheap Way to Visualize Data

### Why

Sometimes, you really, really want to pull a quick visualization of some SQL you just wrote, but don't want to
deal with Tableau licenses, or paying tremendous amounts of money for something similar. You don't need an entire
dashboard, you don't need a bunch of filters -- you need the results of your SQL converted to something like JSON,
and put into a chart for quick and easy display. If that's you, you're in the right place!

### How

This tool is fairly simple and straight-forward to use, *if you already know SQL*. The idea behind this tool is that you
assign the items in your `SELECT` statement as *x and y accessors*. Here's an example:

```
SELECT SUM(a.some_value) AS y1,
       COUNT(b.another_value) AS y2,
       DATE_FORMAT(a.some_date, '%Y-%m-%d') AS x1
FROM table_a a
INNER JOIN table_b b
       ON DATE_FORMAT(a.some_date, '%Y-%m-%d') = DATE_FORMAT(b.some_date, '%Y-%m-%d')
WHERE a.some_date >= '2015-01-01'
       AND a.some_date <= '2015-01-31'
       AND a.some_filter IN (1,2)
       AND a.another_filter IN (1,2,3,4)
GROUP BY x1
ORDER BY x1 ASC;
```

After the request is made, the application will send the SQL back to the database for processing, and after receiving
that output, will convert it into JSON. Using the above query as an example, the JSON will look something like:

```
[{y1: 1, y2: 3, x1: '2015-01-01'}, {y1: 2, y2: 4, x1: '2015-01-02'}, ...]
```

You can break your timeseries into any date format you choose -- down to the very second. Use the *Date Format* text input
to specify how MetricsGraphics should interpret your dates.

### Note:
* The base application is set up to use MySQL, but this should be usable by whatever DB you like.