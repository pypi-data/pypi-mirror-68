py-gnuplot
***********

`Gnuplot`_ is a portable command-line driven graphing utility for many
platforms. To leverage the powful gnuplot and plot beautiful image in python,
we port gnuplot to python.

.. _Gnuplot: http://www.gnuplot.info/

At first let's see some examples and we will introduce them in detail in the
below.

.. csv-table:: a demonstration of gnuplot script and py-gnuplot script
   :header: "gnuplot demo script", "py-gnuplot demo script", Both script produce the same image
   :widths: 25, 25, 70
   :align: left

   `simple.dem`_, simple1.py_, |simple.1.png|
   `surface2.dem`_, surface2.py_, |surface2.9.png|
   `finance.dem`_, finance.py_, |finance.13.png|

.. _simple.dem: http://gnuplot.sourceforge.net/demo/simple.1.gnu
.. _surface2.dem: http://gnuplot.sourceforge.net/demo/surface2.9.gnu
.. _finance.dem: http://gnuplot.sourceforge.net/demo/finance.13.gnu
.. |simple.1.png| image:: http://gnuplot.sourceforge.net/demo/simple.1.png
   :width: 350
.. |surface2.9.png| image:: http://gnuplot.sourceforge.net/demo/surface2.9.png
   :width: 350
.. |finance.13.png| image:: http://gnuplot.sourceforge.net/demo/finance.13.png
   :width: 350

1. Introduction and basic concept
=================================

Gnuplot is powerful and our aim is to port almost all the functions to python
with the little effort. And we almost done that, we can plot the data as
Gnuplot in python with even less lines.

1.1 The py-gnuplot include two submodules:
------------------------------------------

    * gnuplot: the exact python implementation of gnuplot, it has the same
      functions as gnuplot, we can plot the file and function as in gnuplot;
    * pyplot: We can plot the pandas dataframe generated in python, it process
      the python generated data;

For functions and file data, it's fit to use gnuplot submodule to plot the
data as in gnuplot. For python generated data, especially `pandas`_ dataframe,
it's easy to use pyplot submodule to plot the data;

.. _pandas: https://pandas.pydata.org/

An example for pygnuplot.gnuplot:

1.2 Each submodule has two means to call the functions
------------------------------------------------------

For each submodule, we both have two means to call the functions:

    * object-oriented interface: Via class Gnuplot and you will always have a
      Gnuplot object. 
    * Easy way: Via global class-less functions, almost one single function
      could plot what you want..

object-oriented interface is straightworward and it is simple interepretation
for Gnuplot script and easy to understand if you are familar with Gnuplot. But
it's a little complex to plot data, especially the panda data in the memory.

For easy use and for users who are not very familar with Gnuplot, we develop
the sub module pyplot for easily plotting the data, it refer to the syntax of
matplotlib and mplfinance, the syntax is easy to understand and you needn't
know too much about gnuplot syntax;

It's recommended to use **Easy way** since it's easy to understand based on
the point of python's view.

2. object-oriented interface and Easy way
=========================================

As describe above, object-oriented interface is simple and easy to understand
as gnuplot's logic. Easy way plot the data in python way.

2.1 object-oriented interface
------------------------------

object-oriented interface is a simple wrapper for gnuplot, you can convert the
gnuplot script to py-gnuplot script line by line in py-gnuplot.gnuplot module.
For example we can convert gnuplot demo script: `simple.dem`_ to python script
easily by wrapping them with cmd(''), you can see it's straightforward and is
1:1 mapping:

module gnuplot has an object-oriented interface (via class gnuplotlib) and you
must allocate a gnuplot object before you use it.

.. code-block:: python

    #!/usr/bin/env python3
    #coding=utf8
    from pygnuplot import gnuplot, pyplot

    # Illustration of object-oriented interface, you can see we only wrap the
    # gnuplot script by g.cmd('...') and it's simple and straitfoward if you
    # are familar with Gnuplot.
    g = gnuplot.Gnuplot()
    g.cmd('set terminal pngcairo font "arial,10" fontscale 1.0 size 600, 400')
    g.cmd('set output "simple.1.png"')
    g.cmd('set key fixed left top vertical Right noreverse enhanced autotitle box lt black linewidth 1.000 dashtype solid')
    g.cmd('set style increment default')
    g.cmd('set samples 50, 50')
    g.cmd('set title "Simple Plots" ')
    g.cmd('set title  font ",20" norotate')
    g.cmd('plot [-10:10] sin(x),atan(x),cos(atan(x))')

