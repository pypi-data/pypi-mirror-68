import inspect

from django.test import TestCase
from django.urls import resolve, reverse


class URLTestMixin(object):
    def assert_url_matches_view(self, view, expected_url, url_name,
                                url_args=None, url_kwargs=None, urlconf=None):
        """
        Assert a view's url is correctly configured

        Check the url_name reverses to give a correctly formated expected_url.
        Check the expected_url resolves to the expected view.
        """

        reversed_url = reverse(
            url_name,
            urlconf=urlconf,
            args=url_args,
            kwargs=url_kwargs,
        )
        self.assertEqual(reversed_url, expected_url)

        resolved_view = resolve(expected_url, urlconf=urlconf).func
        self.assertEqual(
            (resolved_view.__module__, resolved_view.__name__),
            (view.__module__, view.__name__),
        )

        message = 'Resolved view `{}` is a class. Did you forget `.as_view()`?'
        self.assertFalse(
            inspect.isclass(resolved_view),
            message.format(resolved_view),
        )


class URLTestCase(URLTestMixin, TestCase):
    pass
