import unittest

from ddgen.utils import prioritize_refseq_transcripts


class TestTranscripts(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_min_transcripts(self):
        txs = ['NM_123.4', 'NM_124.4', 'NM_1001.2']
        tx = prioritize_refseq_transcripts(txs)
        self.assertEqual(tx, 'NM_123.4')

    def test_min_transcripts_multiple_sources(self):
        txs = ['NM_123.4', 'NR_123.4', 'XM_123.4', 'XR_123.4']
        tx = prioritize_refseq_transcripts(txs)
        self.assertEqual(tx, 'NM_123.4')

        txs = ['NR_123.4', 'XM_123.4', 'XR_123.4']
        tx = prioritize_refseq_transcripts(txs)
        self.assertEqual(tx, 'XM_123.4')

        txs = ['NR_123.4', 'XR_123.4']
        tx = prioritize_refseq_transcripts(txs)
        self.assertEqual(tx, 'NR_123.4')

        txs = ['XR_123.4']
        tx = prioritize_refseq_transcripts(txs)
        self.assertEqual(tx, 'XR_123.4')
