Description
===========

gen-distinct-terminal-colors is a simple script made to select a list of
terminal colors that are sufficiently visually distinct. This can be useful for
e.g. setting your IRC client's nickname colors.

The output isn't perfect (especially for larger output sizes), but should give
a good starting point.

Note that this script highly depends on
[termcolors](https://github.com/dranjan/termcolors) to get your terminal's
supported colors. Please see the project's page for compatibility notes with
different terminals.

Usage
=====

Syntax:

    python gen-distinct-terminal-colors.py <output size>

For example, to get a list of 16 visually distinct colors:

    python gen-distinct-terminal-colors.py 16

Dependencies
============

- [colormath](https://pypi.org/project/colormath/)
- [numpy](https://pypi.org/project/numpy/)
- [scikit-learn](https://pypi.org/project/scikit-learn/)
- [scipy](https://pypi.org/project/scipy/)
- [termcolors](https://github.com/dranjan/termcolors)
- [wcag-contrast-ratio](https://pypi.org/project/wcag-contrast-ratio/)

Dependencies can be installed easily using `pip install --user -r
requirements.txt`.

Screenshot
==========

![Screenshot](https://raw.githubusercontent.com/GermainZ/gen-distinct-terminal-colors/master/screenshot.png "Screenshot")
