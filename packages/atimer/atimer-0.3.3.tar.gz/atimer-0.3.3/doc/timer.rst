Timer Usage
===========
A timer instance is created with :py:class:`atimer.Timer` class. To delay
execution, await the timer object. The result of the await expression is
number of timer expirations.

The next example creates timer object with 250 ms interval, arms the timer
and uses the timer six times in the loop (the if statement purpose is
explained below).

.. literalinclude:: ../examples/time-show.py
   :lines: 20-41

The output of the example shows loop iteration counter, current system
clock value and number of expirations::

    0: 1548799590.000  1
    1: 1548799590.250  1
    2: 1548799590.500  1
    3: 1548799591.602  4
    4: 1548799591.750  1
    5: 1548799592.000  1

The following properties of the timer can be noticed

- the difference between each execution is 250ms; this is despite the
  the time needed for execution of all the statements within the loop
- almost all timer expirations are synchronized with system clock at the
  edge of the 250 ms interval
- one expiration (loop iteration `3`) is affected by overrun due to the
  `time.sleep` statement; however the timer corrects itself to continue
  delayed execution at expected pace

.. vim: sw=4:et:ai
