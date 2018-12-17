from django.test import TestCase
from os import remove

from blitz import resources_env


class GetStuffChoicesTestCase(TestCase):
    def setUp(self):
        self.stuff_files = {
            "new_stuff.xml": """
                <root>
                  <nextAvailableId>236</nextAvailableId>
                  <stuff name="lightSign">
                    <id>1</id>
                  </stuff>
                  <stuff name="darkSeal">
                    <id>2</id>
                  </stuff>
                  <stuff name="part_for_fusion">
                    <id>3</id>
                  </stuff>
                  <stuff name="certificate">
                    <id>4</id>
                  </stuff>
                </root>
            """,
            "old_stuff.xml": """
                <root>
                  <nextAvailableId>236</nextAvailableId>
                  <lightSign>
                    <id>1</id>
                  </lightSign>
                  <darkSeal>
                    <id>2</id>
                  </darkSeal>
                  <part_for_fusion>
                    <id>3</id>
                  </part_for_fusion>
                  <certificate>
                    <id>4</id>
                  </certificate>
                </root>
            """

        }

        for file_path, text in self.stuff_files.iteritems():
            with open(file_path, 'w') as f:
                f.write(text)

        self.expected_result = [('certificate', u'certificate - certificate id 4'),
                                ('darkSeal', u'darkSeal - darkSeal id 2'),
                                ('lightSign', u'lightSign - lightSign id 1'),
                                ('part_for_fusion', u'part_for_fusion - part_for_fusion id 3')]

    def tearDown(self):
        for file_path in self.stuff_files:
            remove(file_path)

    def test_get_choices(self):
        for file_path in self.stuff_files:
            choices = resources_env.get_stuff_choices(file_path)
            self.assertEqual(choices, self.expected_result)

