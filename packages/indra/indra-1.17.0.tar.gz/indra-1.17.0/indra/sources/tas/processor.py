from __future__ import absolute_import, print_function, unicode_literals
from builtins import dict, str

__all__ = ['TasProcessor']

from indra.statements import Inhibition, Agent, Evidence
from indra.databases import hgnc_client, chebi_client
from indra.databases.lincs_client import LincsClient


CLASS_MAP = {'1': 'Kd < 100nM', '2': '100nM < Kd < 1uM',
             '3': '1uM < Kd < 10uM', '10': 'Kd > 10uM'}


class TasProcessor(object):
    """A processor for the Target Affinity Spectrum data table."""
    def __init__(self, data, affinity_class_limit):
        self._data = data
        self._lc = LincsClient()
        self.affinity_class_limit = affinity_class_limit

        self.statements = []
        for row in data:
            # Skip rows that are above the affinity class limit
            if int(row['class_min']) > affinity_class_limit:
                continue
            self._process_row(row)
        return

    def _process_row(self, row):
        drug = self._extract_drug(row['hms_id'])
        prot = self._extract_protein(row['approved_symbol'], row['gene_id'])
        ev = self._make_evidence(row['class_min'])
        # NOTE: there are several entries in this data set that refer to
        # non-human Entrez genes, e.g.
        # https://www.ncbi.nlm.nih.gov/gene/3283880
        # We skip these for now because resources for Entrez-based
        # mappings for non-human genes are not integrated, and would cause
        # pre-assembly issues.
        if 'HGNC' not in prot.db_refs:
            return
        self.statements.append(Inhibition(drug, prot, evidence=ev))

    def _extract_drug(self, hms_id):
        refs = self._lc.get_small_molecule_refs(hms_id)
        name = self._lc.get_small_molecule_name(hms_id)
        if 'PUBCHEM' in refs:
            chebi_id = chebi_client.get_chebi_id_from_pubchem(refs['PUBCHEM'])
            if chebi_id:
                refs['CHEBI'] = 'CHEBI:%s' % chebi_id
        return Agent(name, db_refs=refs)

    def _extract_protein(self, name, gene_id):
        refs = {'EGID': gene_id}
        hgnc_id = hgnc_client.get_hgnc_from_entrez(gene_id)
        if hgnc_id is not None:
            refs['HGNC'] = hgnc_id
            up_id = hgnc_client.get_uniprot_id(hgnc_id)
            if up_id:
                refs['UP'] = up_id
            # If there is a HGNC ID, we standardize the gene name
            name = hgnc_client.get_hgnc_name(hgnc_id)
        return Agent(name, db_refs=refs)

    def _make_evidence(self, class_min):
        ev = Evidence(source_api='tas', epistemics={'direct': True},
                      annotations={'class_min': CLASS_MAP[class_min]})
        return ev
