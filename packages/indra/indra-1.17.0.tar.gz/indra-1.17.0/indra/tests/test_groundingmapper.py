from indra.preassembler.grounding_mapper import default_mapper as gm
from indra.preassembler.grounding_mapper import GroundingMapper
from indra.preassembler.grounding_mapper.analysis import *
from indra.preassembler.grounding_mapper.gilda import ground_statements, \
    get_gilda_models, ground_statement
from indra.preassembler.grounding_mapper.standardize import \
    standardize_agent_name, standardize_db_refs
from indra.statements import Agent, Phosphorylation, Complex, Inhibition, \
    Evidence, BoundCondition
from indra.util import unicode_strs
from nose.tools import raises
from nose.plugins.attrib import attr


def test_simple_mapping():
    akt = Agent('pkbA', db_refs={'TEXT': 'Akt', 'UP': 'XXXXXX'})
    stmt = Phosphorylation(None, akt)
    mapped_stmts = gm.map_stmts([stmt])
    assert len(mapped_stmts) == 1
    mapped_akt = mapped_stmts[0].sub
    assert mapped_akt.db_refs['TEXT'] == 'Akt'
    assert mapped_akt.db_refs['FPLX'] == 'AKT'
    assert unicode_strs((akt, stmt, gm, mapped_akt))


def test_map_standardize_up_hgnc():
    a1 = Agent('MAPK1', db_refs={'HGNC': '6871'})
    a2 = Agent('MAPK1', db_refs={'UP': 'P28482'})
    stmt = Phosphorylation(a1, a2)
    mapped_stmts = gm.map_stmts([stmt])
    assert len(mapped_stmts) == 1
    st = mapped_stmts[0]
    assert st.enz.db_refs['HGNC'] == st.sub.db_refs['HGNC']
    assert st.enz.db_refs['UP'] == st.sub.db_refs['UP']


def test_map_standardize_chebi_pc():
    a1 = Agent('X', db_refs={'PUBCHEM': '42611257'})
    a2 = Agent('Y', db_refs={'CHEBI': 'CHEBI:63637'})
    stmt = Phosphorylation(a1, a2)
    mapped_stmts = gm.map_stmts([stmt])
    assert len(mapped_stmts) == 1
    st = mapped_stmts[0]
    assert st.enz.db_refs['PUBCHEM'] == st.sub.db_refs['PUBCHEM'], \
        (st.enz.db_refs, st.sub.db_refs)
    assert st.enz.db_refs['CHEBI'] == st.sub.db_refs['CHEBI'], \
        (st.enz.db_refs, st.sub.db_refs)
    assert st.enz.name == 'vemurafenib'
    assert st.sub.name == 'vemurafenib'


def test_map_standardize_chebi_hmdb():
    a1 = Agent('X', db_refs={'HMDB': 'HMDB0000122'})
    a2 = Agent('Y', db_refs={'CHEBI': 'CHEBI:4167'})
    stmt = Phosphorylation(a1, a2)
    mapped_stmts = gm.map_stmts([stmt])
    assert len(mapped_stmts) == 1
    st = mapped_stmts[0]
    assert st.enz.db_refs['CHEBI'] == st.sub.db_refs['CHEBI'], \
        (st.enz.db_refs, st.sub.db_refs)
    assert st.enz.name == 'D-glucopyranose', st.enz
    assert st.sub.name == 'D-glucopyranose', st.sub


def test_bound_condition_mapping():
    # Verify that the grounding mapper grounds the agents within a bound
    # condition
    akt = Agent('pkbA', db_refs={'TEXT': 'Akt', 'UP': 'XXXXXX'})
    erk = Agent('ERK1', db_refs={'TEXT': 'ERK1'})
    akt.bound_conditions = [BoundCondition(erk)]

    stmt = Phosphorylation(None, akt)

    mapped_stmts = gm.map_stmts([stmt])

    s = mapped_stmts[0]
    mapped_akt = mapped_stmts[0].sub
    mapped_erk = mapped_akt.bound_conditions[0].agent

    assert mapped_akt.db_refs['TEXT'] == 'Akt'
    assert mapped_akt.db_refs['FPLX'] == 'AKT'

    assert mapped_erk.db_refs['TEXT'] == 'ERK1'
    assert mapped_erk.db_refs['HGNC'] == '6877'
    assert mapped_erk.db_refs['UP'] == 'P27361'


