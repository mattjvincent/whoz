# -*- coding: utf_8 -*-

from __future__ import print_function
from future.utils import iteritems
from builtins import str

import sqlite3
import re
import sys

import whoz.utils as utils

LOG = utils.get_logger()

DATABASE = ''

if sys.version_info > (3,):
    long = int

def connect_to_database():
    return sqlite3.connect(DATABASE)

REGEX_ENSEMBL_MOUSE_ID = re.compile("ENSMUS([EGTP])[0-9]{11}", re.IGNORECASE)
REGEX_ENSEMBL_HUMAN_ID = re.compile("ENS([EGTP])[0-9]{11}", re.IGNORECASE)
REGEX_MGI_ID = re.compile("MGI:[0-9]{1,}", re.IGNORECASE)
REGEX_REGION = re.compile("(CHR|)*\s*([0-9]{1,2}|X|Y|MT)\s*(-|:)?\s*(\d+)\s*(MB|M|K|)?\s*(-|:|)?\s*(\d+|)\s*(MB|M|K|)?", re.IGNORECASE)

SQL_TERM_EXACT = '''
SELECT MAX(s.score||'||'||s.description||'||'||l.lookup_value) AS match_description, l.ensembl_gene_id, g.*
  FROM ensembl_genes g,
       ensembl_genes_lookup l,
       search_ranking s
WHERE g.ensembl_gene_id = l.ensembl_gene_id
  AND l.ranking_id = s.ranking_id
  AND l.lookup_value = :term
GROUP BY l.ensembl_gene_id
ORDER BY match_description - length(match_description) DESC, g.symbol ASC
'''

SQL_TERM_EXACT_MM = '''
SELECT MAX(s.score||'||'||s.description||'||'||l.lookup_value) AS match_description, l.ensembl_gene_id, g.*
  FROM ensembl_genes g,
       ensembl_genes_lookup l,
       search_ranking s
WHERE g.ensembl_gene_id = l.ensembl_gene_id
  AND l.ranking_id = s.ranking_id
  AND l.lookup_value = :term
  AND l.species_id = 'Mm'
GROUP BY l.ensembl_gene_id
ORDER BY match_description - length(match_description) DESC, g.symbol ASC
'''

SQL_TERM_EXACT_HS = '''
SELECT MAX(s.score||'||'||s.description||'||'||l.lookup_value) AS match_description, l.ensembl_gene_id, g.*
  FROM ensembl_genes g,
       ensembl_genes_lookup l,
       search_ranking s
WHERE g.ensembl_gene_id = l.ensembl_gene_id
  AND l.ranking_id = s.ranking_id
  AND l.lookup_value = :term
  AND l.species_id = 'Hs'
GROUP BY l.ensembl_gene_id
ORDER BY match_description - length(match_description) DESC, g.symbol ASC
'''

SQL_TERM_LIKE = '''
SELECT MAX(s.score||'||'||s.description||'||'||l.lookup_value) AS match_description, l.ensembl_gene_id, g.*
  FROM ensembl_genes g,
       ensembl_genes_lookup l,
       ensembl_search es,
       search_ranking s
WHERE g.ensembl_gene_id = l.ensembl_gene_id
  AND l.ranking_id = s.ranking_id
  AND es._ensembl_genes_lookup_key = l._ensembl_genes_lookup_key
  AND es.lookup_value MATCH :term
GROUP BY l.ensembl_gene_id
ORDER BY match_description - length(match_description) DESC, g.symbol ASC
'''

SQL_TERM_LIKE_MM = '''
SELECT MAX(s.score||'||'||s.description||'||'||l.lookup_value) AS match_description, l.ensembl_gene_id, g.*
  FROM ensembl_genes g,
       ensembl_genes_lookup l,
       ensembl_search es,
       search_ranking s
WHERE g.ensembl_gene_id = l.ensembl_gene_id
  AND l.ranking_id = s.ranking_id
  AND es._ensembl_genes_lookup_key = l._ensembl_genes_lookup_key
  AND es.lookup_value MATCH :term
  AND l.species_id = 'Mm'
GROUP BY l.ensembl_gene_id
ORDER BY match_description - length(match_description) DESC, g.symbol ASC
'''

