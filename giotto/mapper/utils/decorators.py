"""Convenience class decorators for use in a Mapper context."""
# License: GNU AGPLv3

from sklearn.base import TransformerMixin


def method_to_transform(cls, method_name):
    """Wrap a class to add a :meth:`transform`method as an alias to an
    existing method.

    An example of use is for classes possessing a :meth:`score` method such
    as kernel density estimators and anomaly/novelty detection estimators,
    to allow for these estimators are to be used as steps in a pipeline.

    Parameters
    ----------
    cls : object
        Class to be wrapped. If `method_name` is not one of its methods,
        :meth:`transform` always returns ``None``.

    method_name : str
        Name of the method in `cls` to which :meth:`transform` will be
        an alias. The fist argument of this method becomes the `X`
        input for :meth:`transform`.

    Returns
    -------
    wrapped_cls : object
        New class inheriting from :class:`sklearn.base.TransformerMixin`,
        so that a :meth:`fit_transform` is also available. Its name is the
        name of `cls` prepended with ``'Extended'``.

    Examples
    --------
    >>> import numpy as np
    >>> from numpy.testing import assert_almost_equal
    >>> from sklearn.neighbors import KernelDensity
    >>> from giotto.mapper import method_to_transform
    >>> X = np.random.random((100, 2))
    >>> kde = KernelDensity()
    >>> kde_extended = method_to_transform(
    ...     KernelDensity, 'score_samples')()
    >>> Xt = kde.fit(X).score_samples(X)
    >>> Xt_extended = kde_extended.fit_transform(X)
    >>> assert_almost_equal(Xt, Xt_extended)
    True

    """
    def wrapper(wrapped):
        class ExtendedEstimator(wrapped, TransformerMixin):
            def transform(self, X, y=None):
                has_method = hasattr(self, method_name)
                if has_method:
                    return getattr(self, method_name)(X)
        ExtendedEstimator.__name__ = 'Extended' + wrapped.__name__
        return ExtendedEstimator
    wrapped_cls = wrapper(cls)
    return wrapped_cls