def test_bound_condition_mapping_multi():
    # Test with multiple agents
    akt = Agent('pkbA', db_refs={'TEXT': 'Akt', 'UP': 'XXXXXX'})
    erk = Agent('ERK1', db_refs={'TEXT': 'ERK1'})
    akt.bound_conditions = [BoundCondition(erk)]
    stmt = Phosphorylation(akt, erk)
    mapped_stmts = gm.map_stmts([stmt])
    s = mapped_stmts[0]
    mapped_akt = mapped_stmts[0].enz
    mapped_erk1 = mapped_akt.bound_conditions[0].agent
    mapped_erk2 = mapped_stmts[0].sub

    assert mapped_akt.db_refs['TEXT'] == 'Akt'
    assert mapped_akt.db_refs['FPLX'] == 'AKT'

    for e in (mapped_erk1, mapped_erk2):
        assert e.db_refs['TEXT'] == 'ERK1'
        assert e.db_refs['HGNC'] == '6877'
        assert e.db_refs['UP'] == 'P27361'


def test_bound_condition_mapping_agent_json():
    # Test with agent/json mapping
    akt = Agent('pkbA', db_refs={'TEXT': 'p-Akt', 'UP': 'XXXXXX'})
    erk = Agent('ERK1', db_refs={'TEXT': 'ERK1'})
    akt.bound_conditions = [BoundCondition(erk)]
    stmt = Phosphorylation(None, akt)

    mapped_stmts = gm.map_stmts([stmt])

    s = mapped_stmts[0]
    mapped_akt = mapped_stmts[0].sub
    mapped_erk = mapped_akt.bound_conditions[0].agent

    #assert mapped_akt.db_refs['TEXT'] == 'p-AKT', mapped_akt.db_refs
    assert mapped_akt.db_refs['FPLX'] == 'AKT', mapped_akt.db_refs

    assert mapped_erk.db_refs['TEXT'] == 'ERK1'
    assert mapped_erk.db_refs['HGNC'] == '6877'
    assert mapped_erk.db_refs['UP'] == 'P27361'


def test_ignore():
    agent = Agent('FA', db_refs={'TEXT': 'FA'})
    stmt = Phosphorylation(None, agent)
    mapped_stmts = gm.map_stmts([stmt])
    assert len(mapped_stmts) == 0


def test_renaming():
    akt_indra = Agent('pkbA', db_refs={'TEXT': 'Akt', 'FPLX': 'AKT family',
                                       'UP': 'P31749'})
    akt_hgnc_from_up = Agent('pkbA', db_refs={'TEXT': 'Akt', 'UP': 'P31749'})
    akt_other = Agent('pkbA', db_refs={'TEXT': 'Akt'})
    tat_up_no_hgnc = Agent('foo', db_refs={'TEXT': 'bar', 'UP': 'P04608'})
    stmts = [Phosphorylation(None, akt_indra),
             Phosphorylation(None, akt_hgnc_from_up),
             Phosphorylation(None, akt_other),
             Phosphorylation(None, tat_up_no_hgnc), ]
    renamed_stmts = gm.rename_agents(stmts)
    assert len(renamed_stmts) == 4
    # Should draw on BE first
    assert renamed_stmts[0].sub.name == 'AKT family'
    # Then on the HGNC lookup from Uniprot
    assert renamed_stmts[1].sub.name == 'AKT1', renamed_stmts[1].sub.name
    # Don't fall back on text if there's no grounding
    assert renamed_stmts[2].sub.name == 'pkbA'
    assert renamed_stmts[3].sub.name == 'tat'
    assert unicode_strs((akt_indra, akt_hgnc_from_up, akt_other,
                         tat_up_no_hgnc, stmts, gm, renamed_stmts))


def test_save_sentences_unicode():
    mek = Agent('MEK', db_refs={'TEXT': 'MAP2K1'})
    ev = Evidence(source_api='reach', pmid='PMID000asdf',
                  text='foo\U0001F4A9bar')
    st = Phosphorylation(None, mek, evidence=[ev])
    sent = get_sentences_for_agent('MAP2K1', [st])
    assert unicode_strs(sent)
    twg = agent_texts_with_grounding([st])
    save_sentences(twg, [st], 'test_save_sentences.csv')


