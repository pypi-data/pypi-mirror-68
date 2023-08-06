
.. include:: /project-links.txt
.. include:: /abbreviation.txt



.. getthecode:: full-test.py
    :language: python3
    :hidden:

.. note::
   You can see the source by clicking on the eye

.. code-block:: py3

    
    # A source code comment
    ##
    ###
    
    foo = 1
    

==========================
 A Restructuredtext Title
==========================

.. code-block:: py3

    
    foo = 1
    


Some reStructuredText contents

Some Markdown contents

`An inline-style link <https://www.python.org>`__

.. code-block:: py3

    
    foo = 1
    
    # Insert the output of the following python code
    print(foo)


.. code-block:: none

    1
    


.. code-block:: py3

    
    foo = 1
    
    # Hidden Python code


.. code-block:: py3

    
    foo = 1
    

Format RST content with current locals dictionary using @<@...@>@ instead of {...}.

.. math::

    I_d = 369 I_s \left( e^{\frac{V_d}{n V_T}} - 1 \right)


.. code-block:: py3

    
    # Add Python code as a literal block


.. code-block:: py

    for x in ():
      1 / 0 / 0


.. code-block:: py3

    
    # Interactive code


.. code-block:: py3

    1 + 1


.. code-block:: none

    2


.. code-block:: py3

    2 * 4 * 2


.. code-block:: none

    16


.. code-block:: py3

    a, b = 1, 2


.. code-block:: none



.. code-block:: py3

    1, 2, 3


.. code-block:: none

    (1, 2, 3)


.. code-block:: py3

    
    # Guarded error


.. code-block:: py3

    1/0

.. code-block:: pytb

    ZeroDivisionError division by zero
    [0;31m---------------------------------------------------------------------------[0m
    [0;31mZeroDivisionError[0m                         Traceback (most recent call last)
    [0;32m~/home/developpement/python/pyterate/examples/document-generator/full-test.py[0m in [0;36m<module>[0;34m[0m
    [0;32m----> 1[0;31m [0;36m1[0m[0;34m/[0m[0;36m0[0m[0;34m[0m[0;34m[0m[0m
    [0m
    [0;31mZeroDivisionError[0m: division by zero


.. code-block:: py3

    
    # Add a Python file as a literal block


.. getthecode:: RingModulator.py
    :language: py3


.. code-block:: py3

    
    # Add the file content as literal block


.. literalinclude:: kicad-pyspice-example.cir


.. code-block:: py3

    
    # Insert an image


.. image:: kicad-pyspice-example.sch.svg
    :align: center


.. code-block:: py3

    
    # Insert Circuit_macros diagram


.. image:: circuit.png
    :align: center


.. code-block:: py3

    
    # Insert Tikz figure


.. image:: diode.svg
    :align: center
    :width: 600


.. code-block:: py3

    
    import numpy as np
    import matplotlib.pyplot as plt
    figure = plt.figure(1, (20, 10))
    x = np.arange(1, 10, .1)
    y = np.sin(x)
    plt.plot(x, y)
    
    # Insert a Matplotlib figure


.. image:: my-figure.png
    :align: center
    :width: 1280


.. code-block:: py3

    
    # Insert a table
    N = 2
    x = np.arange(-N, N, 0.5)
    y = np.arange(-N, N, 0.5)
    xx, yy = np.meshgrid(x, y, sparse=True)
    z = np.sin(xx**2 + yy**2) / (xx**2 + yy**2)

==== ==== ==== ==== ==== ==== ==== ====
 0.1 -0.0 -0.2 -0.2 -0.2 -0.2 -0.2 -0.0
-0.0 -0.2 -0.0  0.2  0.3  0.2 -0.0 -0.2
-0.2 -0.0  0.5  0.8  0.8  0.8  0.5 -0.0
-0.2  0.2  0.8  1.0  1.0  1.0  0.8  0.2
-0.2  0.3  0.8  1.0  nan  1.0  0.8  0.3
-0.2  0.2  0.8  1.0  1.0  1.0  0.8  0.2
-0.2 -0.0  0.5  0.8  0.8  0.8  0.5 -0.0
-0.0 -0.2 -0.0  0.2  0.3  0.2 -0.0 -0.2
==== ==== ==== ==== ==== ==== ==== ====

====== ====== ====== ====== ====== ====== ====== ======
     A      B      C      D      E      F      G      H
====== ====== ====== ====== ====== ====== ====== ======
 0.124 -0.005 -0.192 -0.211 -0.189 -0.211 -0.192 -0.005
-0.005 -0.217 -0.033  0.239  0.346  0.239 -0.033 -0.217
-0.192 -0.033  0.455  0.759  0.841  0.759  0.455 -0.033
-0.211  0.239  0.759  0.959  0.990  0.959  0.759  0.239
-0.189  0.346  0.841  0.990    nan  0.990  0.841  0.346
-0.211  0.239  0.759  0.959  0.990  0.959  0.759  0.239
-0.192 -0.033  0.455  0.759  0.841  0.759  0.455 -0.033
-0.005 -0.217 -0.033  0.239  0.346  0.239 -0.033 -0.217
====== ====== ====== ====== ====== ====== ====== ======


.. code-block:: py3

    
    foo = 1

