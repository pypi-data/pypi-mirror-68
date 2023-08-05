***********
Assert Info
***********

Assert Info fixes up bare assert statements in your code so they include diagnostics when
they they're hit.

A problem that crops up when working in legacy code bases is the use of ``assert X == Y``,
when this fails you get minimal diagnostics.

Whilst `Pytest <https://docs.pytest.org/en/latest/>`_ solves this by playing with AST at run
time, inserting diagnostics on the fly, you can't just run all your code with `Pytest`.

The standard libraries `unittest <https://docs.python.org/3/library/unittest.html>`_ solves
this problem with helper functions that include extra diagnostics by default, for instance
``assertEqual``.

This package will inspect any file and replace assert statement which aren't accompanied
by a message with a `unittest` style assertion so that when it fails you get diagnostics!

To run the script:

.. code-block:: shell

    pip install assert-info
    assert-info -h