def test_hgnc_sym_but_not_up():
    erk = Agent('ERK1', db_refs={'TEXT': 'ERK1'})
    stmt = Phosphorylation(None, erk)
    g_map = {'ERK1': {'TEXT': 'ERK1', 'HGNC': '6871'}}
    gm = GroundingMapper(g_map)
    mapped_stmts = gm.map_stmts([stmt])
    assert len(mapped_stmts) == 1
    mapped_erk = mapped_stmts[0].sub
    assert mapped_erk.name == 'MAPK1'
    assert mapped_erk.db_refs['TEXT'] == 'ERK1'
    assert mapped_erk.db_refs['HGNC'] == '6871'
    assert mapped_erk.db_refs['UP'] == 'P28482'
    assert unicode_strs((erk, stmt, gm, mapped_stmts, mapped_erk))


def test_up_but_not_hgnc():
    erk = Agent('ERK1', db_refs={'TEXT': 'ERK1'})
    stmt = Phosphorylation(None, erk)
    g_map = {'ERK1': {'TEXT': 'ERK1', 'UP': 'P28482'}}
    gm = GroundingMapper(g_map)
    mapped_stmts = gm.map_stmts([stmt])
    assert len(mapped_stmts) == 1
    mapped_erk = mapped_stmts[0].sub
    assert mapped_erk.name == 'MAPK1'
    assert mapped_erk.db_refs['TEXT'] == 'ERK1'
    assert mapped_erk.db_refs['HGNC'] == '6871'
    assert mapped_erk.db_refs['UP'] == 'P28482'
    assert unicode_strs((erk, stmt, gm, mapped_stmts, mapped_erk))


def test_hgnc_but_not_up():
    erk = Agent('ERK1', db_refs={'TEXT': 'ERK1'})
    stmt = Phosphorylation(None, erk)
    g_map = {'ERK1': {'TEXT': 'ERK1', 'HGNC': '6871'}}
    gm = GroundingMapper(g_map)
    mapped_stmts = gm.map_stmts([stmt])
    assert len(mapped_stmts) == 1
    mapped_erk = mapped_stmts[0].sub
    assert mapped_erk.name == 'MAPK1'
    assert mapped_erk.db_refs['TEXT'] == 'ERK1'
    assert mapped_erk.db_refs['HGNC'] == '6871'
    assert mapped_erk.db_refs['UP'] == 'P28482'
    assert unicode_strs((erk, stmt, gm, mapped_stmts, mapped_erk))


@raises(ValueError)
def test_hgnc_sym_with_no_id():
    erk = Agent('ERK1', db_refs={'TEXT': 'ERK1'})
    stmt = Phosphorylation(None, erk)
    g_map = {'ERK1': {'TEXT': 'ERK1', 'HGNC': 'foobar'}}
    gm = GroundingMapper(g_map)
    mapped_stmts = gm.map_stmts([stmt])


@raises(ValueError)
def test_up_and_invalid_hgnc_sym():
    erk = Agent('ERK1', db_refs={'TEXT': 'ERK1'})
    stmt = Phosphorylation(None, erk)
    g_map = {'ERK1': {'TEXT': 'ERK1', 'UP': 'P28482', 'HGNC': 'foobar'}}
    gm = GroundingMapper(g_map)


def test_up_with_no_gene_name_with_hgnc_sym():
    erk = Agent('ERK1', db_refs={'TEXT': 'ERK1'})
    stmt = Phosphorylation(None, erk)
    g_map = {'ERK1': {'TEXT': 'ERK1', 'UP': 'A0K5Q6', 'HGNC': '6871'}}
    gm = GroundingMapper(g_map)
    mapped_stmts = gm.map_stmts([stmt])
    assert mapped_stmts[0].sub.db_refs['HGNC'] == '6871', \
        mapped_stmts[0].sub.db_refs
    assert mapped_stmts[0].sub.db_refs['UP'] == 'P28482', \
        mapped_stmts[0].sub.db_refs


def test_multiple_mapped_up():
    ag = Agent('xx', db_refs={'HGNC': '377', 'UP': 'O43687'})
    gm.standardize_agent_name(ag, True)
    assert ag.db_refs['HGNC'] == '377'
    assert ag.db_refs['UP'] == 'O43687'
    assert ag.name == 'AKAP7'