The generated output is as following:

.. image:: http://gnuplot.sourceforge.net/demo/simple.1.png

Meanwhile we provide more complex wrapper and you can think plot action as a
plot() method and others are set() method, it also works as following:

.. code-block:: python

    #!/usr/bin/env python3
    #coding=utf8
    from pygnuplot import gnuplot, pyplot

    g = gnuplot.Gnuplot()
    g.set(terminal = 'pngcairo font "arial,10" fontscale 1.0 size 600, 400',
            output = '"simple.1.png"',
            key = 'fixed left top vertical Right noreverse enhanced autotitle box lt black linewidth 1.000 dashtype solid',
            style = 'increment default',
            samples = '50, 50',
            title = '"Simple Plots" font ",20" norotate')
    g.plot('[-10:10] sin(x),atan(x),cos(atan(x))')

It's equivalent to method 1 but seems muck like a python script.

2.2 easy way
--------------

The recommended way is simple and easy to understand in python way:

.. _simple1.py:

.. code-block:: python

    #!/usr/bin/env python3
    #coding=utf8
    from pygnuplot import gnuplot, pyplot

    gnuplot.plot('[-10:10] sin(x),atan(x),cos(atan(x))',
            terminal = 'pngcairo font "arial,10" fontscale 1.0 size 600, 400',
            output = '"simple.1.png"',
            key = 'fixed left top vertical Right noreverse enhanced autotitle box lt black linewidth 1.000 dashtype solid',
            style = 'increment default',
            samples = '50, 50',
            title = '"Simple Plots" font ",20" norotate')

This generates exact the same output but is more simple and seems muck like a
python script.

3. gnuplot and pyplot
======================

In brief, gnuplot submodule is for plotting functions and data in file, while
pyplot submodule is for plotting python itself generated data in pandas
dataframe format.

3.1 Sub module gnuplot: the original gnuplot
--------------------------------------------

gnuplot demo script: `surface2.dem`_ could be writen as python script as
following:


.. _surface2.py:

.. code-block:: python

    #!/usr/bin/env python3
    #coding=utf8
    from pygnuplot import gnuplot, pyplot

    gnuplot.splot('cos(u)+.5*cos(u)*cos(v),sin(u)+.5*sin(u)*cos(v),.5*sin(v) with lines',
            '1+cos(u)+.5*cos(u)*cos(v),.5*sin(v),sin(u)+.5*sin(u)*cos(v) with lines',
            terminal = 'pngcairo enhanced font "arial,10" fontscale 1.0 size 600, 400 ',
            output = '"surface2.9.png"',
            dummy = 'u, v',
            key = 'bmargin center horizontal Right noreverse enhanced autotitle nobox',
            style = ['increment default','data lines'],
            parametric = '',
            view = '50, 30, 1, 1',
            isosamples = '50, 20',
            hidden3d = 'back offset 1 trianglepattern 3 undefined 1 altdiagonal bentover',
            xyplane = 'relative 0',
            title = '"Interlocking Tori" ',
            urange = '[ -3.14159 : 3.14159 ] noreverse nowriteback',
            vrange = '[ -3.14159 : 3.14159 ] noreverse nowriteback')

And the generated output is as following:

.. image:: http://gnuplot.sourceforge.net/demo/surface2.9.png

3.2 Sub module pyplot: plot the python generated data
-----------------------------------------------------

Sub module gnuplot is straightworward and easy to understand but a little
complex. It's simple intepretion for Gnuplot script so you must understand
Gnuplot deeply at first.

For easy use and for users who are not very familar with Gnuplot, we develop a
new sub module for easily plotting the data, it refer to the syntax of matplotlib
and mplfinance, the syntax is easy to understand and you needn't know too much
about gnuplot syntax;