SQL_TERM_LIKE_HS = '''
SELECT MAX(s.score||'||'||s.description||'||'||l.lookup_value) AS match_description, l.ensembl_gene_id, g.*
  FROM ensembl_genes g,
       ensembl_genes_lookup l,
       ensembl_search es,
       search_ranking s
WHERE g.ensembl_gene_id = l.ensembl_gene_id
  AND l.ranking_id = s.ranking_id
  AND es._ensembl_genes_lookup_key = l._ensembl_genes_lookup_key
  AND es.lookup_value MATCH :term
  AND l.species_id = 'Hs'
GROUP BY l.ensembl_gene_id
ORDER BY match_description - length(match_description) DESC, g.symbol ASC
'''

SQL_ID = '''
SELECT MAX(s.score||'||'||s.description||'||'||l.lookup_value) AS match_description, l.ensembl_gene_id, g.*
  FROM ensembl_genes g,
       ensembl_genes_lookup l,
       ensembl_search es,
       search_ranking s
WHERE g.ensembl_gene_id = l.ensembl_gene_id
  AND l.ranking_id = s.ranking_id
  AND es._ensembl_genes_lookup_key = l._ensembl_genes_lookup_key
  AND l.ranking_id in ('MI', 'EG', 'ET', 'EE', 'EP', 'HI')
  AND es.lookup_value MATCH :term
GROUP BY l.ensembl_gene_id
ORDER BY match_description - length(match_description) DESC, g.symbol ASC
'''

SQL_ID_MM = '''
SELECT MAX(s.score||'||'||s.description||'||'||l.lookup_value) AS match_description, l.ensembl_gene_id, g.*
  FROM ensembl_genes g,
       ensembl_genes_lookup l,
       ensembl_search es,
       search_ranking s
WHERE g.ensembl_gene_id = l.ensembl_gene_id
  AND l.ranking_id = s.ranking_id
  AND es._ensembl_genes_lookup_key = l._ensembl_genes_lookup_key
  AND l.species_id = 'Mm'
  AND l.ranking_id in ('MI', 'EG', 'ET', 'EE', 'EP', 'HI')
  AND es.lookup_value MATCH :term
GROUP BY l.ensembl_gene_id
ORDER BY match_description - length(match_description) DESC, g.symbol ASC
'''

SQL_ID_HS = '''
SELECT MAX(s.score||'||'||s.description||'||'||l.lookup_value) AS match_description, l.ensembl_gene_id, g.*
  FROM ensembl_genes g,
       ensembl_genes_lookup l,
       ensembl_search es,
       search_ranking s
WHERE g.ensembl_gene_id = l.ensembl_gene_id
  AND l.ranking_id = s.ranking_id
  AND es._ensembl_genes_lookup_key = l._ensembl_genes_lookup_key
  AND l.species_id = 'Hs'
  AND l.ranking_id in ('MI', 'EG', 'ET', 'EE', 'EP', 'HI')
  AND es.lookup_value MATCH :term
GROUP BY l.ensembl_gene_id
ORDER BY match_description - length(match_description) DESC, g.symbol ASC
'''

SQL_REGION = '''
SELECT *
  FROM ensembl_genes e
 WHERE e.chromosome = :chromosome
   AND e.start_position >= :start_position
   AND e.end_position <= :end_position
 ORDER BY cast(replace(replace(replace(e.chromosome, 'X', '50'), 'Y', '51'), 'MT', 51) AS int), e.start_position, e.end_position
'''

SQL_REGION_MM = '''
SELECT *
  FROM ensembl_genes e
 WHERE e.chromosome = :chromosome
   AND e.start_position >= :start_position
   AND e.end_position <= :end_position
   AND e.species_id = 'Mm'
 ORDER BY cast(replace(replace(replace(e.chromosome, 'X', '50'), 'Y', '51'), 'MT', 51) AS int), e.start_position, e.end_position
'''

SQL_REGION_HS = '''
SELECT *
  FROM ensembl_genes e
 WHERE e.chromosome = :chromosome
   AND e.start_position >= :start_position
   AND e.end_position <= :end_position
   AND e.species_id = 'Hs'
 ORDER BY cast(replace(replace(replace(e.chromosome, 'X', '50'), 'Y', '51'), 'MT', 51) AS int), e.start_position, e.end_position
'''

SQL_ID_FULL = '''
SELECT *
  FROM ensembl_genes e,
       ensembl_gtep g
WHERE e.ensembl_gene_id = g.gene_id
  AND e.ensembl_gene_id IN (
        SELECT distinct gtep.gene_id
          FROM ensembl_gtep gtep
         WHERE gtep.gene_id = :term
            OR gtep.transcript_id = :term
            OR gtep.exon_id = :term
            OR gtep.protein_id = :term)
 ORDER BY e._ensembl_genes_key
'''