def test_up_and_mismatched_hgnc():
    erk = Agent('ERK1', db_refs={'TEXT': 'ERK1'})
    stmt = Phosphorylation(None, erk)
    g_map = {'ERK1': {'TEXT': 'ERK1', 'UP': 'P28482', 'HGNC': '6877'}}
    gm = GroundingMapper(g_map)
    mapped_stmts = gm.map_stmts([stmt])
    assert mapped_stmts[0].sub.db_refs['HGNC'] == '6877', \
        mapped_stmts[0].sub.db_refs
    assert mapped_stmts[0].sub.db_refs['UP'] == 'P27361', \
        mapped_stmts[0].sub.db_refs


def test_up_id_with_no_hgnc_id():
    """Non human protein"""
    gag = Agent('Gag', db_refs={'TEXT': 'Gag'})
    stmt = Phosphorylation(None, gag)
    g_map = {'Gag': {'TEXT': 'Gag', 'UP': 'P04585'}}
    gm = GroundingMapper(g_map)
    mapped_stmts = gm.map_stmts([stmt])
    assert len(mapped_stmts) == 1
    mapped_gag = mapped_stmts[0].sub
    assert mapped_gag.name == 'gag-pol'
    assert mapped_gag.db_refs['TEXT'] == 'Gag'
    assert mapped_gag.db_refs.get('HGNC') is None
    assert mapped_gag.db_refs['UP'] == 'P04585'
    assert unicode_strs((gag, stmt, gm, mapped_stmts, mapped_gag))


def test_up_id_with_no_gene_name():
    """Expect no HGNC entry; no error raised."""
    no_gn = Agent('NoGNname', db_refs={'TEXT': 'NoGN'})
    stmt = Phosphorylation(None, no_gn)
    g_map = {'NoGN': {'TEXT': 'NoGN', 'UP': 'A0K5Q6'}}
    gm = GroundingMapper(g_map)
    mapped_stmts = gm.map_stmts([stmt])
    assert len(mapped_stmts) == 1
    mapped_ag = mapped_stmts[0].sub
    assert mapped_ag.name == 'NoGNname'
    assert mapped_ag.db_refs['TEXT'] == 'NoGN'
    assert mapped_ag.db_refs.get('HGNC') is None
    assert mapped_ag.db_refs['UP'] == 'A0K5Q6'
    assert unicode_strs((no_gn, stmt, gm, mapped_stmts, mapped_ag))


def test_in_place_overwrite_of_gm():
    """Make sure HGNC lookups don't modify the original grounding map by adding
    keys."""
    erk = Agent('ERK1', db_refs={'TEXT': 'ERK1'})
    stmt = Phosphorylation(None, erk)
    g_map = {'ERK1': {'TEXT': 'ERK1', 'UP': 'P28482'}}
    gm = GroundingMapper(g_map)
    mapped_stmts = gm.map_stmts([stmt])
    gmap_after_mapping = gm.grounding_map
    assert set(gmap_after_mapping['ERK1'].keys()) == set(['TEXT', 'UP'])


def test_map_entry_hgnc_and_up():
    """Make sure that HGNC symbol is replaced with HGNC ID when grounding map
    includes both UP ID and HGNC symbol."""
    rela = Agent('NF-kappaB p65', db_refs={'TEXT': 'NF-kappaB p65'})
    erk = Agent('ERK1', db_refs={'TEXT': 'ERK1'})
    stmt = Phosphorylation(erk, rela)
    g_map = {'NF-kappaB p65': {'TEXT': 'NF-kappaB p65', 'UP': 'Q04206',
                               'HGNC': '9955'}}
    gm = GroundingMapper(g_map)
    mapped_stmts = gm.map_stmts([stmt])
    assert len(mapped_stmts) == 1
    ms = mapped_stmts[0]
    assert ms.sub.db_refs == {'TEXT': 'NF-kappaB p65', 'UP': 'Q04206',
                              'HGNC': '9955'}


def test_map_agent():
    erk = Agent('ERK1', db_refs={'TEXT': 'ERK1'})
    p_erk = Agent('P-ERK', db_refs={'TEXT': 'p-ERK'})
    stmt = Complex([erk, p_erk])
    mapped_stmts = gm.map_stmts([stmt])
    mapped_ag = mapped_stmts[0].members[1]
    assert mapped_ag.name == 'ERK'
    assert mapped_ag.db_refs.get('FPLX') == 'ERK'


def test_name_standardize_hgnc_up():
    a1 = Agent('x', db_refs={'HGNC': '9387'})
    GroundingMapper.standardize_agent_name(a1, True)
    assert a1.name == 'PRKAG3'
    a1 = Agent('x', db_refs={'UP': 'Q9UGI9'})
    GroundingMapper.standardize_agent_name(a1, True)
    assert a1.name == 'PRKAG3'
    a1 = Agent('x', db_refs={'UP': 'Q8BGM7'})
    GroundingMapper.standardize_agent_name(a1, True)
    assert a1.name == 'Prkag3'