Meanwhile, sub module gnuplot is object oriented and you must allocate a
gnuplot object before you use it while submodule pyplot don't need that.
Submodule pyplot need that the data should be panda dataframe format. Let's
see the example `histograms.1.gnu`_ from gnuplot demo, the python sciprt is as
following:

.. _histograms.1.gnu: http://gnuplot.sourceforge.net/demo/histograms.1.gnu

.. code-block:: python

    #!/usr/bin/env python3
    #coding=utf8
    from pygnuplot import gnuplot, pyplot
    import pandas as pd

    df = pd.read_csv('immigration.dat', index_col = 0, sep='\t', comment='#')
    pyplot.plot(df,
            'using 2:xtic(1), for [i=3:22] "" using i ',
            terminal = 'pngcairo transparent enhanced font "arial,10" fontscale 1.0 size 600, 400 ',
            output = '"histograms.1.png"',
            key = 'fixed right top vertical Right noreverse noenhanced autotitle nobox',
            style = 'data linespoints',
            datafile = ' missing "-"',
            xtics = 'border in scale 1,0.5 nomirror rotate by -45 autojustify norangelimit',
            title = '"US immigration from Europe by decade"')

And the generated output is as following:

.. image:: http://gnuplot.sourceforge.net/demo/histograms.1.png

4. Mapping between the original Gnuplot and py-gnuplot
======================================================

The principle is if you can write Gnuplot script, you can write py-gnuplot.
There is 1-1 mapping between almost all Gnuplot command and python function;

Gnuplot commands are mapped to py-python function. Gnuplot has many Commands
but there is only a few ones which are related plot. We will portting more and
more commands and now the following commands are available.

4.1 plot
--------

plot is the primary command for drawing plots with gnuplot::

    plot {<ranges>} <plot-element> {, <plot-element>, <plot-element>}

    # Examples:
    plot sin(x)
    plot sin(x), cos(x)
    plot "datafile.1" with lines, "datafile.2" with points

We port it as a function in py-python and the plot-element is passed as
variable parameters, please be noted that the plot-element should be in the
single quotation marks:

.. code-block:: python

    #!/usr/bin/env python3
    #coding=utf8
    from pygnuplot import gnuplot, pyplot

    # gnuplot.plot() is definied as:
    # def plot(*args, **kwargs)

    # usage examples, please note that we didn't give the
    # output so # could only see the image flash on the
    # screen. Will introduce how to output the image to
    # files.
    gnuplot.plot('sin(x)')
    gnuplot.plot('sin(x)', 'cos(x)')
    gnuplot.plot('"datafile.1" with lines',
                '"datafile.2" with points')

.. important:: Submodule gnuplot and submodule pyplot have difference in plot(), gnuplot.plot() support functions and file data while pyplot.plot() support pandas dataframe data type. Further more pyplot.plot() pass the df as the first parameter. This is the only difference between gnuplot submodule and pyplot module.

If we generate the data in the python insteading using the exist funtions and
datafile, we should use pyplot to plot the data, for example:

.. code-block:: python

    #!/usr/bin/env python3
    #coding=utf8
    from pygnuplot import gnuplot, pyplot

    # pyplot.plot() is definied as:
    # def plot(df, *args, **kwargs)

    # usage examples, please note that we didn't give the output so could only
    # see the image flash on the screen. Will introduce how to output the
    # image to files.
    df = pd.DataFrame(data = {'col1': [1, 2],
                              'col2': [3, 4],
                              'col3': [5, 6]})
    gnuplot.plot(df, 'using 1:2 with lines', 'using 1:3 with points')


4.2 splot
---------

splot is the command for drawing 3D plots::

    splot {<ranges>}
    {<iteration>}
    <function> | {{<file name> | <datablock name>} {datafile-modifiers}}

    # Examples:
    splot sin(sqrt(x**2+y**2))/sqrt(x**2+y**2)
    splot ’<file_name>’

We port it as a function splot() in py-python and the plot-element is passed
as variable parameters, please be noted that the plot-element should be in the
single quotation marks:

.. code-block:: python

    #!/usr/bin/env python3
    #coding=utf8
    from pygnuplot import gnuplot, pyplot

    # gnuplot.splot() is definied as:
    # def splot(*args, **kwargs)

    # usage examples, please note that we didn't give the output so
    # could only see the image flash on the screen. Will introduce
    # how to output the image to files.
    gnuplot.splot('sin(sqrt(x**2+y**2))/sqrt(x**2+y**2)')
    gnuplot.splot('"<file_name>"')

4.3 set
-------

The set command can be used to set lots of options in gnuplot. for example::

    set xtics offset 0,graph 0.05
    set label "y=x" at 1,2
    set label 2 "S" at graph 0.5,0.5 center font "Symbol,24"
    set label 3 "y=x^2" at 2,3,4 right

In py-gnuplot we use dictionary parameter to pass them to plot() function, We
use each option name as the key, the option value as the dictionary value.
If some option contain an iteration clause, we use list as the dictionary value,
then the above set command could be writen as::

    xtics = 'offset 0,graph 0.05'
    labes = ['"y=x" at 1,2',
             '2 "S" at graph 0.5,0.5 center font "Symbol,24"',
             '3 "y=x^2" at 2,3,4 right']

For example the following Gnuplot script::

    set boxwidth 0.9 relative
    set style fill solid 1.0
    set label "y=x" at 1,2
    set label 2 "S" at graph 0.5,0.5 center font "Symbol,24"
    set label 3 "y=x^2" at 2,3,4 right
    plot ’file.dat’ with boxes

could be implemented as the following:

.. code-block:: python

    #!/usr/bin/env python3
    #coding=utf8
    from pygnuplot import gnuplot, pyplot

    # style is passed as function dictionary parameter
    gnuplot.plot('"file.dat’with boxes',
                boxwidth = '0.9 relative',
                style = 'fill solid 1.0',
                labes = ['"y=x" at 1,2',
                '2 "S" at graph 0.5,0.5 center font "Symbol,24"',
                '3 "y=x^2" at 2,3,4 right'])

By default, Gnuplot display the output to the standard output. The set term
and output command redirects the display to the specified file or device::

    set terminal pngcairo font "arial,10" fontscale 1.0 size 600, 400
    set output "test.png"

Then if we want to redirect the image to a file, we could do that by giving
the term and output parameters:

.. code-block:: python

    #!/usr/bin/env python3
    #coding=utf8
    from pygnuplot import gnuplot, pyplot

    # style is passed as function dictionary parameter
    gnuplot.plot('"file.dat’with boxes',
                boxwidth = '0.9 relative',
                style = 'fill solid 1.0',
                labes = ['"y=x" at 1,2',
                '2 "S" at graph 0.5,0.5 center font "Symbol,24"',
                '3 "y=x^2" at 2,3,4 right'],
                output = '"finance.13.png"',
                term = 'pngcairo font "arial,10" fontscale 1.0 size 900, 600')


4.4 multiplot
-------------

In Gnuplot, multiplot is not a command but a option to enable multiplot mode.
But we use it as a seperate function multiplot() to plot several data next to
each other on the same page or screen window::

    def multiplot(\*args, \*\*kwargs):
        @args: the subplot object list;
        @kwargs: the setting options that need to be set before call plot;

    def make_subplot(\*args, \*\*kwargs)
        The parameter definition is the same as plot()/splot, but it doesn't
        plot the df really, it only return the plot dictionary for later
        multiplot() use.

Before call multiplot() we must generate the subplot object by calling
make_subplot(), It is much like mplfinance.add_plot(), it only add the subplot
command for further call:

.. code-block:: python

    #!/usr/bin/env python3
    #coding=utf8
    from pygnuplot import gnuplot, pyplot

    sub1 = gnuplot.make_subplot('sin(x)', ylabel = 'ylabel')
    sub2 = gnuplot.make_subplot('cos(x)', xlabel = 'xlabel')
    sub3 = gnuplot.make_subplot('sin(2*x)', noxlabel = '', ylabel = '')
    sub4 = gnuplot.make_subplot('cos(2*x)', xlabel = 'xlabel')
    gnuplot.multiplot(sub1, sub2, sub3, sub4,
                      output = '"sample.multiplot.png"',
                      term = 'pngcairo size 900,600 font ",11"',
                      multiplot  = 'layout 2,2 columnsfirst margins 0.1,0.9,0.1,0.9 spacing 0.1')

