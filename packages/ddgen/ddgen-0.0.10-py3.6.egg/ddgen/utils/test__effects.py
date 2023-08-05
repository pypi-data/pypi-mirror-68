import unittest

import ddgen.utils as u


class TestEffects(unittest.TestCase):

    def test_effect_ranks(self):
        self.assertEqual(u.VARIANT_EFFECT_PRIORITIES['CHROMOSOME_NUMBER_VARIATION'], 0)  # max priority
        self.assertEqual(u.VARIANT_EFFECT_PRIORITIES['SEQUENCE_VARIANT'], 68)  # min priority

    def test_get_priority(self):
        self.assertEqual(u.get_variant_effect_priority('EXON_LOSS_VARIANT'), 2)
        self.assertEqual(u.get_variant_effect_priority('TRANSLOCATION'), 5)
        self.assertEqual(u.get_variant_effect_priority('MISSENSE_VARIANT'), 21)
        self.assertEqual(u.get_variant_effect_priority('gibberish'), -1)
        self.assertEqual(u.get_variant_effect_priority(''), -1)