def test_name_standardize_chebi():
    a1 = Agent('x', db_refs={'CHEBI': '15996'})
    GroundingMapper.standardize_agent_name(a1, False)
    assert a1.name == 'GTP'


def test_name_standardize_go():
    a1 = Agent('x', db_refs={'GO': 'GO:0006915'})
    GroundingMapper.standardize_agent_name(a1, False)
    assert a1.name == 'apoptotic process'


def test_name_standardize_mesh():
    a1 = Agent('x', db_refs={'MESH': 'D008545'})
    GroundingMapper.standardize_agent_name(a1, False)
    assert a1.name == 'Melanoma', a1.name


def test_name_standardize_mesh_go():
    a1 = Agent('x', db_refs={'MESH': 'D058750'})
    GroundingMapper.standardize_agent_name(a1, True)
    assert a1.db_refs['GO'] == 'GO:0001837'
    assert a1.name == 'epithelial to mesenchymal transition', a1.name
    a1 = Agent('x', db_refs={'GO': 'GO:0001837'})
    GroundingMapper.standardize_agent_name(a1, True)
    assert a1.db_refs['MESH'] == 'D058750'
    assert a1.name == 'epithelial to mesenchymal transition', a1.name


def test_name_standardize_mesh_other_db():
    a1 = Agent('x', db_refs={'MESH': 'D001194'})
    GroundingMapper.standardize_agent_name(a1, True)
    assert a1.db_refs['CHEBI'] == 'CHEBI:46661'
    assert a1.name == 'asbestos', a1.name

    db_refs = {'MESH': 'D000067777'}
    db_refs = standardize_db_refs(db_refs)
    assert db_refs.get('HGNC') == '3313', db_refs
    assert db_refs.get('UP') == 'Q12926', db_refs
    a2 = Agent('x', db_refs=db_refs)
    standardize_agent_name(a2)
    assert a2.name == 'ELAVL2'


def test_standardize_db_refs_efo_hp_doid():
    refs = standardize_db_refs({'EFO': '0009502'})
    assert refs.get('MESH') == 'D000007', refs
    refs = standardize_db_refs({'MESH': 'D000007'})
    assert refs.get('EFO') == '0009502', refs

    refs = standardize_db_refs({'HP': 'HP:0031801'})
    assert refs.get('MESH') == 'D064706', refs
    refs = standardize_db_refs({'MESH': 'D064706'})
    assert refs.get('HP') == 'HP:0031801', refs

    # Currently there is no one-to-many mapping in the direction towards MeSH
    # (there used to be) if there is again, we should test it here
    #refs = standardize_db_refs({'DOID': 'DOID:0060695'})
    #assert 'MESH' not in refs

    # One-to-many mappings away from MESH
    refs = standardize_db_refs({'MESH': 'D000071017'})
    assert 'DOID' not in refs

    refs = standardize_db_refs({'DOID': 'DOID:0060495'})
    assert refs.get('MESH') == 'D000067208'

    # This is an xrefs-based mapping that isn't in Gilda's resource file
    refs = standardize_db_refs({'EFO': '0000694'})
    assert refs.get('MESH') == 'D045169'


def test_standardize_name_efo_hp_doid():
    ag = Agent('x', db_refs={'HP': 'HP:0031801'})
    standardize_agent_name(ag)
    # Name based on MESH mapping
    assert ag.name == 'Vocal Cord Dysfunction'

    ag = Agent('x', db_refs={'HP': 'HP:0000002'})
    standardize_agent_name(ag)
    # Name based on HP itself
    assert ag.name == 'Abnormality of body height'

    ag = Agent('x', db_refs={'DOID': 'DOID:0014667'})
    standardize_agent_name(ag)
    # Name based on MESH mapping
    assert ag.name == 'Metabolic Diseases'

    ag = Agent('x', db_refs={'EFO': '1002050'})
    standardize_agent_name(ag)
    # Name based on MESH mapping
    assert ag.name == 'Nephritis', (ag.name, ag.db_refs)

    ag = Agent('x', db_refs={'EFO': '0000001'})
    standardize_agent_name(ag)
    # Name based on EFO itself
    assert ag.name == 'experimental factor', (ag.name, ag.db_refs)