5. Plot methods detail
======================

5.1 methods in gnuplot
-----------------------

5.2 methods in pyplot
-----------------------

pyplot is easy to use and it only has a few functions, all the configuration
are passed as function parameter.

pyplot take pandas dataframe as data.

plot(df, \*args, \*\*kwargs)
+++++++++++++++++++++++++++++

@ df: The data that need to plot. it should be pandas dataframe format.
In gnuplot we pass the data as a function or data file. But normally in
python script, we normally get the data in the memory, not in the file. So
we develop the submodule to plot the data in memory, we should pass the df
in pandas dataframe format, for example::

    df = pd.read_csv('immigration.dat', index_col = 0,
                    sep='\t', comment='#')
    pyplot.plot(df, ...)

@ args: The plot command we need to plot. Gnuplot plot data like that::

    plot 'finance.dat' using 0:2:3:4:5 notitle with financebars lt 8, \
         'finance.dat' using 0:9 notitle with lines lt 3, \
         'finance.dat' using 0:10 notitle with lines lt 1, \
         'finance.dat' using 0:11 notitle with lines lt 2

Now we omit the command "plot" and data "finance.dat" since we have
already pass them in the function name and the first parameter "df", we
pass the command as a list of command as following::

    pyplot.plot(df,
                'using 0:2:3:4:5 notitle with financebars lt 8',
                'using 0:9 notitle with lines lt 3',
                'using 0:10 notitle with lines lt 1',
                'using 0:11 notitle with lines lt 2',
                ...)

@ kwargs: As we know The set command is
used to set lots of options before plot, splot, or replot command is
given. We skip the 'set' keyword and use the options name as the key, the
following part is used the attribute value, for example we use the
following line to set the xtics in gnuplot::

    set xtics border in scale 1,0.5 nomirror rotate by -45 autojustify norangelimit

Then in the function, we will use::

    xtics = 'border in scale 1,0.5 nomirror rotate by -45 autojustify norangelimit'

as a parameters. Some options order sensitive, so we need the python
version > 3.7, which seems to pass the function parameter in order. Or there will
some issue and cause exception::

    pyplot.plot(df,
                'using 0:2:3:4:5 notitle with financebars lt 8',
                ...,
                xtics = 'border in scale 1,0.5 nomirror rotate by -45 autojustify norangelimit',
                ...)

splot(df, \*args, \*\*kwargs)
+++++++++++++++++++++++++++++

The parameter are same as plot(), the only difference is it use "splot" to
plot insteading of "plot".

make_subplot(df, \*args, \*\*kwargs)
+++++++++++++++++++++++++++++++++++++

The parameter definition is the same as plot()/splot, but it doesn't plot the
df really, it only return the plot dictionary for later multiplot() use.

It is much like mplfinance.add_plot(), it only add the subplot command for
further call::

    sub1 = pyplot.make_subplot(df,
            'using 0:2:3:4:5 notitle with candlesticks lt 8',
            'using 0:9 notitle with lines lt 3',
            logscale = 'y',
            yrange = '[75:105]',
            ytics = '(105, 100, 95, 90, 85, 80)',
            xrange = '[50:253]',
            grid = 'xtics ytics',
            lmargin = '9',
            rmargin = '2',
            format = 'x ""',
            xtics = '(66, 87, 109, 130, 151, 174, 193, 215, 235)',
            title = '"Change to candlesticks"',
            size = ' 1, 0.7',
            origin = '0, 0.3',
            bmargin = '0',
            ylabel = '"price" offset 1',
            label = ['1 "Acme Widgets" at graph 0.5, graph 0.9 center front',
                '2 "Courtesy of Bollinger Capital" at graph 0.01, 0.07',
                '3 "  www.BollingerBands.com" at graph 0.01, 0.03']
            )

multiplot(\*args, \*\*kwargs)
++++++++++++++++++++++++++++++++++

The multiplot set the setting in kwargs at first, and then call the
subplot in args to multiplot.

