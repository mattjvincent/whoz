# -*- coding: utf_8 -*-

from __future__ import print_function
from future.utils import iteritems
from builtins import str

import sqlite3
import sys

import whoz.utils as utils
import whoz.search.search_database as sd

LOG = utils.get_logger()

if sys.version_info > (3,):
    long = int




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


def get_id(database, id, verbose=False):
    if verbose:
        LOG.debug('id={}'.format(str(id)))

    status = sd.get_status()
    query = SQL_ID_FULL
    results = {}

    if verbose:
        LOG.debug(str(query))

    try:
        conn = sd.connect_to_database(database)
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
        return None, sd.get_status(True, 'Database Error: ' + str(e))

    if status.error:
        return None, status

    return results, status






