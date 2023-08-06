__all__ = ['standardize_agent_name', 'standardize_db_refs',
           'name_from_grounding']

import logging
from indra.databases import uniprot_client, hgnc_client, mesh_client, \
    chebi_client, go_client, efo_client, hp_client, doid_client

logger = logging.getLogger(__name__)


def standardize_db_refs(db_refs):
    """Return a standardized db refs dict for a given db refs dict.

    Parameters
    ----------
    db_refs : dict
        A dict of db refs that may not be standardized, i.e., may be
        missing an available UP ID corresponding to an existing HGNC ID.

    Returns
    -------
    dict
        The db_refs dict with standardized entries.
    """
    # First we normalize out EFO, HP and DOID and map them to MESH
    for db_ns in ('EFO', 'HP', 'DOID'):
        if db_ns in db_refs:
            mesh_id = mesh_client.get_mesh_id_from_db_id(db_ns, db_refs[db_ns])
            if mesh_id:
                db_refs['MESH'] = mesh_id
                break

    # Next we normalize out MESH to other name spaces
    mesh_id = db_refs.get('MESH')
    # TODO: in principle we could also do a reverse mapping to MESH IDs from
    # other name spaces
    if mesh_id:
        db_mapping = mesh_client.get_db_mapping(mesh_id)
        if db_mapping:
            db_ns, db_id = db_mapping
            if db_ns not in db_refs:
                db_refs[db_ns] = db_id

    # Next we look at gene/protein name spaces
    up_id = db_refs.get('UP')
    up_pro = db_refs.get('UPPRO')
    hgnc_id = db_refs.get('HGNC')

    # If we have a feature without its protein, we get it
    if up_pro and not up_id:
        up_id_mapped = uniprot_client.get_feature_of(up_pro)
        if up_id_mapped:
            db_refs['UP'] = up_id_mapped
            up_id = up_id_mapped

    # If we have a UP ID and no HGNC ID, we try to get a gene name,
    # and if possible, a HGNC ID from that
    if up_id and not hgnc_id:
        hgnc_id = uniprot_client.get_hgnc_id(up_id)
        if hgnc_id:
            db_refs['HGNC'] = hgnc_id
    # Otherwise, if we don't have a UP ID but have an HGNC ID, we try to
    # get the UP ID
    elif hgnc_id:
        # Now get the Uniprot ID for the gene
        mapped_up_id = hgnc_client.get_uniprot_id(hgnc_id)
        if mapped_up_id:
            # If we find an inconsistency, we explain it in an error
            # message and fall back on the mapped ID
            if up_id and up_id != mapped_up_id:
                # We handle a special case here in which mapped_up_id is
                # actually a list of UP IDs that we skip and just keep
                # the original up_id
                if ', ' not in mapped_up_id:
                    # If we got a proper single protein mapping, we use
                    # the mapped_up_id to standardize to.
                    msg = ('Inconsistent groundings UP:%s not equal to '
                           'UP:%s mapped from HGNC:%s, standardizing to '
                           'UP:%s' % (up_id, mapped_up_id, hgnc_id,
                                      mapped_up_id))
                    logger.debug(msg)
                    db_refs['UP'] = mapped_up_id
            # If there is no conflict, we can update the UP entry
            else:
                db_refs['UP'] = mapped_up_id

    # Now we normalize between chemical name spaces
    pc_id = db_refs.get('PUBCHEM')
    chebi_id = db_refs.get('CHEBI')
    hmdb_id = db_refs.get('HMDB')
    mapped_chebi_id = None
    mapped_pc_id = None
    hmdb_mapped_chebi_id = None
    # If we have original PUBCHEM and CHEBI IDs, we always keep those:
    if pc_id:
        mapped_chebi_id = chebi_client.get_chebi_id_from_pubchem(pc_id)
        if mapped_chebi_id and not mapped_chebi_id.startswith('CHEBI:'):
            mapped_chebi_id = 'CHEBI:%s' % mapped_chebi_id
    if chebi_id:
        mapped_pc_id = chebi_client.get_pubchem_id(chebi_id)
    if hmdb_id:
        hmdb_mapped_chebi_id = chebi_client.get_chebi_id_from_hmdb(hmdb_id)
        if hmdb_mapped_chebi_id and \
                not hmdb_mapped_chebi_id.startswith('CHEBI:'):
            hmdb_mapped_chebi_id = 'CHEBI:%s' % hmdb_mapped_chebi_id
    # We always keep originals if both are present but display warnings
    # if there are inconsistencies
    if pc_id and chebi_id and mapped_pc_id and pc_id != mapped_pc_id:
        msg = ('Inconsistent groundings PUBCHEM:%s not equal to '
               'PUBCHEM:%s mapped from %s, standardizing to '
               'PUBCHEM:%s.' % (pc_id, mapped_pc_id, chebi_id, pc_id))
        logger.debug(msg)
    elif pc_id and chebi_id and mapped_chebi_id and chebi_id != \
            mapped_chebi_id:
        msg = ('Inconsistent groundings %s not equal to '
               '%s mapped from PUBCHEM:%s, standardizing to '
               '%s.' % (chebi_id, mapped_chebi_id, pc_id, chebi_id))
        logger.debug(msg)
    # If we have PC and not CHEBI but can map to CHEBI, we do that
    elif pc_id and not chebi_id and mapped_chebi_id:
        db_refs['CHEBI'] = mapped_chebi_id
    elif hmdb_id and chebi_id and hmdb_mapped_chebi_id and \
            hmdb_mapped_chebi_id != chebi_id:
        msg = ('Inconsistent groundings %s not equal to '
               '%s mapped from %s, standardizing to '
               '%s.' % (chebi_id, hmdb_mapped_chebi_id, hmdb_id, chebi_id))
        logger.debug(msg)
    elif hmdb_id and not chebi_id and hmdb_mapped_chebi_id:
        db_refs['CHEBI'] = hmdb_mapped_chebi_id
    # If we have CHEBI and not PC but can map to PC, we do that
    elif chebi_id and not pc_id and mapped_pc_id:
        db_refs['PUBCHEM'] = mapped_pc_id

    # Finally, we standardize between MESH and GO
    go_id = db_refs.get('GO')
    if mesh_id and not go_id:
        mapped_go_id = mesh_client.get_go_id(mesh_id)
        if mapped_go_id:
            db_refs['GO'] = mapped_go_id
    elif go_id and not mesh_id:
        mapped_mesh_id = mesh_client.get_mesh_id_from_go_id(go_id)
        if mapped_mesh_id:
            db_refs['MESH'] = mapped_mesh_id

    # Otherwise there is no useful mapping that we can add and no
    # further conflict to resolve.
    return db_refs