@args: It is the list of subplot generated by make_subplot(), it would be
called one by one.

@kwargs: The global setting for multiplot;

For example::

    pyplot.multiplot(sub1, sub2,
            output = '"history.%s.png"' %(code),
            term = 'pngcairo size 1920,1080 font ",11"')

multisplot(\*args, \*\*kwargs)
++++++++++++++++++++++++++++++++++

To be implemented.

6. More examples
================

6.1 splot
---------

module gnuplot has an object-oriented interface (via class gnuplotlib) and you
must allocate a gnuplot object before you use it.

.. _simple.dem: http://gnuplot.sourceforge.net/demo/simple.1.gnu
.. code-block:: python

    #!/usr/bin/env python3
    #coding=utf8
    from pygnuplot import gnuplot, pyplot
    g = gnuplot.Gnuplot()
    g.cmd('set terminal pngcairo font "arial,10" fontscale 1.0 size 600, 400')
    g.cmd('set output "simple.1.png"')
    g.cmd('set key fixed left top vertical Right noreverse enhanced autotitle box lt black linewidth 1.000 dashtype solid')
    g.cmd('set style increment default')
    g.cmd('set samples 50, 50')
    g.cmd('set title "Simple Plots" ')
    g.cmd('set title  font ",20" norotate')
    g.cmd('plot [-10:10] sin(x),atan(x),cos(atan(x))')

The generated output is as following:

.. image:: http://gnuplot.sourceforge.net/demo/simple.1.png

6.2 multiplot
-------------

we convert the gnuplot demo script: `finance.dem`_ to the final python script:

.. _finance.py:

.. code-block:: python

    #!/usr/bin/env python3
    #coding=utf8
    from pygnuplot import gnuplot, pyplot
    import pandas as pd

    df = pd.read_csv('finance.dat', sep='\t', index_col = 0, parse_dates = True,
            names = ['date', 'open','high','low','close', 'volume','volume_m50',
                'intensity','close_ma20','upper','lower '])
    sub1 = pyplot.make_subplot(df,
            'using 0:2:3:4:5 notitle with candlesticks lt 8',
            'using 0:9 notitle with lines lt 3',
            'using 0:10 notitle with lines lt 1',
            'using 0:11 notitle with lines lt 2',
            'using 0:8 axes x1y2 notitle with lines lt 4',
            logscale = 'y',
            yrange = '[75:105]',
            ytics = '(105, 100, 95, 90, 85, 80)',
            xrange = '[50:253]',
            grid = 'xtics ytics',
            lmargin = '9',
            rmargin = '2',
            format = 'x ""',
            xtics = '(66, 87, 109, 130, 151, 174, 193, 215, 235)',
            title = '"Change to candlesticks"',
            size = ' 1, 0.7',
            origin = '0, 0.3',
            bmargin = '0',
            ylabel = '"price" offset 1',
            label = ['1 "Acme Widgets" at graph 0.5, graph 0.9 center front',
                '2 "Courtesy of Bollinger Capital" at graph 0.01, 0.07',
                '3 "  www.BollingerBands.com" at graph 0.01, 0.03']
            )

    sub2 = pyplot.make_subplot(df,
            'using 0:($6/10000) notitle with impulses lt 3',
            'using 0:($7/10000) notitle with lines lt 1',
            bmargin = '',
            size = '1.0, 0.3',
            origin = '0.0, 0.0',
            tmargin = '0',
            nologscale = 'y',
            autoscale = 'y',
            format = ['x', 'y "%1.0f"'],
            ytics = '500',
            xtics = '("6/03" 66, "7/03" 87, "8/03" 109, "9/03" 130, "10/03" 151, "11/03" 174, "12/03" 193, "1/04" 215, "2/04" 235)',
            ylabel = '"volume (0000)" offset 1')

    pyplot.multiplot(sub1, sub2,
            output = '"finance.13.png"',
            term = 'pngcairo font "arial,10" fontscale 1.0 size 900, 600')

And this the generated output:

.. image:: http://gnuplot.sourceforge.net/demo/finance.13.png

7. Q/A
======

8. TODO
============

The 0.1 release only support plot/multiplot, will support splot/multisplot the
next release