QUERIES = {}
QUERIES['SQL_TERM_EXACT'] = SQL_TERM_EXACT
QUERIES['SQL_TERM_EXACT_MM'] = SQL_TERM_EXACT_MM
QUERIES['SQL_TERM_EXACT_HS'] = SQL_TERM_EXACT_HS
QUERIES['SQL_TERM_LIKE'] = SQL_TERM_LIKE
QUERIES['SQL_TERM_LIKE_MM'] = SQL_TERM_LIKE_MM
QUERIES['SQL_TERM_LIKE_HS'] = SQL_TERM_LIKE_HS
QUERIES['SQL_ID'] = SQL_ID
QUERIES['SQL_ID_MM'] = SQL_ID_MM
QUERIES['SQL_ID_HS'] = SQL_ID_HS
QUERIES['SQL_REGION'] = SQL_REGION
QUERIES['SQL_REGION_MM'] = SQL_REGION_MM
QUERIES['SQL_REGION_HS'] = SQL_REGION_HS


class Status:
    pass


class Region:
    """
    Encapsulates a genomic region
    """
    def __init__(self):
        self.chromosome = ''
        self.start_position = None
        self.end_position = None

    def __str__(self):
        return str(self.chromosome) + ':' + str(self.start_position) + '-' + str(self.end_position)

    def __repr__(self):
        return {'chromosome': self.chromosome,
                'start_position': self.start_position,
                'end_position': self.end_position}


class Query:
    """
    Simple class to encapsulate query objects

    """
    def __init__(self, term=None, species_id=None, exact=False, verbose=False):
        self.term = term
        self.species_id = species_id
        self.exact = exact
        self.verbose = verbose
        self._region = None
        self.query = None

    def __str__(self):
        return 'QUERY: \n' + str(self.query) + '\nTERM: ' + str(self.term) + '\nSPECIES_ID: ' + str(self.species_id) + \
               '\nEXACT: ' + str(self.exact) + '\nVERBOSE: ' + str(self.verbose) + '\nREGION: ' + str(self._region) + \
               '\nPARAMS: ' + str(self.get_params())

    def get_params(self):
        if self._region:
            return {'chromosome': self._region.chromosome,
                    'start_position': self._region.start_position,
                    'end_position': self._region.end_position}
        return {'term': self.term}


class Match:
    """ Simple class to encapsulate a match

    """
    def __init__(self, ensembl_gene_id=None, external_id=None, symbol=None, name=None, description=None,
                 synonyms=None, species_id=None, chromosome=None, position_start=None, position_end=None, strand=None,
                 match_reason=None, match_value=None):
        self.ensembl_gene_id = ensembl_gene_id
        self.external_id = external_id
        self.species_id = species_id
        self.symbol = symbol
        self.name = name
        self.description = description
        self.synonyms = synonyms
        self.chromosome = chromosome
        self.position_start = position_start
        self.position_end = position_end
        self.strand = strand
        self.match_reason = match_reason
        self.match_value = match_value

    def __str__(self):
        return str(self.ensembl_gene_id)

    def dict(self):
        return self.__dict__



class Result:
    """ Simple class to encapsulate a Query and matches

    """
    def __init__(self, query=None, matches=[]):
        self.query = query
        self.matches = matches


def str2bool(v):
    """ Checks to see if v is a string representing True

    Parameters:
        v: a string representing a boolean value
    Returns:
        True or False
    """
    if v:
        return v.lower() in ("yes", "true", "t", "1")
    return False


def nvl(value, default):
    """ Evaluates if value es empty or None, if so returns default

    Parameters:
        value: the evalue to evaluate
        default: the default value
    Returns:
        value or default
    """
    if value:
        return value
    return default


def nvli(value, default):
    ret = default
    if value:
        try:
            ret = int(value)
        except ValueError:
            pass
    return ret


def get_status(error = False, message=None):
    """ Create a status with no error and no message

    Parameters:
        error: True if there is an error, False otherwise
        message: The error message
    Returns:
        status: Status object
    """
    _status = Status()
    _status.error = error
    _status.message = nvl(message, '')
    return _status


def get_multiplier(factor):
    if factor.lower() == 'mb':
        return 10000000
    elif factor.lower() == 'm':
        return 1000000
    elif factor.lower() == 'k':
        return 1000

    return 1


