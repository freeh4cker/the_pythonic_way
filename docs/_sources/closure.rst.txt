.. _closure:


========
Closures
========

.. warning::

    To understand this course you must master the concepts of mutable and immutable objects, references to the objects,
    scope of variables, lifetime of variables ...

    These concepts are covered in the course :ref:`Fundamentals of python <fundamentals>`.


Introduction
============

The concept of closures was developed in the 1960s and was first fully implemented in 1970s
as a language feature in the Scheme programming language to support lexically scoped first-class functions.
The use of closures is associated with functional programming languages [wikipedia]_
In Object Oriented Programming languages we consider that objects are data with methods attached.
In functional programming Languages closures are functions with data attached [Sebastian]_.


.. container::

    .. image:: _static/figs/closure1.png
        :alt: nested function namespace
        :align: left
        :height: 200px

    .. code-block:: python
        :linenos:

        def foo():
            x = 3
            y = 'z'
            def bar():
                print(x, y)
            x = 5
            return bar

.. container::

   In the namespace of foo there are three locals variables *x*, *y* and *bar*
   but when the execution of foo is finished the corresponding namespace disappear,
   except the return varialble to the function *bar*

.. container:: clearer

   .. image :: _static/figs/spacer.png


.. container::

    .. image:: _static/figs/closure2.png
        :alt: nested function namespace
        :align: left
        :height: 265px

    .. code-block:: python
        :linenos:
        :lineno-start: 8

        b = foo()

.. container::

   In *b* function we refer to *x* and *y* variables (see line 5).

   | So when does the execution of *b* will work?
   | How *b* can work with variables used which are not defined in any namespaces (neither local, nor global)?

.. container:: clearer

   .. image :: _static/figs/spacer.png


Now closures comes on stage
---------------------------


Although the concept of closure exists in python from version 2.2 [Guido_van_Rossum]_ in python2,
there is some limitations in there uses.
These limitations has been overcome in python3.
In the following examples I will try to show you how closures work python3 and
I'll point out the limitations in python2.

.. container::

    .. image:: _static/figs/closure3.png
        :alt: closure
        :align: left
        :height: 200px

    .. code-block:: python
        :linenos:

        def foo():
            x = 3
            y = 'z'
            def bar():
                print(x, y)
            x = 5
            return bar

        >>> b()
        >>> 5 z
        >>> b.__closure__
        (<cell at 0x7f7ae69bf5e8: int object at 0x7f7ae68638c0>, <cell at 0x7f7ae68c01c8: str object at 0x7f7ae68cfae8>)
        >>> b.__closure__[0].ce_contents
        >>> 5
        >>> b.__code__.co_freevars
        ('x', 'y')


    Thanks to the introspection functionality of Python, we can see how it works.
    When foo namespace disappear at the end of the function.
    Python see that bar namespace reference an element in foo.
    So instead of mark it for garbaging, it capture it in a closure.

    We can see line 11 that `b` have a closure (a tuple) with two elements, these elements reference an `int`
    and a `string` object.
    The value of this elements (cell) are `5` and `'z'`.

    The function capture also in the `b.__code__.co_freevars` the name of the variables caught in the closure
    'x' and 'y'. So when the code of bar is executed the local variables are created in the local namespace.
    When the code run and execute the line 5 *print(x, y)*
    *x* and *y* have not been created in the local namespace (the declaration-assignment operator *=* is not used)
    so python lookup if a closure was created, the variables name are in __code__.co_freevars and
    their values are in *__closure__* in the same order.

.. container:: clearer

   .. image :: _static/figs/spacer.png

As I said above a closure, is when a function reference a non-local variable of that function.
To work the function capture these "free" variables in a "closure".
After the definition of the function the variables are accessible only via a reference inside the function.
But the variables are not in the scope or namespace of the function so their lifetime
is not the function execution lifetime but the function itself.
So the function can keep a state between several calls.



Several function can share the same closure
===========================================

.. container::

    .. image:: _static/figs/closure4.png
        :alt: 2 func share closure
        :align: left
        :height: 300px

    .. code-block:: python
            :linenos:

            def foo(x):
                def read():
                    return x
                def write(y):
                    nonlocal x
                    x += y
                    return x
                return read, write
            >>>
            >>> r, w = foo(3)
            >>>
            >>> r()
            3
            >>> r.__closure__
            (<cell at 0x7f8b697045e8: int object at 0x7f8b695a8880>,)
            >>> w.__closure__
            (<cell at 0x7f8b697045e8: int object at 0x7f8b695a8880>,)


In this example we can see that only one closure (same memory address) is made and both `write` and `read` functions reference
this closure. So if we modify the *x* variable in the closure from the `write` function the `read` function have the
updated value.

But we can create new functions objects corresponding to `read` and `write` functions.
These new functions will referenced a new closure (the memory address is different than `r.__closure__`)::

    >>> r2, w2 = foo(5)
    >>> r2.__closure__
    (<cell at 0x7f8b69605378: int object at 0x7f8b695a88c0>,)
    >>> w2.__closure__
    (<cell at 0x7f8b69605378: int object at 0x7f8b695a88c0>,)
    >>>
    >>> r()
    3
    >>> r2()
    5
    >>> w(5)
    8
    >>> w2(5)
    10



Function referencing global variables does not closure
======================================================

A closure is made only if a function reference a variable in an enclosing namespace.
Not if the function reference a global variable [DmitrySoshnikov]_. ::

        global_var = 100

        def foo():
             global global_var
             def bar():
                     print(global_var)
             global_var = 5
             return bar

        b = foo()
        b()
        5

        print(b.__closure__)
        None


Function without free variables does not closure
================================================

