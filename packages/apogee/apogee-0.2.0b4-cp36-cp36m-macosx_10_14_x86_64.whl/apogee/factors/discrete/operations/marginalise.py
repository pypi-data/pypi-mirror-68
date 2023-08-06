"""
The MIT License

Copyright (c) 2017-2020 Mark Douthwaite

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import numpy as np

import apogee.core as ap


def factor_marginalise(a, v):
    """
    Marginalise out the variable 'v' from factor 'a'.

    Parameters
    ----------
    a: Factor-like
        The target factor-like object.
    v: int/any
        The identifier of the variable to be marginalised out.

    Returns
    -------
    scope: ndarray
        An array containing the scope of the resulting factor.
    card: ndarray
        An array containing the cardinality of the resulting factor.
    vals: ndarray
        An array containing the probability distribution of the resulting factor.

    Examples
    --------
    >>> a = Factor([0], [2], [0.1, 0.9])
    >>> b = Factor([1, 0], [2, 2], [[0.2, 0.8], [0.7, 0.3]])
    >>> c = Factor(*factor_marginalise(a, 0))  # generate new factor from factors a and b
        {0: {0: 0.5, 1: 0.5}, 1: {0: 0.25, 1: 0.75}}

    """

    scope = a.scope[
        np.where(a.scope != v)
    ]  # extract remaining variables from scope scope.
    f_map = ap.index_map_1d(
        a.scope, scope
    )  # create a new map of old scope given new scope.
    card = a.cards[f_map]  # extract cardinality of remaining variables

    assignments = ap.cartesian_product(
        *[np.arange(x) for x in card]
    )  # compute assignments only once.
    f_idx = ap.array_index(
        a.assignments[:, f_map], assignments
    )  # extract indices to be combined.

    values = np.zeros(len(assignments), dtype=np.float64)

    avals = a.parameters
    for i in range(len(a.assignments)):
        if values[f_idx[i]] is None:
            values[f_idx[i]] = avals[i]
        else:
            values[f_idx[i]] += avals[i]

    return scope, card, values