def str_to_region(location):
    status = get_status()
    if not location:
        return None, get_status(True, 'No location')

    valid_location = location.strip()

    if len(valid_location) <= 0:
        return None, get_status(True, 'Empty location')

    match = REGEX_REGION.match(valid_location)

    loc = None

    if match:
        loc = Region()
        loc.chromosome = match.group(2)
        loc.start_position = match.group(4)
        loc.end_position = match.group(7)
        multiplier_one = match.group(5)
        multiplier_two = match.group(8)

        if type(loc.start_position) is str:
            loc.start_position = long(loc.start_position)
        if type(loc.end_position) is str:
            loc.end_position = long(loc.end_position)

        if multiplier_one:
            loc.start_position *= get_multiplier(multiplier_one)

        if multiplier_two:
            loc.end_position *= get_multiplier(multiplier_two)
    else:
        status = get_status(True, 'Invalid location string')

    return loc, status


def convert(input_value):
    if isinstance(input_value, dict):
        return {convert(key): convert(value) for key, value in input_value.iteritems()}
    elif isinstance(input_value, list):
        return [convert(element) for element in input_value]
    elif isinstance(input_value, unicode):
        return input_value.encode('utf-8')
    else:
        return input_value


def validate_ensembl_id(ensembl_id):
    """ Validate an id to make sure it conforms to the convention.

    Parameters:
        ensembl_id: the ensembl identifer (string)
    Returns:
        valid_id: the valid ensembl id or None if not valid
        status: True if error, false otherwise and message

    """
    status = get_status()
    if not ensembl_id:
        return None, get_status(True, 'No Ensembl id')

    valid_id = ensembl_id.strip()

    if len(valid_id) <= 0:
        return None, get_status(True, 'Empty Ensembl id')

    if REGEX_ENSEMBL_HUMAN_ID.match(ensembl_id):
        return valid_id, status
    elif REGEX_ENSEMBL_MOUSE_ID.match(id):
        return valid_id, status

    return None, get_status(True, 'Invalid Ensembl ID')


def _get_query(term, species_id=None, exact=True, verbose=False):
    """ Get query based upon parameters

    Parameters:
        term: the query object
        species_id: either 'Hs', 'Mm', or None
        exact: True for exact matches
        verbose: True to give details
    Returns:
        query: the query
        status: True if error, false otherwise and message

    """
    status = get_status()
    if not term:
        return None, get_status(True, 'No term')

    valid_term = term.strip()

    if len(valid_term) <= 0:
        return None, get_status(True, 'Empty term')

    query = Query(term, species_id, exact, verbose)

    if species_id:
        species_id = '_' + species_id.upper()
    else:
        species_id = ''

    if REGEX_ENSEMBL_MOUSE_ID.match(valid_term):
        query.query = QUERIES['SQL_ID' + species_id]
    elif REGEX_ENSEMBL_HUMAN_ID.match(valid_term):
        query.query = QUERIES['SQL_ID' + species_id]
    elif REGEX_MGI_ID.match(valid_term):
        query.query = QUERIES['SQL_ID' + species_id]
    elif REGEX_REGION.match(valid_term):
        region, status = str_to_region(term)
        if not status.error:
            query.query = QUERIES['SQL_REGION' + species_id]
            query._region = region
        else:
            return None, status
    else:
        if exact:
            query.query = QUERIES['SQL_TERM_EXACT' + species_id]
        else:
            query.query = QUERIES['SQL_TERM_LIKE' + species_id]

            if valid_term[-1] != '*':
                valid_term = valid_term + '*'

            query.term = valid_term

    return query, status


def _query(query, limit=1000000):
    status = get_status()

    if not query:
        return None, get_status(True, 'No query')

    matches = []

    limit = nvli(limit, 1000000)

    try:
        conn = connect_to_database()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        for row in cursor.execute(query.query, query.get_params()):
            match = Match()
            match.ensembl_gene_id = row['ensembl_gene_id']
            match.external_id = row['external_id']
            match.species_id = row['species_id']
            match.symbol = row['symbol']
            match.name = row['name']
            match.description = row['description']

            row_synonyms = row['synonyms']
            synonyms = []
            if row_synonyms:
                synonyms = row_synonyms.split('||')

            match.synonyms = synonyms
            match.chromosome = row['chromosome']
            match.position_start = row['start_position']
            match.position_end = row['end_position']
            match.strand = '+' if row['strand'] > 0 else '-'

            if query._region:
                match.match_reason = 'Region'
                match.match_value = str(match.chromosome) + ':' + str(match.position_start) + '-' + str(match.position_end)
            else:
                row_match_description = row['match_description']
                if row_match_description:
                    desc = row_match_description.split('||')
                match.match_reason = desc[1]
                match.match_value = desc[2]

            matches.append(match)

            if len(matches) >= limit:
                break

        cursor.close()
    except sqlite3.Error as e:
        return None, get_status(True, 'Database Error: ' + str(e))

    return Result(query, matches), status


