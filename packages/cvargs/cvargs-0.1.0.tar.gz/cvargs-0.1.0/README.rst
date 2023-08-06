cvargs
======

A decorator to apply a function on certain arguments of a function.


.. code-block:: python

   import cvargs

   @cvargs.convert(foo=float, kwargs=str)
   def func(foo, *bar, **kwargs):
       ...