def test_standardize_uppro():
    ag = Agent('x', db_refs={'UP': 'P01019'})
    standardize_agent_name(ag)
    assert ag.name == 'AGT'
    ag = Agent('x', db_refs={'UPPRO': 'PRO_0000032458'})
    standardize_agent_name(ag)
    assert ag.name == 'Angiotensin-2', ag.name
    ag = Agent('x', db_refs={'UPPRO': 'PRO_0000032458', 'UP': 'P01019'})
    standardize_agent_name(ag)
    assert ag.name == 'Angiotensin-2', ag.name


@attr('nonpublic')
def test_adeft_mapping():
    er1 = Agent('ER', db_refs={'TEXT': 'ER'})
    pmid1 = '30775882'
    stmt1 = Phosphorylation(None, er1, evidence=[Evidence(pmid=pmid1,
                                                          text_refs={'PMID':
                                                                     pmid1})])

    er2 = Agent('ER', db_refs={'TEXT': 'ER'})
    pmid2 = '28369137'
    stmt2 = Inhibition(None, er2, evidence=[Evidence(pmid=pmid2,
                                                     text_refs={'PMID':
                                                                pmid2})])

    mapped_stmts1 = gm.map_stmts([stmt1])
    assert mapped_stmts1[0].sub.name == 'ESR1'
    assert mapped_stmts1[0].sub.db_refs['HGNC'] == '3467'
    assert mapped_stmts1[0].sub.db_refs['UP'] == 'P03372'

    mapped_stmts2 = gm.map_stmts([stmt2])
    assert mapped_stmts2[0].obj.name == 'endoplasmic reticulum', \
        mapped_stmts2[0].obj.name
    assert mapped_stmts2[0].obj.db_refs['GO'] == 'GO:0005783', \
        mapped_stmts2[0].obj.db_refs

    annotations = mapped_stmts2[0].evidence[0].annotations
    assert 'GO:GO:0005783' in annotations['agents']['adeft'][1]


def test_adeft_mapping_non_pos():
    pcs = Agent('PCS', db_refs={'TEXT': 'PCS'})
    # This is an exact definition of a non-positive label entry so we
    # expect that it will be applied as a grounding
    ev = Evidence(text='post concussive symptoms (PCS)')
    stmt = Phosphorylation(None, pcs, evidence=[ev])
    mapped_stmt = gm.map_stmts([stmt])[0]
    assert 'MESH' in mapped_stmt.sub.db_refs, mapped_stmt.evidence

    pcs = Agent('PCS', db_refs={'TEXT': 'PCS', 'MESH': 'xxx'})
    # There a non-positive entry is implied but not exactly, so
    # the prior grounding will be removed.
    ev = Evidence(text='post symptoms concussive concussion')
    stmt = Phosphorylation(None, pcs, evidence=[ev])
    mapped_stmt = gm.map_stmts([stmt])[0]
    assert 'MESH' not in mapped_stmt.sub.db_refs, mapped_stmt.evidence


def test_misgrounding():
    baz1 = Agent('ZNF214', db_refs={'TEXT': 'baz1', 'HGNC': '13006'})
    stmt = Phosphorylation(None, baz1)
    stmts = gm.map_stmts([stmt])
    stmt = stmts[0]
    assert len(stmt.sub.db_refs) == 1, stmt.sub.db_refs
    assert stmt.sub.db_refs['TEXT'] == 'baz1'
    assert stmt.sub.name == 'baz1'


def test_ground_gilda():
    for mode in ['web', 'local']:
        mek = Agent('Mek', db_refs={'TEXT': 'MEK'})
        erk = Agent('Erk1', db_refs={'TEXT': 'Erk1'})
        stmt = Phosphorylation(mek, erk)
        ground_statements([stmt], mode=mode)
        assert stmt.enz.name == 'MEK', stmt.enz
        assert stmt.enz.db_refs['FPLX'] == 'MEK'
        assert stmt.sub.name == 'MAPK3'
        assert stmt.sub.db_refs['HGNC'] == '6877'
        assert stmt.sub.db_refs['UP'] == 'P27361'