If a function does not reference any variable in enclosing namespace, It does not create closure. ::

        def foo():
            def bar():
                 x = 3
                 print(x)
            return bar

        b = foo()
        print(b.__closure__)
        None


A closure is formed if there's most inner function
==================================================

However, if we have another inner level, then both functions save closure,
even if some parent level doesn't use free vars [DmitrySoshnikov]_. ::

        def f1(x):
            def f2(): # doesn't use free vars
              def f3(): # but "f3" does
                  return x
              return f3
            return f2

        >>> # create "f2"
        >>> f2 = f1(200)
        >>> print(f2)
        <function f2 at 0x23269b0>

        >>> # create "f3"
        >>> f3 = f2()
        >>> print (f3)
        <function f3 at 0x2326a28>

        >>> #As we expected f3 capture ''x'' in a closure
        >>> print(f3.__closure__)
        (<cell at 0x232b8a0: int object at 0x227b0a8>,)
        >>> print(f3.__closure__[0].cell_contents)
        200

        >>> #but f2 too
        >>> f2.__closure__
        (<cell at 0x232b8a0: int object at 0x227b0a8>,)
        >>> f2.__closure__[0].cell_contents
        200

.. note::

   Python capture x in one closure and both f2 and f1 access to the same closure.
   An other example to illustrate that there is only one closure per function,
   but one closure can have several cells, each cells allow to access one object reference. ::

        def L0():
            a = 3
            def L1():
                b = 4
                print("a =", a)
                def L2():
                    print("a = ", a)
                    print("b = ", b)
                return L2
            return L1

        >>> L1 = L0()
        >>> L2 = L1()
        a = 3
        >>> L2()
        a =  3
        b =  4
        >>> L1.__closure__
        (<cell at 0x15dc868: int object at 0x152ac38>,)
        >>> L2.__closure__
        (<cell at 0x15dc868: int object at 0x152ac38>, <cell at 0x15dc948: int object at 0x152ac20>)
        >>>



Python2 limitations
===================
As I said in the `introduction`_, Python 2.x has limited closures.

In the following example, there's no way I can modify `x` inside `bar`
because writing `x = bla` would declare a local `x` in `bar`, not assign to `x` of foo.
This is a side-effect of Python's assignment=declaration.

.. code-block:: python
    :linenos:

    def foo():
       x = 3
       def bar():
          print x
       x = 5
       return bar

    bar = foo()
    bar()


On the following example, As we saw in :ref:`Fundamentals of python <fundamentals>`
at *line 4* python creates a new reference object in the `bar` namespace
which mask the `x` reference object in the enclosing namespace.
Then python does not create closure (l14 & 15).

.. code-block:: python
    :linenos:

    def foo():
        x = 3
        def bar():
            x = 5
            print x
        x = 7
        print x
        return bar

    >>> bar = foo()
    7
    >>> bar()
    5
    >>> print bar.func_closure
    None

.. note::
    the attribute `__closure__` works only in Python3.
    To access to the closure in Python2 use the function property `func_closure`.

For the same reason we cannot modify the value of `x` as ut is a non mutable object.
Python create a new local reference x on the left of the statement but we try
to use it in the right part of the assignment so Python raise an error.

.. code-block:: python
    :linenos:

    def foo():
        x = 3
        def bar():
            x = x + 5
            print x
        return bar

    >>> b = foo()
    >>> b()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 4, in bar
    UnboundLocalError: local variable 'x' referenced before assignment

So in python2 there is no way to modify an non mutable object inside a closure.
We can only read it. But we can modify a mutable object.

.. code-block:: python
    :linenos:

    def foo():
        x = [1]
        def bar(y):
            x.append(y)
            return x
        return bar

    >>> b = foo()
    >>>
    >>> b(2)
    [1, 2]
    >>> b(3)
    [1, 2, 3]
    >>> b.func_closure
    (<cell at 0x10bf8d8: list object at 0x10a5518>,)
    >>> b.func_closure[0].cell_contents
    [1, 2, 3]
    >>>


.. important::

    This limitation is overcome in python3 with the new keyword `nonlocal`.
    This keyword indicate to python that this variable is in the enclosing namespace
    and it shall not create local variable when `'='` operator is used.
    In this case, Python just do an assignment not a variable creation.


When and why using closures
===========================

With a global variable
----------------------

We can use closure each time we need to have a function which keep a state.
This avoid to use the global namespace to store a state.
It' always a **bad** idea to have global variable (risk of side effect) and it's limited to instance:
I need to have a counter each time I call the function I increment the counter.

::

    _global_count = 0

    def counter():
        global _global_count
        _global_count += 1
        return _global_count

    >>> counter()
    1
    >>> counter()
    2
    >>>

#. It's dangerous to use a global variable anybody can access to the *global* count.
#. We can have only one counter.


With a closure
--------------

::

    def make_counter():
        i = 0
        def counter(): # counter() is a closure
            nonlocal i
            i += 1
            return i
        return counter

    c1 = make_counter()
    c2 = make_counter()

    print(c1(), c1(), c2(), c2())
    1 2 1 2

#. The state of the counter can be access only by the function counter. So it is protected from an illegitimate access.
#. As the data are enclosed, we can have several counter at the same time.



References
==========

.. [wikipedia] `<http://en.wikipedia.org/wiki/Closure_(computer_science)#State_representation>`_
.. [Sebastian] http://stackoverflow.com/questions/13857/can-you-explain-closures-as-they-relate-to-python
.. [Guido_van_Rossum] http://python-history.blogspot.fr/2009/04/origins-of-pythons-functional-features.html
.. [DmitrySoshnikov] 4.0 4.1 https://gist.github.com/DmitrySoshnikov/700292


Authorship
==========

:Authors: freeh4cker <freeh4cker (at) gmail.com>
:Date: |today|
