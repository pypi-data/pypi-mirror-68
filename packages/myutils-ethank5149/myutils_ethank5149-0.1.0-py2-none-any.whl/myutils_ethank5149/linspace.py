"""Docstring for the example.py module.
# @file pyroot.py
# @brief Finds root of a given function.
#
# Allows implementation of a number of methods to find a root
# of a univariate function.
#
# @author Ethan Knox(ethank5149)
# @bug No known bugs.

Modules names should have short, all-lowercase names.  The module name may
have underscores if this improves readability.

Every module should have a docstring at the very top of the file.  The
module's docstring may extend over multiple lines.  If your docstring does
extend over multiple lines, the closing three quotation marks must be on
a line by itself, preferably preceded by a blank line.

"""


# Global Definitions
EPS = 2.22044604925e-16
ZERO = 1e-14


def main(start, stop, n):
    """linspace(start, stop, n) -> linearly spaced range of n numbers from
    start to stop

    Return a virtual sequence of num numbers from start to stop (inclusive).

    """
    if not isinstance(n, int) or n <= 1:
        raise ValueError('n must be an integer > 1')
    step = (stop-start)/(n-1)
    output = [start]
    for i in range(1, n):
        output.append(output[-1]+step)
    return output


def sign(a): return 1 if a >= 0 else -1.0