import logging

from pkg_resources import resource_filename

HG19 = ('hg19', 'grch37')
HG38 = ('hg38', 'grch38')


class GenomeIntervalGenerator:

    def __init__(self, genome_dict: str):
        """

        :param genome_dict: path to genome dict file, or
        """
        if genome_dict.lower() in HG19:
            dict_path = resource_filename(__name__, 'data/hg19.dict')
        elif genome_dict.lower() in HG38:
            dict_path = resource_filename(__name__, 'data/hg38.dict')
        else:
            dict_path = genome_dict

        self._seq_dict = SeqDict(dict_path)
        self._logger = logging.getLogger(__name__)

    def get_regions(self, region_size, contigs: iter = 'all'):
        """
        Get generator of regions with requested size.

        :param contigs: iterable with contig names to generate regions for
        :param region_size:
        :return: generator that generates tuples, such as ('chr1', 1, 100), when `region_size = 100`
        """
        # check input sanity first
        if contigs == 'all':
            _contigs = self.get_known_contigs()
        elif isinstance(contigs, (list, set, tuple)):
            _contigs = contigs
        else:
            msg = "Expected list/set/tuple with contig names or 'all', got {}".format(type(contigs))
            self._logger.error(msg)
            raise ValueError(msg)

        # then return the generator
        return self._get_generator(region_size, _contigs)

    def _get_generator(self, region_size, contigs):
        for cont in contigs:
            b = 1
            e = region_size
            while e < self._seq_dict.contig_dict[cont].length:
                yield (cont, b, e)
                b = e + 1
                e += region_size
            else:
                yield (cont, b, self._seq_dict.contig_dict[cont].length)

    def get_known_contigs(self) -> tuple:
        """Get alphabetically sorted tuple with known contigs."""
        return tuple(sorted(self._seq_dict.contig_dict.keys()))


class SeqDict:

    def __init__(self, dict_path: str):
        """
        :param: dict_path - path to sequence dictionary file
        """
        self.contig_dict = dict()
        with open(dict_path) as fh:
            for line in fh:
                if not line.startswith("@SQ"):
                    continue
                sde = SeqDictEntry(line)
                self.contig_dict[sde.name] = sde


class SeqDictEntry(object):

    def __init__(self, line: str):
        """
        :param:
        """
        entry = line.strip().split("\t")
        if (len(entry)) < 5:
            raise Exception("Invalid line '{}'!".format(line))

        self.type = entry[0]  # "@SQ"
        self.name = entry[1][3:]  # "SN:chr10" -> "chr10"
        self.length = int(entry[2][3:])  # "LN:248956422" -> 248956422
        self.m5 = entry[3][3:]  # "M5:862f5" -> "862f5"
        self.ur = entry[4][
                  3:]  # "UR:file:///home/ielis/genomes/hg38/hg38.fa" -> "file:///home/ielis/genomes/hg38/hg38.fa"

    def __str__(self):
        return ", ".join([self.type, self.name, str(self.length), self.m5, self.ur])
