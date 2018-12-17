from datetime import datetime, date

from django.test import TestCase

from toolcommon.jsonblitz import dumps, loads


class JsonblitzTestCase(TestCase):
    def test_DumpAndLoadDefault_values(self):
        data = {
            u'int_value': 123,
            u'float_value': 12.3,
            u'str_value': u'string value',
            u'null_value': None,
            u'dict_value': {
                u'int_value': 321,
                u'str_value': u'string value 2'
            },
            u'array_value': [
                1,
                3.2,
                u'str_value',
                {u'int_value': 2},
                None,
            ]
        }

        decoded = dumps(data)
        encoded = loads(decoded)

        self.assertEqual(data, encoded)

    def test_DumpAndLoadDatetime_OK(self):
        data = {
            'dt': datetime.now(),
            'dtutc': datetime.utcnow(),
            'd': date.today(),
        }

        decoded = dumps(data)
        encoded = loads(decoded)

        self.assertEqual(data, encoded)
