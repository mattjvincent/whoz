from builtins import int
from past.builtins import long

#import logging
import sys


from intermine.webservice import Service
import whoz.utils as utils
service = Service("http://www.mousemine.org/mousemine/service")

LOG = utils.get_logger()


def _fix(val):
    if val is None:
        return ''

    if isinstance(val, (float, long, int)):
        return str(val)

    if isinstance(val, bytes):
        return bytes.decode(val).strip()

    return str(val).strip()


def extract_genes(filename):
    fd = sys.stdout if not filename else open(filename, 'w')

    # Get a new query on the class (table) you will be querying:
    query = service.new_query("SequenceFeature")

    query_columns = []
    query_columns.append("primaryIdentifier")
    query_columns.append("symbol")
    query_columns.append("name")
    query_columns.append("description")
    query_columns.append("sequenceOntologyTerm.name")
    query_columns.append("chromosomeLocation.locatedOn.primaryIdentifier")
    query_columns.append("chromosomeLocation.start")
    query_columns.append("chromosomeLocation.end")
    query_columns.append("chromosomeLocation.strand")
    query_columns.append("organism.shortName")
    query_columns.append("mgiType")

    LOG.debug("Downloading MGI gene data...")

    # The view specifies the output columns
    query.add_view(",".join(query_columns))

    # Uncomment and edit the line below (the default) to select a custom sort order:
    # query.add_sort_order("Gene.primaryIdentifier", "ASC")

    # You can edit the constraint values below
    query.add_constraint("organism.shortName", "=", "M. musculus", code = "A")

    # Uncomment and edit the code below to specify your own custom logic:
    # query.set_logic("A")

    fd.write('\t'.join(query_columns).replace('.', '_'))
    fd.write('\n')

    count = 0

    for row in query.rows():
        count += 1
        if count % 10000 == 0:
            LOG.debug("{} lines parsed".format(count))

        elem = []
        for column in query_columns:
            elem.append('"{}"'.format(_fix(row[column])))
        fd.write('\t'.join(elem))
        fd.write('\n')


def extract_ensembl_ids(filename):
    fd = sys.stdout if not filename else open(filename, 'w')

    # Get a new query on the class (table) you will be querying:
    query = service.new_query("SequenceFeature")

    # The view specifies the output columns
    query_columns = []
    query_columns.append("primaryIdentifier")
    query_columns.append("symbol")
    query_columns.append("crossReferences.identifier")
    query_columns.append("crossReferences.source.name")

    LOG.debug("Downloading MGI Ensembl ids...")

    query.add_view(",".join(query_columns))

    query.add_constraint("organism.shortName", "=", "M. musculus", code = "A")
    query.add_constraint("crossReferences.source.name", "=", "Ensembl Gene Model", code = "B")

    fd.write('\t'.join(query_columns).replace('.', '_'))
    fd.write('\n')

    count = 0
    for row in query.rows():
        count += 1
        if count % 10000 == 0:
            LOG.debug("{} lines parsed".format(count))

        elem = []
        for column in query_columns:
            elem.append('"' + str(_fix(row[column])) + '"')
        fd.write('\t'.join(elem))
        fd.write('\n')


def extract_entrez_ids(filename):
    fd = sys.stdout if not filename else open(filename, 'w')

    # Get a new query on the class (table) you will be querying:
    query = service.new_query("SequenceFeature")

    # The view specifies the output columns
    query_columns = []
    query_columns.append("primaryIdentifier")
    query_columns.append("symbol")
    query_columns.append("crossReferences.identifier")
    query_columns.append("crossReferences.source.name")

    LOG.debug("Downloading MGI Entrez ids...")

    query.add_view(",".join(query_columns))

    query.add_constraint("organism.shortName", "=", "M. musculus", code = "A")
    query.add_constraint("crossReferences.source.name", "=", "Entrez Gene", code = "B")

    fd.write('\t'.join(query_columns).replace('.', '_'))
    fd.write('\n')

    count = 0

    for row in query.rows():
        count += 1
        if count % 10000 == 0:
            LOG.debug("{} lines parsed".format(count))

        elem = []
        for column in query_columns:
            elem.append('"' + str(_fix(row[column])) + '"')
        fd.write('\t'.join(elem))
        fd.write('\n')


def extract_synonyms(filename):
    fd = sys.stdout if not filename else open(filename, 'w')

    # Get a new query on the class (table) you will be querying:
    query = service.new_query("SequenceFeature")

    # The view specifies the output columns
    query_columns = []
    query_columns.append("primaryIdentifier")
    query_columns.append("symbol")
    query_columns.append("synonyms.value")

    LOG.debug("Downloading MGI synonyms...")

    query.add_view(",".join(query_columns))

    # Uncomment and edit the line below (the default) to select a custom sort order:
    # query.add_sort_order("SequenceFeature.primaryIdentifier", "ASC")

    # You can edit the constraint values below
    #query.add_constraint("primaryIdentifier", "==", "MGI:1916232", code = "A")
    query.add_constraint("organism.shortName", "=", "M. musculus", code = "A")

    # Uncomment and edit the code below to specify your own custom logic:
    # query.set_logic("A")
    fd.write('\t'.join(query_columns).replace('.', '_'))
    fd.write('\n')

    count = 0

    for row in query.rows():
        count += 1
        if count % 10000 == 0:
            LOG.debug("{} lines parsed".format(count))

        elem = []
        for column in query_columns:
            elem.append('"' + str(_fix(row[column])) + '"')
        fd.write('\t'.join(elem))
        fd.write('\n')

def extract_synonyms_one_line(filename):
    fd = sys.stdout if not filename else open(filename, 'w')

    # Get a new query on the class (table) you will be querying:
    query = service.new_query("SequenceFeature")

    # The view specifies the output columns
    query_columns = []
    query_columns.append("primaryIdentifier")
    query_columns.append("symbol")
    query_columns.append("synonyms.value")

    LOG.debug("Downloading MGI synonyms (oneline)...")

    query.add_view(",".join(query_columns))

    # Uncomment and edit the line below (the default) to select a custom sort order:
    # query.add_sort_order("SequenceFeature.primaryIdentifier", "ASC")

    # You can edit the constraint values below
    query.add_constraint("organism.shortName", "=", "M. musculus", code = "A")
    #query.add_constraint("primaryIdentifier", "=", "MGI:3761162", code = "B")

    # Uncomment and edit the code below to specify your own custom logic:
    # query.set_logic("A")
    fd.write('primaryIdentifier\tsynonyms\n')

    ids = {}

    count = 0

    for row in query.rows():
        count += 1
        if count % 10000 == 0:
            LOG.debug("{} lines parsed".format(count))

        id = _fix(row['primaryIdentifier'])
        symbol = _fix(row['symbol']).strip()
        synonym = _fix(row['synonyms.value']).strip()

        if symbol != synonym:
            if id in ids:
                synonyms = ids[id]
                if synonym not in synonyms:
                    synonyms.append(synonym)
                    ids[id] = synonyms
            else:
                synonyms = []
                synonyms.append(synonym)
                ids[id] = synonyms

    for key in ids:
        line = str(key) + '\t' + '||'.join(ids[key])
        fd.write(line)
        fd.write('\n')


