=====
pyh2m
=====


.. image:: https://img.shields.io/pypi/v/h2m.svg
        :target: https://pypi.python.org/pypi/h2m


simple and flexible html to markdown python converter


h2m.feed('''<h1>Level One Heading</h1>''')

assert h2m.md() == '''# Level One Heading'''

h2m.feed('''<h2>Level Two Heading</h2>''')

assert h2m.md() == '''## Level Two Heading'''

h2m.feed('''<h3>Level Three Heading</h3>''')

assert h2m.md() == '''### Level Three Heading'''


* Free software: MIT license


Features
--------

* TODO Tables of gov

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