def search(term, species_id=None, exact=True, verbose=False, limit=None):
    if verbose:
        LOG.debug('term={}'.format(str(term)))
        LOG.debug('species_id={}'.format(str(species_id)))
        LOG.debug('exact={}'.format(str(exact)))
        LOG.debug('verbose={}'.format(str(verbose)))
        LOG.debug('limit={}'.format(str(limit)))

    query, status = _get_query(term, species_id, exact, verbose)

    if verbose:
        LOG.debug(str(query))

    if status.error:
        return None, status

    result, status = _query(query, limit)

    if verbose:
        LOG.debug('# matches', len(result.matches))

    if status.error:
        return None, status

    return result, status


def get_id(id, verbose=False):
    if verbose:
        LOG.debug('id={}'.format(str(id)))

    status = get_status()
    query = SQL_ID_FULL
    results = {}

    if verbose:
        LOG.debug(str(query))

    try:
        conn = connect_to_database()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        for row in cursor.execute(query, {'term': id}):
            gene_id = str(row['ensembl_gene_id'])
            transcript_id = str(row['transcript_id'])
            exon_id = str(row['exon_id'])
            protein_id = row['protein_id']
            #print('-------------------')
            #print(row)
            #print(results)

            if gene_id in results:
                gene = results[gene_id]
                #print('found gene: {}'.format(gene))
            else:
                gene = {
                    'id': gene_id,
                    'transcripts': {}
                }

                if row['symbol']:
                    gene['symbol'] = row['symbol']
                if row['name']:
                    gene['name'] = row['name']
                if row['description']:
                    gene['description'] = row['description']
                if row['external_id']:
                    gene['external_id'] = row['external_id']
                if row['species_id']:
                    gene['species_id'] = row['species_id']
                if row['chromosome']:
                    gene['chromosome'] = row['chromosome']
                if row['start_position']:
                    gene['start'] = row['start_position']
                if row['end_position']:
                    gene['end'] = row['end_position']
                if row['strand']:
                    gene['strand'] = '+' if row['strand'] > 0 else '-'
                if row['synonyms']:
                    row_synonyms = row['synonyms']
                    gene['synonyms'] = row_synonyms.split('||')

                #print('created gene: {}'.format(gene))

            if transcript_id in gene['transcripts']:
                transcript = gene['transcripts'][transcript_id]
                #print('found transcript: {}'.format(transcript))
            else:
                transcript = {
                    'id': transcript_id,
                    'start_position': row['transcript_start'],
                    'end_position': row['transcript_end'],
                    'exons': {}
                }
                #print('created transcript: {}'.format(transcript))

            if exon_id in transcript['exons']:
                exon = transcript['exons'][exon_id]
                #print('found exon: {}'.format(exon))
            else:
                exon = {
                    'id': exon_id,
                    'start_position': row['exon_start'],
                    'end_position': row['exon_end'],
                    'rank': row['exon_rank']
                }
                #print('created exon: {}'.format(exon))

            if protein_id:
                exon['protein_id'] = protein_id

            transcript['exons'][exon_id] = exon
            gene['transcripts'][transcript_id] = transcript

            #print('exon=', exon)
            #print('transcript=', transcript)
            #print('gene=', gene)
            results[gene_id] = gene

        cursor.close()

        # convert to sorted list rather than dict
        ret = []
        for (gene_id, gene) in iteritems(results):
            t = []
            for (transcript_id, transcript) in iteritems(gene['transcripts']):
                e = []
                for (exon_id, exon) in iteritems(transcript['exons']):
                    e.append(exon)
                transcript['exons'] = sorted(e, key=lambda ex: ex['rank'])
                t.append(transcript)
            gene['transcripts'] = sorted(t, key=lambda tr: tr['start_position'])
            ret.append(gene)

        results = ret

    except sqlite3.Error as e:
        return None, get_status(True, 'Database Error: ' + str(e))

    if status.error:
        return None, status

    return results, status







