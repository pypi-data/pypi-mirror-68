import re
import typing

_tx_priorities = {
    'NM_': 1,
    'XM_': 2,
    'NR_': 3,
    'XR_': 4
}


def prioritize_refseq_transcripts(txs: typing.Union[list, tuple, set]):
    """RefSeq transcripts have following categories: {NM_, XM_, NR_, XR_}.
    If we have transcripts from multiple sources, we want to select the one coming from the source with highest priority.
    E.g. `NM_` has higher priority than `XM_`.

    If we have multiple transcripts from a single source, we want to select the one with smaller integer.
    E.g. `NM_123.4` has higher priority than `NM_124.4`.
    :param txs: iterable with transcript accession id strings

    """
    priorities = [_tx_priorities[tx[:3]] for tx in txs if tx[:3] in _tx_priorities]
    if priorities:
        max_observed_priority = min(priorities)  # lower number has higher priority
        if max_observed_priority == 1:
            # we have at least single `NM_` transcript
            nms = [tx for tx in txs if tx.startswith('NM_')]
            if len(nms) == 1:
                return nms[0]
            else:
                return _find_max_priority_within_single_source(nms, 'NM_')

        elif max_observed_priority == 2:
            # we have at least single `NM_` transcript
            xms = [tx for tx in txs if tx.startswith('XM_')]
            if len(xms) == 1:
                return xms[0]
            else:
                return _find_max_priority_within_single_source(xms, 'XM_')
        elif max_observed_priority == 3:
            # we have at least single `NR_` transcript
            nrs = [tx for tx in txs if tx.startswith('NR_')]
            if len(nrs) == 1:
                return nrs[0]
            else:
                return _find_max_priority_within_single_source(nrs, 'NR_')
        elif max_observed_priority == 4:
            # we have at least single `NR_` transcript
            xrs = [tx for tx in txs if tx.startswith('XR_')]
            if len(xrs) == 1:
                return xrs[0]
            else:
                return _find_max_priority_within_single_source(xrs, 'XR_')

    else:
        return None


def _find_max_priority_within_single_source(txs, source):
    if len(txs) != 0:
        if len(txs) == 1:
            # there is a single transcript that starts with `source`
            return txs[0]
        else:
            # multiple `source` transcripts
            pt = re.compile("{}(?P<number>\d+)\.(?P<subscript>\d*)".format(source))
            numbers = [int(pt.match(tx).group('number')) for tx in txs]
            min_number = min(numbers)
            min_idx = numbers.index(min_number)
            return txs[min_idx]
    else:
        return None