def standardize_agent_name(agent, standardize_refs=True):
    """Standardize the name of an Agent based on grounding information.

    If an agent contains a FamPlex grounding, the FamPlex ID is used as a
    name. Otherwise if it contains a Uniprot ID, an attempt is made to find
    the associated HGNC gene name. If one can be found it is used as the
    agent name and the associated HGNC ID is added as an entry to the
    db_refs. Similarly, CHEBI, MESH and GO IDs are used in this order of
    priority to assign a standardized name to the Agent. If no relevant
    IDs are found, the name is not changed.

    Parameters
    ----------
    agent : indra.statements.Agent
        An INDRA Agent whose name attribute should be standardized based
        on grounding information.
    standardize_refs : Optional[bool]
        If True, this function assumes that the Agent's db_refs need to
        be standardized, e.g., HGNC mapped to UP.
        Default: True

    Returns
    -------
    bool
        True if a new name was set, False otherwise.
    """
    # We return immediately for None Agents
    if agent is None:
        return False

    if standardize_refs:
        agent.db_refs = standardize_db_refs(agent.db_refs)

    # We next look for prioritized grounding, if missing, we return
    db_ns, db_id = agent.get_grounding()

    # If there's no grounding then we can't do more to standardize the
    # name and return
    if not db_ns or not db_id:
        return False

    # If there is grounding available, we can try to get the standardized name
    # and in the rare case that we don't get it, we don't set it.
    standard_name = name_from_grounding(db_ns, db_id)
    # Handle special case with UPPRO, if we can't get a feature name
    # we fall back on regular gene/protein naming
    if not standard_name and db_ns == 'UPPRO':
        db_ns, db_id = agent.get_grounding(ns_order=['HGNC', 'UP'])
        if not db_ns or not db_id:
            return False
        standard_name = name_from_grounding(db_ns, db_id)
    if not standard_name:
        return False

    agent.name = standard_name
    return True


def name_from_grounding(db_ns, db_id):
    """Return a standardized name given a name space and an ID.

    Parameters
    ----------
    db_ns : str
        The name space in which the ID is defined.
    db_id : str
        The ID within the name space.

    Returns
    -------
    str or None
        The standardized name corresponding to the grounding or None if
        not available.
    """
    if db_ns == 'FPLX':
        return db_id
    elif db_ns == 'HGNC':
        return hgnc_client.get_hgnc_name(db_id)
    elif db_ns == 'UP':
        return uniprot_client.get_gene_name(db_id, web_fallback=False)
    elif db_ns == 'CHEBI':
        return chebi_client.get_chebi_name_from_id(db_id)
    elif db_ns == 'MESH':
        return mesh_client.get_mesh_name(db_id, False)
    elif db_ns == 'GO':
        return go_client.get_go_label(db_id)
    elif db_ns == 'HP':
        return hp_client.get_hp_name_from_hp_id(db_id)
    elif db_ns == 'EFO':
        return efo_client.get_efo_name_from_efo_id(db_id)
    elif db_ns == 'DOID':
        return doid_client.get_doid_name_from_doid_id(db_id)
    elif db_ns == 'UPPRO':
        feat = uniprot_client.get_feature_by_id(db_id)
        if feat and feat.name:
            return feat.name
    return None
