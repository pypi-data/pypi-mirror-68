from unittest import TestCase

from .context import extract_informations


class ExtractInformationsTest(TestCase):

    def test_should_have_tags(self):
        headers = {'params': {'tags': ['cat', 'dog']},
                   'operations': ['to_save'],
                   'pipeline': 'idp',
                   'step': 'ids'}

        params, operations,_,_ = extract_informations(headers)

        self.assertEqual(params, {'tags': ['cat', 'dog']})
        self.assertEqual(operations, ['to_save'])
