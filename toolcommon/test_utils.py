from django.test import TestCase

from toolcommon.utils import cached_value, get_unique_name, make_https_host


class UtilsTestCase(TestCase):
    def test_CachedValue_Ok(self):
        called = []

        @cached_value
        def get_cached_value(value1, value2):
            called.append((value1, value2))
            return len(called)

        self.assertEqual(len(called), 0)

        self.assertEqual(get_cached_value(None, None), 1)
        self.assertEqual(len(called), 1)

        self.assertEqual(get_cached_value(None, 1), 2)
        self.assertEqual(len(called), 2)

        self.assertEqual(get_cached_value(1, 1), 3)
        self.assertEqual(len(called), 3)

        self.assertEqual(get_cached_value(1, 1), 3)
        self.assertEqual(len(called), 3)

    def test_GetUniqueName_Ok(self):
        name = get_unique_name("name_base_{}")

        self.assertTrue(name.startswith("name_base_"))
        self.assertNotEqual(get_unique_name("name_base_{}"), get_unique_name("name_base_{}"))

    def test_MakeHttpHost_Ok(self):
        host = make_https_host('git.io')
        self.assertEqual(host, 'https://git.io')

        host = make_https_host(None)
        self.assertIsNone(host)

        host = make_https_host('https://git.io')
        self.assertEqual(host, 'https://git.io')