def test_ground_gilda_source():
    ev1 = Evidence(source_api='reach')
    ev2 = Evidence(source_api='sparser')
    ev3 = Evidence(source_api='trips')
    stmts = [Phosphorylation(None, Agent('x', db_refs={'TEXT': 'kras'}),
                             evidence=ev)
             for ev in (ev1, ev2, ev3)]
    ground_statements(stmts, sources=['trips'])
    assert stmts[0].sub.name == 'x', stmts[0]
    assert stmts[1].sub.name == 'x'
    assert stmts[2].sub.name == 'KRAS'
    ground_statements(stmts, sources=['reach', 'sparser'])
    assert all(stmt.sub.name == 'KRAS' for stmt in stmts)


def test_gilda_ground_ungrounded():
    ag1 = Agent('x', db_refs={'TEXT': 'RAS', 'FPLX': 'RAS'})
    ag2 = Agent('x', db_refs={'TEXT': 'RAS'})
    ag3 = Agent('x', db_refs={'TEXT': 'RAS', 'XXXXX': 'XXXX'})
    stmts = [Phosphorylation(None, ag) for ag in (ag1, ag2, ag3)]
    ground_statement(stmts[0], ungrounded_only=True)
    assert ag1.name == 'x'
    ground_statement(stmts[0], ungrounded_only=False)
    assert ag1.name == 'RAS', ag1
    ground_statement(stmts[1], ungrounded_only=True)
    assert ag2.name == 'RAS'
    ground_statements([stmts[2]], ungrounded_only=True)
    assert ag3.name == 'RAS'


def test_get_gilda_models():
    models = get_gilda_models()
    assert 'NDR1' in models


@attr('nonpublic')
def test_gilda_disambiguation():
    gm.gilda_mode = 'web'
    er1 = Agent('NDR1', db_refs={'TEXT': 'NDR1'})
    pmid1 = '18362890'
    stmt1 = Phosphorylation(None, er1,
                            evidence=[Evidence(pmid=pmid1,
                                               text_refs={'PMID': pmid1})])

    er2 = Agent('NDR1', db_refs={'TEXT': 'NDR1'})
    pmid2 = '16832411'
    stmt2 = Inhibition(None, er2,
                       evidence=[Evidence(pmid=pmid2,
                                          text_refs={'PMID': pmid2})])

    mapped_stmts1 = gm.map_stmts([stmt1])
    assert mapped_stmts1[0].sub.name == 'STK38', mapped_stmts1[0].sub.name
    assert mapped_stmts1[0].sub.db_refs['HGNC'] == '17847', \
        mapped_stmts1[0].sub.db_refs
    assert mapped_stmts1[0].sub.db_refs['UP'] == 'Q15208', \
        mapped_stmts1[0].sub.db_refs

    mapped_stmts2 = gm.map_stmts([stmt2])
    assert mapped_stmts2[0].obj.name == 'NDRG1', \
        mapped_stmts2[0].obj.name
    assert mapped_stmts2[0].obj.db_refs['HGNC'] == '7679', \
        mapped_stmts2[0].obj.db_refs
    assert mapped_stmts2[0].obj.db_refs['UP'] == 'Q92597', \
        mapped_stmts2[0].obj.db_refs

    annotations = mapped_stmts2[0].evidence[0].annotations
    assert len(annotations['agents']['gilda'][1]) == 2, \
        annotations
    assert annotations['agents']['gilda'][0] is None
    assert annotations['agents']['gilda'][1] is not None


@attr('nonpublic')
def test_gilda_disambiguation_local():
    gm.gilda_mode = 'local'
    er1 = Agent('NDR1', db_refs={'TEXT': 'NDR1'})
    pmid1 = '18362890'
    stmt1 = Phosphorylation(None, er1,
                            evidence=[Evidence(pmid=pmid1,
                                               text_refs={'PMID': pmid1})])
    mapped_stmts1 = gm.map_stmts([stmt1])
    annotations = mapped_stmts1[0].evidence[0].annotations
    assert annotations['agents']['gilda'][0] is None
    assert annotations['agents']['gilda'][1] is not None
    assert len(annotations['agents']['gilda'][1]) == 2, \
        annotations
    # This is to make sure the to_json of the ScoredMatches works
    assert annotations['agents']['gilda'][1][0]['term']['db'] == 'HGNC'


def test_uppro_fallback():
    # This UP chain has no name currently so we can test that the fallback
    # to naming by the UP ID is working
    ag = Agent('x', db_refs={'UP': 'Q6IE75', 'UPPRO': 'PRO_0000383648'})
    standardize_agent_name(ag)
    assert ag.name == 'Bace2'
