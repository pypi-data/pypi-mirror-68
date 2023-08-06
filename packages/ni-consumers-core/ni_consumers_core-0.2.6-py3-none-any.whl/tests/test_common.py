from unittest import TestCase

from .context import extract_informations


class ExtractInformationsTest(TestCase):

    def test_should_have_tags(self):
        headers = {'tags': ['cat', 'dog'],
                   'operations': ['to_save'],
                   'pipeline': 'idp',
                   'step': 'ids'}

        tags, operations,_,_ = extract_informations(headers)

        self.assertEqual(tags, ['cat', 'dog'])
        self.assertEqual(operations, ['to_save'])
